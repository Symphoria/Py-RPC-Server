def is_even(num):
    if num % 2 == 0:
        return True
    else:
        return False


def find_count(s, c):
    return s.count(c)


def find_sum(array):
    result = []

    for element in array:
        for x in element:
            result.append(x)

    return result
