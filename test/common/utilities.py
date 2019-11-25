import copy
import json
import logging
import os
from os import path
from unittest.mock import Mock
import sqlite3
from netsuitesdk import NetSuiteConnection
from netsuite_db_connector import NetSuiteExtractConnector, NetSuiteLoadConnector

logger = logging.getLogger(__name__)

def get_mock_ns_dict(filename):
    basepath = path.dirname(__file__)
    filepath = path.join(basepath, filename)
    mock_ns_json = open(filepath, 'r').read()
    mock_ns_dict = json.loads(mock_ns_json)
    return mock_ns_dict

def get_mock_ns_from_file(filename):
    mock_ns_dict = get_mock_ns_dict(filename)
    mock_ns = Mock()
    mock_ns.accounts.get_all.return_value = mock_ns_dict['accounts']
    mock_ns.accounts.get_all_generator.return_value = iter(mock_ns_dict['accounts'])
    mock_ns.classifications.get_all.return_value = mock_ns_dict['classifications']
    mock_ns.departments.get_all.return_value = mock_ns_dict['departments']
    mock_ns.locations.get_all.return_value = mock_ns_dict['locations']
    mock_ns.currencies.get_all.return_value = mock_ns_dict['currencies']
    mock_ns.vendors.get_all.return_value = mock_ns_dict['vendors']
    mock_ns.vendor_bills.get_all.return_value = mock_ns_dict['vendor_bills']

    # TODO: need to fix return_value
#    mock_ns.vendor_bills.post.return_value = copy.deepcopy(mock_ns_dict['vendor_bills'][0])
    return mock_ns

def get_mock_ns():
    return get_mock_ns_from_file('mock_ns.json')

def get_mock_ns_empty():
    return get_mock_ns_from_file('mock_ns_empty.json')

def dict_compare_keys(d1, d2, key_path=''):
    ''' Compare two dicts recursively and see if dict1 has any keys that dict2 does not
    Returns: list of key paths
    '''
    res = []
    if not d1:
        return res
    if not isinstance(d1, dict):
        return res
    for k in d1:
        if k not in d2:
            missing_key_path = f'{key_path}->{k}'
            res.append(missing_key_path)
        else:
            if isinstance(d1[k], dict):
                key_path1 = f'{key_path}->{k}'
                res1 = dict_compare_keys(d1[k], d2[k], key_path1)
                res = res + res1
            elif isinstance(d1[k], list):
                key_path1 = f'{key_path}->{k}[0]'
                dv1 = d1[k][0] if len(d1[k]) > 0 else None
                dv2 = d2[k][0] if len(d2[k]) > 0 else None
                res1 = dict_compare_keys(dv1, dv2, key_path1)
                res = res + res1
    return res

def dbconn_table_num_rows(dbconn, tablename):
    ''' Helper function to calculate number of rows
    '''
    query = f'select count(*) from {tablename}'
    return dbconn.cursor().execute(query).fetchone()[0]

def dbconn_table_row_dict(dbconn, tablename):
    query = f'select * from {tablename} limit 1'
    row = dbconn.cursor().execute(query).fetchone()
    return dict(row)

def ns_connect():
    NS_ACCOUNT = os.getenv('NS_ACCOUNT')
    NS_CONSUMER_KEY = os.getenv('NS_CONSUMER_KEY')
    NS_CONSUMER_SECRET = os.getenv('NS_CONSUMER_SECRET')
    NS_TOKEN_KEY = os.getenv('NS_TOKEN_KEY')
    NS_TOKEN_SECRET = os.getenv('NS_TOKEN_SECRET')
    nc = NetSuiteConnection(account=NS_ACCOUNT, consumer_key=NS_CONSUMER_KEY, consumer_secret=NS_CONSUMER_SECRET,
            token_key=NS_TOKEN_KEY, token_secret=NS_TOKEN_SECRET)
    return nc
