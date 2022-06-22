from flask import Flask
import service
import json

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/get_n")
def get_n():
    N = service.info['title']['N']
    return json.dumps({"N":N})


if __name__ == '__main__':
    service.start_service()
    app.run(host='127.0.0.1', port=5000, debug=True)
