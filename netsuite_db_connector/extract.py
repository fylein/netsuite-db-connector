"""
NetSuiteExtractConnector(): Connection between NetSuite and Database
"""

import logging
import sqlite3
import time
from os import path
from typing import List
import copy

class NetSuiteExtractConnector:
    """
    - Extract Data from NetSuite and load to Database
    """
    def __init__(self, ns, dbconn):
        self.__dbconn = dbconn
        self.__ns = ns
        self.__dbconn.row_factory = sqlite3.Row
        self.logger = logging.getLogger(self.__class__.__name__)

    def create_tables(self):
        """
        Creates DB tables
        """
        basepath = path.dirname(__file__)
        ddlpath = path.join(basepath, 'extract_ddl.sql')
        ddlsql = open(ddlpath, 'r').read()
        self.__dbconn.executescript(ddlsql)

    def _get_col_names(self, table_name):
        """Get column names of a table, given its name and a cursor
        (or connection) to the database.
        """
        cursor = self.__dbconn.cursor()
        reader = cursor.execute(f'SELECT * FROM {table_name}')
        res = [x[0] for x in reader.description] 
        cursor.close()
        return res

    def _generate_insert_statement(self, table_name):
        column_names = self._get_col_names(table_name=table_name)
        columns = ', '.join(column_names)
        placeholders = ':'+', :'.join(column_names)
        query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        return query

    def extract_currencies(self):
        stmt = self._generate_insert_statement(table_name='ns_extract_currencies')
        # self.logger.info('statement: %s', stmt)
        cur = self.__dbconn.cursor()
        gen = self.__ns.currencies.get_all_generator()
        for c in gen:
            cur.execute(stmt, c)
        cur.close()
        self.__dbconn.commit()

    def extract_accounts(self):
        stmt = self._generate_insert_statement(table_name='ns_extract_accounts')
        # self.logger.info('statement: %s', stmt)
        cur = self.__dbconn.cursor()
        gen = self.__ns.accounts.get_all_generator()
        for c in gen:
            cur.execute(stmt, c)
        cur.close()
        self.__dbconn.commit()

    def extract_departments(self):
        stmt = self._generate_insert_statement(table_name='ns_extract_departments')
        # self.logger.info('statement: %s', stmt)
        cur = self.__dbconn.cursor()
        gen = self.__ns.departments.get_all_generator()
        for c in gen:
            cur.execute(stmt, c)
        cur.close()
        self.__dbconn.commit()

    def extract_locations(self):
        stmt = self._generate_insert_statement(table_name='ns_extract_locations')
        # self.logger.info('statement: %s', stmt)
        cur = self.__dbconn.cursor()
        gen = self.__ns.locations.get_all_generator()
        for c in gen:
            cur.execute(stmt, c)
        cur.close()
        self.__dbconn.commit()

    def extract_vendors(self):
        stmt = self._generate_insert_statement(table_name='ns_extract_vendors')
        # self.logger.info('statement: %s', stmt)
        cur = self.__dbconn.cursor()
        gen = self.__ns.vendors.get_all_generator()
        for c in gen:
            cur.execute(stmt, c)
        cur.close()
        self.__dbconn.commit()

    def extract_classifications(self):
        stmt = self._generate_insert_statement(table_name='ns_extract_classifications')
        # self.logger.info('statement: %s', stmt)
        cur = self.__dbconn.cursor()
        gen = self.__ns.classifications.get_all_generator()
        for c in gen:
            cur.execute(stmt, c)
        cur.close()
        self.__dbconn.commit()

