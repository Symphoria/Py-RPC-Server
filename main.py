import json
import requests
from flask import Flask, request, make_response
from flask_cors import CORS
from flask_pymongo import PyMongo

import procedures
from serialize import marshal
from deserialize import unmarshal


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
CORS(app)
mongo = PyMongo(app)

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


def check_duplicate(client_id, request_no):
    stored_result = mongo.db.history.find_one({"clientId": client_id, "requestNo": request_no})

    if stored_result:
        return True, stored_result['result']
    else:
        return False, 'No stored result'


def update_stored_result(client_id, request_no, result):
    stored_result = mongo.db.history.find_one({'clientId': client_id})

    if stored_result:
        mongo.db.history.update_one({'clientId': request.remote_addr}, {
            '$set': {
                'requestNo': request_no,
                'result': result
            }
        })
    else:
        mongo.db.history.insert_one({'clientId': client_id, 'requestNo': request_no, 'result': result})


@app.route('/', methods=['GET'])
def hello():
    return 'Hello World'


@app.route('/remote-call', methods=['POST'])
def remote_call():
    data = request.get_json()
    is_duplicate, stored_result = check_duplicate(request.remote_addr, data['request_no'])

    if is_duplicate:
        return make_response(stored_result), 200

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
    json_response = json.dumps(marshalled_result)

    update_stored_result(request.remote_addr, data['request_no'], json_response)

    return make_response(json_response), 200


if __name__ == '__main__':
    # register_rpc(signature['find_count'])
    app.run(debug=True)
