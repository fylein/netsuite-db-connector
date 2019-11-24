"""
NetSuiteLoadConnector(): Connection between NetSuite and Database
"""

import logging
from os import path
from typing import Generator

import sqlite3

class NetSuiteLoadConnector:
    """
    - Extract Data from Database and load to NetSuite
    """
    def __init__(self, ns, dbconn):
        self.__ns = ns
        self.__dbconn = dbconn
        self.__dbconn.row_factory = sqlite3.Row
        self.logger = logging.getLogger(self.__class__.__name__)

    def create_tables(self):
        """
        Creates DB tables
        """
        basepath = path.dirname(__file__)
        ddlpath = path.join(basepath, 'load_ddl.sql')
        ddlsql = open(ddlpath, 'r').read()
        self.__dbconn.executescript(ddlsql)

    def get_vendor_bill_external_ids(self):
        """
        Returns list of vendor bill ids
        """
        rows = self.__dbconn.cursor().execute('select "externalId" from ns_load_vendor_bills').fetchall()
        if not rows:
            return []
        return [row['externalId'] for row in rows]

    def get_vendor_bill_ns_internal_id(self, vendor_bill_external_id):
        row = self.__dbconn.cursor().execute('select "internalId" from ns_load_vendor_bills where "externalId" = ?', (vendor_bill_external_id,)).fetchone()
        if not row:
            return None
        return row['internalId']

    @staticmethod
    def _replace_with_nested(data, key, type_name):
        """
        Convenience method that takes a structure like:
        data = {
            ${key}InternalId: ${value}
        }
        and changes data to:
        data = {
            ${key}: {
                'internalId': ${value},
                'type': ${type_name}
            }
        }
        """
        k = f'{key}InternalId'
        if k not in data:
            return
        if data[k]:
            data[key] = {
                'internalId': data[k],
                'type': type_name
            }
        del data[k]

    def load_vendor_bill(self, vendor_bill_external_id):
        row = self.__dbconn.cursor().execute('select * from ns_load_vendor_bills where "externalId" = ?', (vendor_bill_external_id, )).fetchone()
        vendor_bill = dict(row)
        NetSuiteLoadConnector._replace_with_nested(data=vendor_bill, key='currency', type_name='currency')
        NetSuiteLoadConnector._replace_with_nested(data=vendor_bill, key='entity', type_name='vendor')
        NetSuiteLoadConnector._replace_with_nested(data=vendor_bill, key='class', type_name='classification')
        NetSuiteLoadConnector._replace_with_nested(data=vendor_bill, key='location', type_name='location')

        expenses = []
        for row in self.__dbconn.cursor().execute('select * from ns_load_vendor_bills_expenses where "vendorBillExternalId" = ?', (vendor_bill_external_id,)):
            exp = dict(row)
            del exp['vendorBillExternalId']
            NetSuiteLoadConnector._replace_with_nested(data=exp, key='account', type_name='account')
            NetSuiteLoadConnector._replace_with_nested(data=exp, key='class', type_name='classification')
            NetSuiteLoadConnector._replace_with_nested(data=exp, key='location', type_name='location')
            NetSuiteLoadConnector._replace_with_nested(data=exp, key='department', type_name='department')
            expenses.append(exp)

        vendor_bill['expenseList'] = expenses
        self.logger.info('vb = %s', vendor_bill)
        res = self.__ns.vendor_bills.post(vendor_bill)
        self.logger.info('res = %s', res)
        assert res['externalId'] == vendor_bill['externalId'], 'External ID does not match'
        internal_id = res['internalId']

        self.__dbconn.cursor().execute('update ns_load_vendor_bills set "internalId" = ? where "externalId" = ?', (internal_id, vendor_bill_external_id,))
        self.__dbconn.commit()
        return internal_id
