import requests
import json
from flask import jsonify
def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    req_ip = '35.226.209.144'
    port_number = '8080'
    url = 'http://{}:{}/v1/models/eos:predict'.format(req_ip, port_number)
    response = requests.post(url, data=json.dumps(request_json))
    return jsonify(response.json())
