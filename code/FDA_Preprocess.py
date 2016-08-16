from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import itertools

#Constants
UPC_PATTERN_TEXT = '\D\d[-\s](\d{6}[\s-]?\d{6})|(\d{1,2}[-\s]?\d{1,2}[-\s]?\d{5}[\s-]?\d{5}[-\s]?\d)|(\d{13})|(\d{12})|(\d[\s-]\d{5}[-\s]?\d{5}[- \r\n\f]\d)|(\d[\s-]\d{5}[-\s]?\d{5})|(\d{6}[-\s]\d{5}[-\s]?\d)|(\d{6}[\s-]\d{5})|(\d{5}[- \r\n\f]?\d{5})'
UPC_PATTERN_PAGE = '\D(\d{12})\D|\D(\d[\s-]\d{5}[-\s]?\d{5}[-\s]\d)\D|\D(\d{6}[-\s]\d{5}[-\s]?\d)\D|\D(\d{5}[\s-]?\d{5})\D|\D(\d{6}[\s-]\d{5})\D'

##TODO: add remove non-digits
def removeSymbols(upc_list): 

    """
    Removes dashes and spaces in place from each element in a list of strings.
    
    Parameters
    ----------
    upc_list: list of str
        List of UPC numbers as strings
    
    Raises
    ------
    TODO
       
    SAMPLE USAGE
    ------------
    >>> l = ['7-01248-00301-2', '7 01248-01096 6', '7 01248 00156 8']
    >>> removeSymbols(l)
    >>> l
    ['701248003012', '701248010966', '701248001568']
    """
    
    for index in range(len(upc_list)):
        upc_list[index] = upc_list[index].replace('-','')
        upc_list[index] = upc_list[index].replace(' ','')
        upc_list[index] = re.sub("\D","", upc_list[index])

    
def MakeUPCList(text, link = False, re_pattern = None):
    """
    Finds groups of characters in text that match specified pattern 
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
        
    Raises
    ------
    TODO
    
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
        removeSymbols(upc_list)
    return upc_list   
        
def makeUPCCol(string_list, link = False, re_pattern = None, verbose = True):
    """
    Creates a list of lists of strings in that match specified pattern 
    for each row in a list of strings using MakeUPCList function.
    
    Parameters
    ----------
    string_list: list of str ?(or pandas Series of strings)?
        List of string to be searched (if link = False (default))
        List of urls linking to pages that contain the text to be searched (if link = True)
    link: bool
        If false (default) `string_list` parameter passed in is list of strings to be searched;
        if true, `string_list` parameter passed in is a list of urls 
            linking to pages with text to be searched    
    re_pattern: str 
        Regex pattern to search for
        UPC_PATTERN_TEXT is default if link = False (default)
        UPC_PATTERN_PAGE is default if link = True
        
    Returns
    -------
    upc_col: list of lists of str
        List of lists of strings from each row of `str_list` that matched `re_pattern`.
        `upc_col` is the same length as `string_col`. 
        
    Raises
    ------
    TODO
    
    Notes ?Repeat?   
       
    SAMPLE USAGE
    ------------    
    >>> makeUPCCol(['Lot # 07.31.2015  UPC#  7 08953 60203 5',
        'Lot # 07.31.2015  UPC#  7 08953 60101 4',
        'Lot # 07.31.2015  UPC#  7 08953 60102 1'])
    [['708953602035'], ['708953601014']]

    TODO:
    show passing series?

    """ 
    upc_col = list()
    for idx, val in enumerate(string_list):
        if verbose:
            if idx % 500 == 0:
                print(idx, "rows processed")
            if idx+1 == len(string_list):
                print(idx+1, "rows processed : COMPLETE")
        upc_list = MakeUPCList(val, link, re_pattern)
        upc_col.append(upc_list)
    return pd.Series(upc_col, string_list.index)

def makeEventUPCCol(df, upc_colname, event_colname, upc_length = 12):
    event_upc_lists = [[upc for upc in df[df[event_colname] == event][upc_colname]] for event in df[event_colname]]
    if upc_length is None:
        event_upcs = [[u for u in set(itertools.chain.from_iterable(u_list))] for u_list in event_upc_lists]
    else:
        event_upcs = [[u for u in set(itertools.chain.from_iterable(u_list)) if len(u) == upc_length] for u_list in event_upc_lists]
    return pd.Series(event_upcs)




    

    
    