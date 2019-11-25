import logging

from common.utilities import (dbconn_table_num_rows, dbconn_table_row_dict,
                              dict_compare_keys, get_mock_ns_empty)
from netsuite_db_connector.load import NetSuiteLoadConnector

logger = logging.getLogger(__name__)

def test_load_get_vendor_bill_external_ids(nslc):
    dbconn = nslc._NetSuiteLoadConnector__dbconn
    external_ids = nslc.get_vendor_bill_external_ids()
    assert external_ids == ['1237'], 'external_ids are incorrect'

    dbconn.cursor().execute('delete from ns_load_vendor_bills')
    dbconn.commit()
    external_ids = nslc.get_vendor_bill_external_ids()
    assert external_ids == [], 'external_ids are incorrect'

def test_load_vendor_bills(nslc):
    ns = nslc._NetSuiteLoadConnector__ns
    nslc.load_vendor_bill(vendor_bill_external_id='1237')
    ns.vendor_bills.post.assert_called()
    vb_posted = ns.vendor_bills.post.call_args[0][0]
    assert vb_posted['externalId'] == '1237'
    assert vb_posted['location']['internalId'] == '1'

def test_get_vendor_bill_ns_internal_id(nslc):
    assert not nslc.get_vendor_bill_ns_internal_id(vendor_bill_external_id='1237'), 'internal id should not exist'
    nslc.load_vendor_bill(vendor_bill_external_id='1237')
    assert nslc.get_vendor_bill_ns_internal_id(vendor_bill_external_id='1237') == '1345', 'internal id does not match'


