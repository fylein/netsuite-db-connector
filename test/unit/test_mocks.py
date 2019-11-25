import pytest

import sqlite3
import logging
from os import path
import json
from unittest.mock import Mock
from common.utilities import dict_compare_keys, dbconn_table_num_rows

logger = logging.getLogger(__name__)

def test_ns_mock_setup(ns):
    assert ns.accounts.get_all()[0]['acctNumber'] == '6010', 'ns mock setup is broken'

def test_dbconn_mock_setup(dbconn):
    with pytest.raises(sqlite3.OperationalError) as e:
        rows = dbconn_table_num_rows(dbconn, 'ns_extract_accounts')

def test_nsec_mock_setup(nsec):
    # python magic to access private variable for testing db state
    dbconn = nsec._NetSuiteExtractConnector__dbconn
    assert dbconn_table_num_rows(dbconn, 'ns_extract_accounts') == 0, 'Unclean db'

def test_dict_compare():
    d1 = {
        'k1' : 'xxx', 'k2' : 2, 'k3' : [1, 2], 'k4' : { 'k41' : [2], 'k42' : { 'k421' : 20}}
    }
    d2 = {
        'k1' : 'xyx', 'k3' : [1, 2], 'k4' : { 'k42' : { 'k421' : 20}}
    }
    d3 = {
        'k1' : 'xyz', 'k3' : [3, 2], 'k4' : { 'k42' : { 'k421' : 40}}
    }
    assert dict_compare_keys(d1, d2) == ['->k2', '->k4->k41'], 'not identifying diff properly'
    assert dict_compare_keys(d2, d3) == [], 'should return no diff'

def test_nslc_mock_setup(nslc):
    dbconn = nslc._NetSuiteLoadConnector__dbconn
    assert dbconn_table_num_rows(dbconn, 'ns_load_vendor_bills') == 1, 'Unclean db'
    assert dbconn_table_num_rows(dbconn, 'ns_load_vendor_bill_expenses') == 2, 'Unclean db'
