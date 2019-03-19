from setuptools import setup

setup(
    name='flask-json-logger',
    version='0.1.0',
    packages=['flask_json_logger'],
    url='https://github.com/hubo1016/flask-json-logger',
    license='Apache 2.0',
    author='hubo',
    author_email='hubo1016@126.com',
    description='Simple JSON log formatter with additional flask context variables',
    install_requires=["python-json-logger>=0.1.2", "Flask", "pychecktype>=1.4.1"]
)
