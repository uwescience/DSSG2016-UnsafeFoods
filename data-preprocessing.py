import requests
import re
from time import sleep

def getASIN(upc):
    """Query upctoasin.com to determine ASIN from UPC.

    First remove any non-numeric characters from the UPC (UPCs are often 
    provided with dashes between certain digits). Query the website and
    retrieve ASIN, then wait one second.

    SAMPLE USAGE
    ------------

    # Look up a single UPC
    getASIN("876063002233")

    # Loop over multiple UPCs. One of the below returns UPCNOTFOUND, presumably
    # because this UPC does not have an ASIN because it's not sold by Amazon:
    upc = ["876063002233", "013000006408", "895296001035", "0-86069-20030-8"]
    for i in upc:
        print(getASIN(i))

    """
    upc_dig = re.sub("[^0-9]", "", upc)
    url = "http://upctoasin.com/" + upc_dig
    response = requests.get(url)
    sleep(1) # Sleep for one second
    return(response.text)
