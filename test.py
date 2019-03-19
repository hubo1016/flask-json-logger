from __future__ import print_function
from subprocess import Popen


if __name__ == '__main__':
    import requests
    import json
    import os
    import signal
    os.environ['FLASK_APP'] = 'example.py'
    with Popen(["python", "-m", "flask", "run", "-h", "127.0.0.1", "-p", "8999"],
               shell=False) as p:
        try:
            r = requests.get('http://127.0.0.1:8999/')
            r.raise_for_status()
            assert r.text == "hello world"
        finally:
            p.terminate()
    with open('test.log', 'r') as f:
        data = json.load(f)
        print(data)
        assert isinstance(data.pop('created'), float)
        assert data == {"levelname": "INFO",
                        "name": "example",
                        "message": "test log",
                        "test": "abc",
                        "test1": "abc",
                        "url": "http://127.0.0.1:8999/",
                        "remote_addr": "127.0.0.1",
                        "test2": "test2",
                        "test3": "test2"}
