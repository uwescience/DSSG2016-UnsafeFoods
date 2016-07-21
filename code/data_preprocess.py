
# coding: utf-8

# In[2]:

import requests
import re
from time import sleep


def getUPC10(upc_list):
    """
    Returns list of the unique 10-digit UPCs from list of UPCs

    First find unique UPCs by inserting into a set, and then build a list of
    UPCs that are of length 10

    Parameters
    ----------
    upc_list: List of UPC numbers as strings

    Returns
    -------
    upc_10: List of unique UPCs that have length 10
       
    SAMPLE USAGE
    ------------    
    upc_list = ['030243507998', '3024386680', '3024386681', '3024386687',
    '3024386683', '3024302860'] 
    getUPC10(upc_list)
    """
    upc_10 = []
    upc_set = set(upc_list)
    for u in upc_set:
        if len(u) == 10:
            upc_10.append(u)
    return upc_10


def checkDigit(s):
    """
    Calculates the 12th 'check digit' from the 11 digit UPC ('Number system
    digit' + 10-digit UPC)
    
    Parameters
    ----------
    s: 11-digit long string
    
    Returns
    -------
    0, 10-remainder: check digit for an 11-digit UPC number

    (1) Add digits in odd positons
    (2) Multiply result of (1) * 3
    (3) Add digits in even positions
    (4) Add results of (2) and (3)
    (5) Find remainder of (4)
    (6) If (5) is 0, return 0, otherwise return 10 - (5)
    
    SAMPLE USAGE
    ------------
    # check digit is 8
    checkDigit("03024350799")
    """
    even_sum = 0
    odd_sum = 0
    for i in range(len(s)):
        if i % 2 == 0:
            odd_sum += int(s[i])
        else: 
            even_sum += int(s[i])
    remainder = (odd_sum * 3 + even_sum) % 10
    if remainder == 0:
        return 0
    else:
        return 10 - remainder

    
def UPC10to12(s):
    """
    Returns list of possible 12-digit UPCs for a 10-digit UPC given each
    possible 'Number system digit' in order of likelyhood 
    given overall frequency distribution of first digits 

    (No more than one UPC in the list actually exists)

    Parameters
    ----------
    s: String containing a 10-digit UPC

    Returns
    -------
    upc12_possible_list: List of possible twelve-digit UPCs with different
    start digits and a valid check digit

    SAMPLE USAGE
    ------------
    #first element of the returned list '030243507998' is the actual UPC
    UPC10to12("3024350799")
    """
    upc12_possible_list = []
    for num in [0, 7, 8, 6, 3, 1, 9, 2, 4, 5]:
        upc_11 = str(num)+s
        upc_12 = upc_11 + str(checkDigit(upc_11))
        upc12_possible_list.append(upc_12)
    return upc12_possible_list

def UPC10(upc, event_upcs12):
    upcs = list()
    for u12 in event_upcs12:
        if u12.find(upc) != -1:
            upcs.append(u12)
            return upcs
    for u12 in event_upcs12:
        if u12.find(upc[0:4]) != -1:
            u11_try = u12[0]+upc
            u12 =  u11_try + str(checkDigit(u11_try))
            upcs.append(u12)
            return upcs
    upcs = UPC10to12(upc)
    return upcs

def UPC11(upc, event_upcs12):
    upcs = list()
    for u12 in event_upcs12:
        if (u12.find(upc)) != -1:
            upcs.append(u12)
            return upcs
    u12 = upc + str(checkDigit(upc))
    upcs.append(u12)
    return upcs

def UPC13(upc):
    upcs = list()
    if upc[:2] == '00':
        u11_try = upc[1:-1]
        u12 =  u11_try + str(checkDigit(u11_try))
        upcs.append(u12)
        return upcs
    else:
        u11_try1 = upc[1:-1]
        u11_try2 = upc[2:]
        u12_1 =  u11_try1 + str(checkDigit(u11_try1))
        u12_2 =  u11_try2 + str(checkDigit(u11_try2))
        upcs.append(u12_1)
        upcs.append(u12_2)
        return upcs

def UPC14(upc):
    upcs = list()
    u11_try = upc[2:-1]
    u12 =  u11_try + str(checkDigit(u11_try))
    upcs.append(u12)
    return upcs

def getUPCS(upc, event_upcs12):
    """
    for rownum in range(enforce.shape[0]):
        for upc in enforce.upcs[rownum]:
            getUPCS(upc, enforce.event_upc12[rownum])
    """
    if len(upc) == 10:
        return UPC10(upc, event_upcs12)
    elif len(upc) == 11:
        return UPC11(upc, event_upcs12)
    elif len(upc) == 12:
        upc_list = [upc]
        return upc_list
    elif len(upc) ==13:
        return UPC13(upc)
    elif len(upc) ==14:
        return UPC14(upc)


# In[ ]:



