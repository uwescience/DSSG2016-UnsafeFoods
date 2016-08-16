

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


