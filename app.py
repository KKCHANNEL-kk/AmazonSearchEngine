import time
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
    start = time.time()
    result = service.handle_query(q, field)
    asins = [r['asin'] for r in result]
    shop_advice, query_advice = service.get_advice(asins)
    end = time.time()
    r = {}
    r['result'] = result
    r['time'] = end-start
    r['shop_advice'] = shop_advice
    r['query_advice'] = query_advice

    return Response(json.dumps(r),  mimetype='application/json')


# if __name__ == '__main__':
service.start_service()
app.run(host='127.0.0.1', port=5000, debug=True)
