"""
NetSuiteExtractConnector(): Connection between NetSuite and Database
"""

import logging
import sqlite3
import time
from os import path
from typing import List
import copy

import pandas as pd

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

    # TODO: add extract functions
