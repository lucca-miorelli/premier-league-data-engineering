################################################################################
##                                  LIBRARIES                                 ##
################################################################################

################
##  EXTERNAL  ##
################

import requests
from typing import List, Dict, Any


################################################################################
##                                  FUNCTIONS                                 ##
################################################################################

def get_events(url:str=None, params:dict=None) -> List[Dict[str, Any]]:
    """
    Get a list of events from the Football API.

    Parameters
    ----------
    url : str
        The base URL of the API.
    params : dict
        The parameters to be passed to the API.

    Returns
    -------
    List[Dict[str, Any]]
        A list of events.

    Raises
    ------
    ValueError
        If the url parameter is None.
    ValueError
        If the response status code is not 200.
    """

    if url is None:
        raise ValueError("The url parameter cannot be None.")

    # Make the request
    response = requests.get(url=url, params=params)

    if response.status_code != 200:
        raise ValueError(f"The response status code was {response.status_code}.")
    else:
        # Get the list of match dictionaries from the response
        matches_list = response.json()
        return matches_list
