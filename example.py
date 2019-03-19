from logging.config import dictConfig

dictConfig(
    {
        "version": 1,
        "formatters":
            {
                "json_formatter":
                    {
                        "()": "flask_json_logger.FlaskJSONFormatter",
                        "fmt": '%(created)f %(levelname)s %(name)s %(message)s',
                        "flask_context":
                            {
                                "g":
                                    {
                                        "includes": ["test", "notexists"],
                                        "mappings": {"test1": "test",
                                                     "notexists2": "notexists"}
                                    },
                                "request":
                                    {
                                        "includes": ["url", "remote_addr"]
                                    },
                                "session":
                                    {
                                        "includes": ["test2", "notexists2"],
                                        "mappings": {"test3": "test2",
                                                     "notexists3": "notexists2"}
                                    }
                            }
                    }
            },
        "handlers":
            {
                "file":
                    {
                        "class": "logging.FileHandler",
                        "level": "DEBUG",
                        "formatter": "json_formatter",
                        "filename": "test.log",
                        "mode": "w"     # for test purpose. use "mode": "a" in product
                    }
            },
        "loggers":
            {
                "example":
                    {
                        "handlers": ["file"],
                        "level": "DEBUG"
                    }
            }
    }
)


from flask import Flask, g, session, request
from logging import getLogger
logger = getLogger(__name__)

app = Flask(__name__)

app.secret_key = b'fdsiapouriewpqjrewqjro23'


@app.before_request
def before_request():
    g.test = "abc"
    session['test2'] = "test2"


@app.route("/", methods=["GET"])
def test():
    logger.info("test log")
    return "hello world"
