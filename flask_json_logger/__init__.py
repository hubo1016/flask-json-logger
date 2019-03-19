from flask import current_app, g, request, session
from pythonjsonlogger.jsonlogger import JsonFormatter
from pychecktype import check_type, map_, NoMatch

_proxies = {'current_app': current_app,
            'g': g,
            'request': request,
            'session': session}


_flask_context_settings_type = \
    {
        "?includes": (None, [str]),
        "?excludes": [str],
        "?mappings": map_(str, str),
        "~": NoMatch
    }


_flask_context_type = \
    {
        '?current_app': _flask_context_settings_type,
        '?g': _flask_context_settings_type,
        '?request': _flask_context_settings_type,
        '?session': _flask_context_settings_type,
        "~": NoMatch
    }


class FlaskJSONFormatter(JsonFormatter):
    def __init__(self, *args, **kwargs):
        """
        :param flask_context: config for extracting fields from flask context.
                              supported keys are current_app, g, request, session
                              use `includes`, `excludes`, `mappings` to specify
                              necessary fields:

                                  includes:
                                      a list for keys to be included, or `None` for any keys
                                      (only available for `g` and `session`)

                                  excludes:
                                      a list of keys to be excluded, used with includes = `True`

                                  mappings:
                                      a dict `dest_key=>source_key` to rename keys to other names,
                                      e.g. `{"myurl": "url"}` add a field `myurl` with value from `url`

                              When context is not available, or keys are not found, they
                              are safely ignored.

        Other parameters are passed to pythonjsonlogger.jsonlogger.JsonFormatter
        """
        if 'flask_context' in kwargs:
            _flask_context = kwargs.pop('flask_context')
            _flask_context = check_type(_flask_context, _flask_context_type)
        else:
            _flask_context = {}
        super(FlaskJSONFormatter, self).__init__(*args, **kwargs)
        self._flask_context = _flask_context

    def add_fields(self, log_record, record, message_dict):
        super(FlaskJSONFormatter, self).add_fields(log_record, record, message_dict)
        if self._flask_context:
            # Add from flask context
            for k, all_, in_, attr in\
                    (('current_app', lambda x: (), hasattr, getattr),
                     ('g', lambda x: tuple(x), hasattr, getattr),
                     ('request', lambda x: (), hasattr, getattr),
                     ('session', lambda x: tuple(x), lambda x, k: k in x, lambda x, k, v=None: x.get(k, v))):
                if k in self._flask_context:
                    obj = _proxies[k]
                    props = self._flask_context[k]
                    if obj:
                        includes = props.get('includes', ())
                        if includes is None:
                            includes = all_(obj)
                        excludes = props.get('excludes', ())
                        if excludes:
                            excludes = set(excludes)
                            includes = [k for k in includes if k not in excludes]
                        for prop_k in includes:
                            if in_(obj, prop_k):
                                log_record[prop_k] = attr(obj, prop_k)
                        mappings = props.get('mappings', {})
                        for map_k, map_v in mappings.items():
                            if in_(obj, map_v):
                                log_record[map_k] = attr(obj, map_v)
