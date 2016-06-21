import requests
from time import sleep

def getASIN(upc):
    """Query upctoasin.com for the UPC, return ASIN, and wait one second (per rate
    limiting instructions)
    """
    url = "http://upctoasin.com/" + upc
    response = requests.get(url)
    sleep(1) # Sleep for one second
    return(response.text)
