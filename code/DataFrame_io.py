
def listToString(string_list, nested = False):
    """
    Converts lists of strings to a delimited string

    Parameters (?Redundant?)
    ----------
    string_list: list of str (or list of list of str)
        list of strings (if nested = False (default))
        list of list of strings (if nested = True)
    nested: bool
        If false (default) `string_list` parameter passed is a list of strings
        if true, `string_list` parameter passed is a list of list of strings
        
    Returns
    -------
    string: str
        String representation of `string_list`, with elements of list separated by semicolons
        If nested=True, each element of inner list is separated by commas

    SAMPLE USAGE
    ------------    
    >>>listToString(['071117001648','079453469252','758108301566'])
    '071117001648;079453469252;758108301566;'

    TODO: nested=True

    """
    string = ''
    for inner in string_list:
        if nested:
            for s in inner:
                string+=(s+",")
        else:
            string+=inner
        string+=(";")
    return string

def listToStringCol(list_col, nested = False):

    """
    Converts column of lists of strings to a column of delimited strings

    Parameters
    ----------
    list_col: list of list of str (or list of list of list of str)
        Column of strings (if nested = False (default))
        Column of list of strings (if nested = True)
    nested: bool
        If false (default) `list_col` parameter passed is a column containing lists of strings
        if true, `list_col` parameter passed is a column containing lists of lists of strings
        
    Returns
    -------
    string_col: list of list of str
        List containing string representations of each entry of `list_col`, 
            with elements of list separated by semicolons
        If nested=True, each element of inner list is separated by commas


    SAMPLE USAGE
    ------------    
    >>> listToStringCol([[], ['041913122651','041913122565'], ['688264867050']])
    ['', '041913122651;041913122565;', '688264867050;']

    TODO: nested=True
    
    """

    string_col = list()
    for string_list in list_col:
        string_col.append(listToString(string_list, nested))
    return string_col

def stringToList(string, nested = False):

    """
    Converts delimited strings to lists of strings

    Parameters (?Redundant?)
    ----------
    string: str
        String representation of a list
    nested: bool
        If false (default) `string` parameter passed contains only semicolon delimiters
        if true, `string` parameter passed represents a nested list, with each element of
            the inner list separated by commas, and inner lists separated by semicolons
        
    Returns
    -------
    string_list: list of str (or list of list of str)


    SAMPLE USAGE
    ------------    
    >>>stringToList('071117001648;079453469252;758108301566;')
    ['071117001648', '079453469252', '758108301566']

    TODO: nested=True

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

    
    """
    Converts a column of delimited strings to a column containing lists of strings

    Parameters (?Redundant?)
    ----------
    string_col: list of str
        Column containing string representations of lists
    nested: bool
        If false (default) each string in `string_col` parameter passed contains only semicolon delimiters
        if true, each string in `string_col` parameter passed represents a nested list, with each element
            of the  inner list separated by commas, and inner lists separated by semicolons
        
    Returns
    -------
    list_col: list of list of str (or list of list of list of str)


    SAMPLE USAGE
    ------------    
    >>>stringToListCol(['', '041913122651;041913122565;', '688264867050;'])
    [[], ['041913122651', '041913122565'], ['688264867050']]
    TODO: nested=True

    """

    list_col = list()
    for string in string_col:
        list_col.append(stringToList(string, nested))
    return list_col