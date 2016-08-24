import requests
import re
from time import sleep
import pandas as pd


def checkDigit(upc_11):
    """
    Calculates the 12th 'check digit' from the 11 digit UPC 
    ('Number system digit' + 10-digit UPC)
    
    Parameters
    ----------
    upc_11: str
        11-digit UPC
    
    Returns
    -------
    check_digit: str
        check digit calculated using algorithm explained in Notes

    Notes
    -----
    A check digit is the final number on a barcode, 
    used to check whether the UPC is valid. It is calulated using
    the first 11 digits using the following algorithm:

    (1) Add digits in odd positons
    (2) Multiply result of (1) * 3
    (3) Add digits in even positions
    (4) Add results of (2) and (3)
    (5) Find remainder of (4)
    (6) If (5) is 0, return 0, otherwise return 10 - (5)
    
    SAMPLE USAGE
    ------------
    >>> checkDigit('03024350799')
    '8'

    """
    even_sum = 0
    odd_sum = 0
    for index in range(len(upc_11)):
        if index % 2 == 0:
            odd_sum += int(upc_11[index])
        else: 
            even_sum += int(upc_11[index])
    remainder = (odd_sum * 3 + even_sum) % 10
    if remainder == 0:
        check_digit = 0
    else:
        check_digit = 10 - remainder
    return str(check_digit)

    
#TODO: Add website explaining Number system digit to "See Also"
def makePossibleUPC12List(upc_10):
    """
    Creates list of possible 12-digit UPCs for a 10-digit UPC 
    given each possible 'number system' digit (0, 7, 8, 6) in order 
    of likelyhood given overall frequency distribution of first digits 

    Parameters
    ----------
    upc_10: str
        10 digit UPC

    Returns
    -------
    upc12_possible_list: list of str
        List of 4 possible 12-digit UPCs with different 
        initial 'number system' digits and a valid check digit

    SAMPLE USAGE
    ------------
    #first element of the returned list '030243507998' is the actual UPC
    >>> makePossibleUPC12List('3024350799')
    ['030243507998', '730243507997', '830243507994', '630243507990']
    """

    upc12_possible_list = []
    for num in [0, 7, 8, 6]:
        upc_11 = str(num)+upc_10
        upc_12 = upc_11 + str(checkDigit(upc_11))
        upc12_possible_list.append(upc_12)
    return upc12_possible_list


def UPC10Process(upc10, event_upc12_list = None):
    """
    Constructs a 12-digit UPC, or a list of possible 12-digit UPCs based on inputted 10-digit UPC.

    If a event 12 digit upc list is passed, attempts to match against this list
    to find "certain" 12-digit UPC. If no match is found, create a possible list
    of 12-digit UPCs using makePossibleUPC12List function. 

    Parameters
    ----------
    upc10: str
        10-digit UPC
    event_upc12_list: list of str
        List of 12-digit UPC strings from the same recall event as `upc10`

    Returns
    -------
    list of str
        List of 12-digit UPC string(s) based on `upc10`

    Raise
    -----
    If the UPC is not 10 digits, the function will throw a ValueError.

    SAMPLE USAGE
    ------------
    >>> UPC10Process('7074250323')
    ['070742503237', '770742503236', '870742503233', '670742503239']
    >>> UPC10Process('1159653102', ['011596242101', '041497058440', '011596550916'])
    ['011596531021']
    >>> UPC10Process('707425032')
    ValueError: 707425032: UPC must be 10 digits long
    """ 
    if len(upc10) != 10:
        raise ValueError(upc10+ ": UPC must be 10 digits long")

    if event_upc12_list is not None:
        for e_upc12 in event_upc12_list:
            if e_upc12.find(upc10) != -1:
                return [e_upc12]
        for e_upc12 in event_upc12_list:
            if e_upc12.find(upc10[0:4]) != -1:
                upc11_match = e_upc12[0]+upc10
                upc12_match =  upc11_match + str(checkDigit(upc11_match))
                return [upc12_match]

    upc12_list = makePossibleUPC12List(upc10)
    return upc12_list 


def UPC11Process(upc11):
    """
    Constructs a 12-digit UPC based on an 11-digit UPC input. 

    Calculate check digit using checkDigit function and 
    append the it to the 11-digit code. 

    Parameters
    ----------
    upc11: str
        11-digit UPC

    Returns
    -------
    list of str
        List containing a single 12-digit UPC string based on `upc11`

    Raise
    -----
    TODO
    If the UPC is not 11 digits, the function will throw a ValueError.

    SAMPLE USAGE
    ------------
    >>> UPC11Process('01159651202')
    ['011596512020']
    >>> UPC11Process('011596512021')
    ValueError: '011596512021': UPC must be 11 digits long
    """ 
    if len(upc11) != 11:
        raise ValueError("'%s': UPC must be 11 digits long" % (upc11))
    upc12 = upc11 + str(checkDigit(upc11))
    return [upc12]

def UPC13Process(upc13, event_upc12_list = None):
    """
    Constructs a 12-digit UPC, or a list of possible 12-digit UPCs based on inputted 13-digit UPC.

    If a event 12 digit upc list is passed, attempts to match against this list
    to find "certain" 12-digit UPC. If no match is found, create a possible list
    of 12-digit UPCs.

    Parameters
    ----------
    upc13: str
        13-digit UPC
    event_upc12_list: list of str
        List of 12-digit UPCs from the same recall event as `upc13`

    Returns
    -------
    list of str
        List of 12-digit UPC string(s) based on `upc13`

    Raise
    -----
    If the UPC is not 13 digits, the function will throw a ValueError.

    SAMPLE USAGE
    ------------
    >>> UPC13Process('7594465008860', ['759465009829', '030034303259', '717524778178'])
    ['759446500888']
    >>> UPC13Process('0026967600000')
    ['026967600008']
    >>>  UPC13Process('0893467803068')
    ['893467803068', '934678030680']
    >>> UPC13Process('089346780306')
    ValueError: '089346780306': UPC must be 13 digits long
    """ 

    if len(upc13) != 13:
        raise ValueError("'%s': UPC must be 13 digits long" % (upc13))

    if event_upc12_list is not None:
        for e_upc12 in event_upc12_list:
            if e_upc12.find(upc13) != -1:
                return [e_upc12]
        for e_upc12 in event_upc12_list:
            if e_upc12.find(upc13[0:4]) != -1:
                upc11_match = upc13[0:11]
                upc12_match = upc11_match + str(checkDigit(upc11_match))
                return [upc12_match]
            if e_upc12.find(upc13[1:5]) != -1:
                upc11_match = upc13[1:-1]
                upc12_match = upc11_match + str(checkDigit(upc11_match))
                return [upc12_match]

    upc11_guess1 = upc13[1:-1]
    upc11_guess2 = upc13[2:]
    upc12_guess1 =  upc11_guess1 + str(checkDigit(upc11_guess1))
    upc12_guess2 =  upc11_guess2 + str(checkDigit(upc11_guess2))
    if upc13[:2] == '00':
        return [upc12_guess1]
    else:
        upc12_list = [upc12_guess1, upc12_guess2]
    return upc12_list

def UPC14Process(upc14):
    """
    Constructs a 12-digit UPC from based on inputted 14-digit UPC

    Parameters
    ----------
    upc14: str
        14-digit UPC

    Returns
    -------
    list of str
        List containing a single 12-digit UPC string based on `upc14`

    Raise
    -----
    If the UPC is not 14 digits, the function will throw a ValueError.

    SAMPLE USAGE
    ------------
    >>> UPC14Process('10049022808956')
    ['049022808959']
    >>> UPC14Process('1004902280895')
    ValueError: '1004902280895': UPC must be 14 digits long
    """ 

    if len(upc14) != 14:
        raise ValueError("'%s': UPC must be 14 digits long" % (upc14))

    upc11_guess = upc14[2:-1]
    upc12_guess =  upc11_guess + str(checkDigit(upc11_guess))
    return [upc12_guess]

def makeUPCProcessedList(upc_list, event_upc12_list = None):
    """
    Creates list of 12 digit UPCs from a list of UPCs, using different UPCProcess
    functions based on the length of each UPC

    Parameters
    ----------
    upc_list: list of str or str
        List of UPC strings of lengths 10 through 14
    event_upc12_list: list of str
        List of 12-digit UPCs from the same recall event as UPCs in `upc_list`

    Returns
    -------
    list of list of str
        List of lists of 12-digit UPCs in which each inner list corresponds
        to a UPC in upc_list

    SAMPLE USAGE
    ------------
    >>> makeUPCProcessedList(['9654700204','00896547002306'], ['810126020215', '810126020208', '896547002641'])
    [['896547002047'], ['896547002306']]
    >>> makeUPCProcessedList(['1076618323225','0815579901','10766818323119'], ['766818312604','763089280601'])
    [['076618323220', '766183232255'],
    ['008155799015', '708155799014', '808155799011', '608155799017'],
    ['766818323112']]
    >>> makeUPCProcessedList('046567021218')
    [['046567021218']]
    >>> makeUPCProcessedList(['877971002','10133016132','141087797100274'])
    [['UPClength=9'], ['101330161321'], ['UPClength=15']]
"""

    upc_processed_nested = list()

    if isinstance(upc_list, str):
        upc_list = [upc_list]

    for upc in upc_list:
        if len(upc) == 10:
            upc_processed_nested.append(UPC10Process(upc, event_upc12_list))
        elif len(upc) == 11:
            upc_processed_nested.append(UPC11Process(upc))
        elif len(upc) == 12:
            upc_processed_nested.append([upc])
        elif len(upc) ==13:
            upc_processed_nested.append(UPC13Process(upc, event_upc12_list))
        elif len(upc) ==14:
            upc_processed_nested.append(UPC14Process(upc))
        else:
            upc_processed_nested.append(["UPClength=%d" %(len(upc))])
    return upc_processed_nested




#TODO: Decide about sleep
def getASIN(upc_list):
    """
    TODO: Update
    Queries UPCtoASIN.com to determine ASIN from UPC. If the UPC is 12 digits,
    query the website and retrieve ASIN, then wait one second (per API rate limit)

    Parameters
    ----------
    upc_list: list of str or str
        List of 12-digit UPC string(s)
    
    Returns
    -------
    asin_list: list of str
        List string(s) containing either a valid Amazon ID (ASIN) or "UPCNOTFOUND"

    Raise
    -----
    TODO
    If any of the UPCs are not 12 digits, the function will throw a ValueError.

    Notes
    -----
    TODO
    API problems

    SAMPLE USAGE
    ------------
    >>> getASIN('876063002233')
    ['B001BCH7KM']
    >>> getASIN('030243507898')
    ['UPCNOTFOUND']
    >>> getASIN(['876063002233', '030243507898'])
    ['B001BCH7KM', 'UPCNOTFOUND']
    >>> getASIN(['876063002233', '03024350789'])
    ValueError: 03024350789: UPC must be 12 digits long

    """
    if isinstance(upc_list, str):
        upc_list = [upc_list]

    asin_list = list()
    for upc in upc_list:
        if len(upc) != 12:
            raise ValueError(upc+ ": UPC must be 12 digits long")
        url = "http://upctoasin.com/" + upc
        response = requests.get(url)
        if len(response.text) > 12:
            sleep(1)    
            response1 = requests.get(url)
            asin_list.append(response1.text)
        else:
            asin_list.append(response.text)
    return asin_list


def getASINList(upc_processed_nested):
    """
    """
    asin_nested = [getASIN(upc_12) for upc_12 in upc_processed_nested]
    return asin_nested

def MakeUPCProcessedASINCol(df, upc_colname, rowrange = None, event_upc12_colname = None, verbose = True):
    u_col = list()
    a_col = list()
    tic()
    if rowrange is None:
        rowrange = df.shape[0]

    for idx in range(rowrange[0], rowrange[1]):
        if verbose:
            if idx % 100 == 0:
                print(idx, "row processed")
                toc()
        if event_upc12_colname is None:
            event_upc12_list = [upc for upc in df[upc_colname][idx] if len(upc) == 12]
            upc_processed = getUPCProcessedList(df[upc_colname][idx], event_upc12_list)
        elif event_upc12_colname in df.columns:
            upc_processed = getUPCProcessedList(df[upc_colname][idx], df[event_upc12_colname][idx])
        else: 
            upc_processed = getUPCProcessedList(df[upc_colname][idx])
        u_col.append(upc_processed)
        a_col.append(getASINList(upc_processed))
    return [u_col, a_col]

def MakeRecallReviewTuples(recall_upc_series, recall_asin_series, review_asin_list, recall_number_series = None, verbose = True):
    tuples = list()
    if not isinstance(recall_upc_series,pd.Series) or not isinstance(recall_asin_series, pd.Series):
        raise TypeError("Parameter is not of type Series")
    else:
        if len(recall_upc_series) != len(recall_asin_series):
            raise ValueError("Series must be same length")
    for idx, asin_entry in enumerate(recall_asin_series):
        if verbose:
            if idx % 100 == 0:
                print(idx, "row processed")
        upc_entry = recall_upc_series[idx]
        for n, asin_list in enumerate(asin_entry):
            for m, asin in enumerate(asin_list):
                if len(asin) == 10:
                    if asin in review_asin_list:
                        upc = upc_entry[n][m]
                        if recall_number_series is None:
                            recall_number = idx
                        else:
                            recall_number = recall_number_series[n][m]
                        tuples.append((upc, asin, recall_number))
    return tuples



