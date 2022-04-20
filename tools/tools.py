def cmp(a, b):
    return (a > b) - (a < b) 

def cmp_str(element1, element2):
    """
    compare number in str format correctley
    """
    try:
        return cmp(int(element1), int(element2))
    except ValueError:
        return cmp(element1, element2)


def quasi_to_key(value_list, sep=';'):
    """convert qid list to str key
    value (splited by sep). This fuction is value safe, which means
    value_list will not be changed.
    return str list.
    """
    return sep.join(value_list)

def get_num_list_from_str(stemp):
    """
    if float(stemp) works, return [stemp]
    else return, stemp.split(',')

    """
    try:
        float(stemp)
        return [stemp]
    except ValueError:
        return stemp.split(',')
