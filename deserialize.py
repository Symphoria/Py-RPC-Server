def unmarshal_boolean(arg):
    if int(arg) == 1:
        return True
    else:
        return False


def unmarshal_int(arg):
    return int(arg)


def unmarshal_float(arg):
    return float(arg)


def unmarshal(arg, arg_type):
    if arg_type == 'int':
        return unmarshal_int(arg)
    elif arg_type == 'boolean':
        return unmarshal_boolean(arg)
    elif arg_type == 'float':
        return unmarshal_float(arg)

    return arg

