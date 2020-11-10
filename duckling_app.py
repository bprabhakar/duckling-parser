#!/usr/bin/env python

import flask
import json
import requests
import logging
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from time import time
import pendulum

app = flask.Flask(__name__)
CORS(app)

DUCKLING_ENDPOINT = "http://0.0.0.0:8000/parse"

@app.route("/duckling", methods=['POST', 'GET'])
def duckling():
    start_time = time()
    request_data = flask.request.args
    question = request_data['question']

    # data to be sent to api 
    data = {
        "locale":"en_US",
        "text":question
    }
    r = requests.post(url = DUCKLING_ENDPOINT, data = data) 
    duckling_resp = json.loads(r.text)

    # 1 - filter only time dim responses
    duckling_resp = [x for x in duckling_resp if x['dim']=='time'][0]

    # 2 - Output as an interval
    matched_text = duckling_resp['body']
    start_dt, end_dt = extract_interval(duckling_resp['value'], tz='Asia/Kolkata')
    latency = int(1000*(time() - start_time))
    response = {
        'question': question,
        'matched_text': matched_text,
        'interval':{
            'from': start_dt,
            'to': end_dt
        },
        'latency': f"{latency}ms"
    }
    response = flask.jsonify(response)
    response.status_code = 200
    return response

def extract_interval(raw_value, tz):
    if raw_value['type'] == 'interval':
        start_ts = pendulum.parse(raw_value['from']['value']).in_timezone(tz)
        end_ts = pendulum.parse(raw_value['to']['value']).in_timezone(tz)
    elif raw_value['type'] == 'value':
        start_ts = pendulum.parse(raw_value['value']).in_timezone(tz)
        end_ts = start_ts.end_of(raw_value['grain'])
    else:
        start_ts = pendulum.now(tz)
        end_ts = pendulum.now(tz)

    return start_ts.to_date_string(), end_ts.to_date_string()


if __name__ == "__main__":
    print("Ready to serve", flush=True)
    app.debug = True
    http_server = WSGIServer(('0.0.0.0', 8001), app)
    http_server.serve_forever()