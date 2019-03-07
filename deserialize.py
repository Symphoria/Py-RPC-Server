import json


def unmarshal_boolean(arg):
    if int(arg) == 1:
        return True
    else:
        return False


def unmarshal_int(arg):
    return int(arg)


def unmarshal(arg, arg_type):
    if arg_type == 'int':
        return unmarshal_int(arg)
    elif arg_type == 'boolean':
        return unmarshal_boolean(arg)

    return json.loads(arg)
