try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import certifi
import json


my_api_key = '242a19f63b83510460236f3f5a8cb8c9'
company_symbol = 'AAPL'
# trying to access Company key stats API: https://site.financialmodelingprep.com/developer/docs/companies-key-stats-free-api/#Python
# free account ONLY works with international data
url = f'https://financialmodelingprep.com/api/v3/profile/{company_symbol}?apikey=' + my_api_key
url_company_outlook = f'https://financialmodelingprep.com/api/v3/profile/{company_symbol}?apikey=' + my_api_key
url_symbols_list = "https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey=" + my_api_key


def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


def print_company_symbols_containing_string(target_string):
    filtered_list_containing_string = list(filter(lambda symbol:symbol.find(target_string) != -1 ,get_jsonparsed_data(url_symbols_list)))
    print(filtered_list_containing_string)
    return filtered_list_containing_string

# print_company_symbols_containing_string('ODET')
print(get_jsonparsed_data(url))
