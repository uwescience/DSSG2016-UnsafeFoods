import requests
import re
from time import sleep

def getASIN(upc):
    """Query upctoasin.com to determine ASIN from UPC.

    First remove any non-numeric characters from the UPC (UPCs are often 
    provided with dashes between certain digits). Query the website and
    retrieve ASIN, then wait one second.

    """
    upc_dig = re.sub("[^0-9]", "", upc)
    url = "http://upctoasin.com/" + upc_dig
    response = requests.get(url)
    sleep(1) # Sleep for one second
    return(response.text)
