def listToString(string_list, nested = False):
    string = ''
    for inner in outer:
        if nested:
            for s in inner:
                string+=(s+",")
        else:
            string+=inner
        string+=(";")
    return string

def listToStringCol(list_col, nested = False):
    string_col = list()
    for string_list in list_col:
        string_col.append(listToString(string_list, nested))
    return list_col

def stringToList(string, nested = False):
    """

    stringToListCol(string, True)

    stringToListCol(string)

    """

    outer = string.split(';')[0:-1]
    if nested:
        string_list = list()
        for inner in outer:
            string_list.append([substring for substring in inner.split(",")[0:-1]])
        return string_list
    else:
        return outer


def stringToListCol(string_col, nested = False):
    list_col = list()
    for string in string_col:
        list_col.append(stringToList(string, nested))
    return list_col