from flask import Flask, request, Response, render_template, redirect, url_for
import service
import json

app = Flask(__name__)

# 跨域支持


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


app.after_request(after_request)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/get_n")
def get_n():
    N = service.info['title']['N']
    return json.dumps({"N": N})


@app.route("/query", methods=['GET'])
def query():
    q = request.args.get('query')
    field = request.args.get('field')
    result = service.handle_query(q, field)
    return Response(json.dumps(result),  mimetype='application/json')


if __name__ == '__main__':
    service.start_service()
    app.run(host='127.0.0.1', port=5000, debug=True)
