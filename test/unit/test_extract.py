import logging

import pytest
from common.utilities import (dbconn_table_num_rows, dbconn_table_row_dict,
                              dict_compare_keys, get_mock_ns_empty)
from netsuite_db_connector import NetSuiteExtractConnector

logger = logging.getLogger(__name__)

@pytest.mark.parametrize('type_name', ['accounts', 'currencies', 'locations', 'classifications', 'departments', 'vendors'])
def test_extract_by_type_name(nsec, type_name):
    dbconn = nsec._NetSuiteExtractConnector__dbconn
    ns = nsec._NetSuiteExtractConnector__ns
    nsec_extract_fn = getattr(nsec, f'extract_{type_name}')
    ids = nsec_extract_fn()
    ns_get_all_fn = getattr(getattr(ns, f'{type_name}'), 'get_all')
    ns_data = ns_get_all_fn()
    db_data = dbconn_table_row_dict(dbconn, f'ns_extract_{type_name}')
    assert dict_compare_keys(db_data, ns_data[0]) == [], 'db table has some columns that ns doesnt'
    assert dbconn_table_num_rows(dbconn, f'ns_extract_{type_name}') == len(ns_data), 'row count mismatch'


def test_empty(dbconn):
    ns = get_mock_ns_empty()
    res = NetSuiteExtractConnector(ns=ns, dbconn=dbconn)
    res.create_tables()
    assert res.extract_accounts() == []
    assert res.extract_vendors() == []
