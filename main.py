import json
import requests
import sys
from flask import Flask, request, make_response
from flask_cors import CORS

import procedures
from serialize import marshal
from deserialize import unmarshal


app = Flask(__name__)
CORS(app)

with open("services.json") as data_file:
    signature = json.load(data_file)

registry_url = "https://rpc-registry-server.herokuapp.com/map"


def register_rpc(service_sign):
    headers = {
        'Content-Type': 'application/json'
    }
    result = requests.post(registry_url, data=json.dumps(service_sign), headers=headers)

    if result.status_code != 200:
        print('ERROR: RPC Registration Failed')

    return result


def call_proc(proc_name, args):
    if proc_name == 'is_even':
        return procedures.is_even(*args)
    elif proc_name == 'find_count':
        return procedures.find_count(*args)


@app.route('/', methods=['GET'])
def hello():
    return 'Hello World'


@app.route('/remote-call', methods=['POST'])
def remote_call():
    data = request.get_json()
    proc_name = data["serviceName"]
    marshalled_args = sorted(data['parameters'], key=lambda x: x['parameterPosition'])
    proc_signature = signature[proc_name]
    proc_parameters = sorted(proc_signature['parameters'], key=lambda x: x['position'])
    args = []

    for i, arg in enumerate(marshalled_args):
        args.append(unmarshal(arg['parameterValue'], proc_parameters[i]['type']))

    result = call_proc(proc_name, args)
    print(result)
    marshalled_result = marshal(result, proc_signature['returnType'])

    return make_response(json.dumps(marshalled_result)), 200


if __name__ == '__main__':
    register_rpc(signature['is_even'])
    app.run(debug=True)
