def sanitizePath(path):
    '''
    incase the path starts with a / then it just removes it

    eg. /a/b -> a/b

    This is so that other functions can work as expected

    :param path:
    :return:
    '''
    if path[0] == "/":
        return path[1:]
    return path