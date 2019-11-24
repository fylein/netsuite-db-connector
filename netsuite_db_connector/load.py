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

    # TODO: add load functions