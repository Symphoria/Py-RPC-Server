import json
from flask import Flask, request, make_response

import procedures
from serialize import marshal
from deserialize import unmarshal


app = Flask(__name__)

signature = {
    'is_even': {
        'name': 'is_even',
        'parameters': [{'position': 1, 'type': 'int'}],
        'server': "http://127.0.0.1:5000/remote-call",
        'returnType': 'boolean'
    },
    'find_count': {
        'name': 'find_count',
        'parameters': [{'position': 1, 'type': 'string'}, {'position': 2, 'type': 'char'}],
        'server': "http://127.0.0.1:5000/remote-call",
        'returnType': 'int'
    }
}


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
    proc_name = data["proc_name"]
    marshalled_args = data["args"]
    proc_signature = signature[proc_name]
    proc_parameters = sorted(proc_signature['parameters'], key=lambda x: x['position'])
    args = []

    for i, arg in enumerate(marshalled_args):
        args.append(unmarshal(arg, proc_parameters[i]['type']))

    result = call_proc(proc_name, args)
    print(result)
    marshalled_result = marshal(result, proc_signature['returnType'])

    return make_response(json.dumps(marshalled_result)), 200


if __name__ == '__main__':
    app.run(debug=True)
