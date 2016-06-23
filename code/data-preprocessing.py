import requests
import re
from time import sleep


def getUPC10(upc_list):
    """
    Returns list of the unique 10-digit UPCs from list of UPCs
       
    First find unique UPCs by inserting into a set, and then build a list of
    UPCs that are of length 10
       
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
    possible 'Number system digit' 

    (No more than one UPC in the list actually exists)

    SAMPLE USAGE
    ------------
    #first element of the returned list '030243507998' is the actual UPC
    UPC10to12("3024350799")
    """
    upc12_possible_list = []
    for num in [0, 1, 6, 7, 8]:
        upc_11 = str(num)+s
        upc_12 = upc_11 + str(checkDigit(upc_11))
        upc12_possible_list.append(upc_12)
    return upc12_possible_list


def getASIN(upc):
    """
    Query UPCtoASIN.com to determine ASIN from UPC.

    First, any non-numeric characters are removed from the UPC (UPCs are often
    provided with dashes between certain digits).

    If the resulting UPC is not twelve digits, the function will throw a
    ValueError.
    
    If the UPC is twelve digits, query the website and retrieve ASIN, then wait
    one second (per API rate limit).

    SAMPLE USAGE
    ------------

    # Look up a single UPC
    getASIN("876063002233")
    getASIN("8760630022")       # Throws an error

    # Loop over multiple UPCs. One of the below returns UPCNOTFOUND, presumably
    # because this UPC does not have an ASIN because it's not sold by Amazon:
    upc = ["876063002233", "013000006408", "895296001035", "0-86069-20030-8"]
    for i in upc:
        print(getASIN(i))
    """
    upc_dig = re.sub("[^0-9]", "", upc)  # Remove non-numeric characters first
    if len(upc_dig) != 12:
        raise ValueError("UPC must be twelve digits long")
    else:
        url = "http://upctoasin.com/" + upc_dig
        response = requests.get(url)
        sleep(1)                # Sleep for one second
        return(response.text)
