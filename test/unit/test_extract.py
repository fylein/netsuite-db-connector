import logging

from common.utilities import (dbconn_table_num_rows, dbconn_table_row_dict,
                              dict_compare_keys, get_mock_ns_empty)
from netsuite_db_connector import NetSuiteExtractConnector

logger = logging.getLogger(__name__)

def test_accounts(nsec):
    dbconn = nsec._NetSuiteExtractConnector__dbconn
    ns = nsec._NetSuiteExtractConnector__ns
    ids = nsec.extract_accounts()
    ns_data = ns.accounts.get_all()[0]
    db_data = dbconn_table_row_dict(dbconn, 'ns_extract_accounts')
    assert dict_compare_keys(db_data, ns_data) == [], 'db table has some columns that ns doesnt'
    assert dbconn_table_num_rows(dbconn, 'ns_extract_accounts') == len(ns.accounts.get_all()), 'row count mismatch'
    assert len(ids) == 37, 'return value messed up'

def test_empty(dbconn):
    ns = get_mock_ns_empty()
    res = NetSuiteExtractConnector(ns=ns, dbconn=dbconn)
    res.create_tables()
    assert res.extract_accounts() == []
