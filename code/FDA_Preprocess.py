from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import itertools

UPC_PATTERN_TEXT = '\D\d[-\s](\d{6}[\s-]?\d{6})|(\d{1,2}[-\s]?\d{1,2}[-\s]?\d{5}[\s-]?\d{5}[-\s]?\d)|(\d{13})|(\d{12})|(\d[\s-]\d{5}[-\s]?\d{5}[- \r\n\f]\d)|(\d[\s-]\d{5}[-\s]?\d{5})|(\d{6}[-\s]\d{5}[-\s]?\d)|(\d{6}[\s-]\d{5})|(\d{5}[- \r\n\f]?\d{5})'
UPC_PATTERN_PAGE = '\D(\d{12})\D|\D(\d[\s-]\d{5}[-\s]?\d{5}[-\s]\d)\D|\D(\d{6}[-\s]\d{5}[-\s]?\d)\D|\D(\d{5}[\s-]?\d{5})\D|\D(\d{6}[\s-]\d{5})\D'

def removeNonDigits(upc_list): 

    """
    Removes non-digits in place from each element in a list of strings
    
    Parameters
    ----------
    upc_list: list of str
        List of UPCs as strings
    
    SAMPLE USAGE
    ------------
    >>> l = ['7-01248-00301-2', '7 01248-01096 6', '7 01248 00156 8']
    >>> removeNonDigits(l)
    >>> l
    ['701248003012', '701248010966', '701248001568']
    """
    
    for index in range(len(upc_list)):
        upc_list[index] = re.sub("\D","", upc_list[index])

    
def makeUPCList(text, link = False, re_pattern = None):
    """
    Finds unique groups of characters in text that match specified pattern 
    and removes dashes and spaces from matched strings using removeSymbols function.  
    
    Parameters
    ----------
    text: str
        String to be searched (if link = False (default))
        Url that links to page containing the text to be searched (if link = True)
    link: bool
        If false (default) `text` parameter passed in is string to be searched;
        if true, `text` parameter passed in is a link to a page with text to be searched    
    re_pattern: str 
        Regex pattern to search for
        UPC_PATTERN_TEXT is default if link = False (default)
        UPC_PATTERN_PAGE is default if link = True
        
    Returns
    -------
    upc_list: list of str
        List of strings from `text` that matched `re_pattern`. If no match is found,
        an empty list is returned.

    Notes
    -----
    Default regex patterns those that are optimal for finding UPCs in texts of different formats
        UPC_PATTERN_TEXT is the optimal pattern for finding UPCs in a text blob
        UPC_PATTERN_PAGE is the optimal pattern for finding UPCs in strings of xml format   
       
    SAMPLE USAGE
    ------------    
    >>> MakeUPCList("12/454-gm UPC (071117182415), 6/1.25-KG UPC (0 00 71117-61227 1)")
    ['071117182415', '00071117612271']
    >>> MakeUPCList("http://www.fda.gov/Safety/Recalls/ucm443680.htm", True)
    ['607238300218', '607238300201', '607238300201']
    >>>
    ['071117182415']
    """ 
    
    if link:
        if re_pattern is None:
            re_pattern = UPC_PATTERN_PAGE
        try:
            upc_url = urlopen(text)
            upc_text = BeautifulSoup(upc_url,"html.parser")    
        except HTTPError:
            upc_text = ""
    else: 
        if re_pattern is None:
            re_pattern = UPC_PATTERN_TEXT
        upc_text = text
        
    upc_list = list()
    p = re.compile(re_pattern)
    upc_match = re.findall(p,str(upc_text)) 
    for match_group in upc_match:
        if isinstance(match_group,tuple):
            upc_list.extend([match for match in match_group if match != ''])
        else:
            upc_list.append(match_group) 
        removeNonDigits(upc_list)
    return list(set(upc_list))
        
def makeUPCCol(string_col, link = False, re_pattern = None, verbose = True):
    """
    Creates a list of strings that match specified pattern 
    for each row in a column of strings using MakeUPCList function.
    
    Parameters
    ----------
    string_col: list of str
        Column of strings to be searched (if link = False (default))
        Column of urls linking to pages that contain the text to be searched (if link = True)
    link: bool
        If false (default) `string_col` parameter passed in is column of strings to be searched;
        if true, `string_col` parameter passed in is a column of urls 
            linking to pages with text to be searched    
    re_pattern: str 
        Regex pattern to search for
        UPC_PATTERN_TEXT is default if link = False (default)
        UPC_PATTERN_PAGE is default if link = True
    verbose: bool
        If true (default), print "n rows processed" for each 500th row, and print total number
        of rows processed when complete

    Returns
    -------
    upc_col: list of list of str
        List of lists of strings from each row of `string_col` that matched `re_pattern`.
        `upc_col` is the same length as `string_col`. 

    SAMPLE USAGE
    ------------    
    >>> makeUPCCol(['Lot # 07.31.2015  UPC#  7 08953 60203 5',
        'Lot # 07.31.2015  UPC#  7 08953 60101 4',
        'Lot # 07.31.2015  UPC#  7 08953 60102 1'])
    [['708953602035'], ['708953601014'], ['708953601021']]

    """ 
    upc_col = list()
    for idx, string in enumerate(string_col):
        if verbose:
            if idx % 500 == 0:
                print(idx, "rows processed")
            if idx+1 == len(string_col):
                print(idx+1, "rows processed : COMPLETE")

        upc_list = makeUPCList(string, link, re_pattern)
        upc_col.append(upc_list)
    return upc_col

def makeEventUPCCol(upc_col, event_col, upc_length = 12):
    """
    Creates list of all FDA event UPCs corresponding to each FDA recall row


    Parameters
    ----------
    upc_col: list of list of str
        List of list of UPCs where inner lists are UPCs associated with a FDA Recall
    event_col: list of str
        List of FDA Recall Event IDs corresponding to each FDA recall 
    upc_length: int
        Length of UPC to be included in `event_col`
        Default value is 12, the most useful for comparison and pattern matching (use with UPC_Process module)
        If upc_length=None, UPCs of all lengths are included


    Returns
    -------
    event_upc_col: list of list of str
        List of list of UPCs where inner lists are all UPCs (of length upc_length) associated with a FDA Recall Event

    Raises
    ------
    If the lists are not the same length, function will raise Value Error


    Notes
    -----
    FDA Recalls contain 1 or more recalled product 
    FDA Recall Events contain 1 or more related FDA Recalls 

    SAMPLE USAGE
    ------------
    >>> makeEventUPCCol([['85556900305'], ['855569003135'], ['030223009146'], ['045009101167']],
                            [70071, 70071, 70104, 70104])
    [['855569003135'],['855569003135'], ['045009101167', '030223009146'], ['045009101167', '030223009146']]
        

    """
    if len(upc_col) != len(event_col):
            raise ValueError("lists must be same length")
    
    df = pd.DataFrame({"upc": upc_col , "event" : event_col}) 

    event_upc_lists = [[upc for upc in df[df["event"] == event]["upc"]] for event in df["event"]]
    if upc_length is None:
        event_upc_col = [[u for u in set(itertools.chain.from_iterable(u_list))] for u_list in event_upc_lists]
    else:
        event_upc_col = [[u for u in set(itertools.chain.from_iterable(u_list)) if len(u) == upc_length] for u_list in event_upc_lists]
    
    return event_upc_col
    