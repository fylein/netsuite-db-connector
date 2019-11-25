import json
import logging
import os
import sqlite3
from os import path
from unittest.mock import Mock

import pytest

from common.utilities import get_mock_ns
from netsuite_db_connector.extract import NetSuiteExtractConnector
from netsuite_db_connector.load import NetSuiteLoadConnector

logger = logging.getLogger(__name__)

@pytest.fixture
def ns():
    return get_mock_ns()

@pytest.fixture
def dbconn():
    SQLITE_DB_FILE = '/tmp/test_ns.db'
    if os.path.exists(SQLITE_DB_FILE):
        os.remove(SQLITE_DB_FILE)
    conn = sqlite3.connect(SQLITE_DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    return conn

@pytest.fixture
def nsec(ns, dbconn):
    res = NetSuiteExtractConnector(ns=ns, dbconn=dbconn)
    res.create_tables()
    return res

@pytest.fixture
def nslc(ns, dbconn):
    res = NetSuiteLoadConnector(ns=ns, dbconn=dbconn)
    res.create_tables()
    basepath = path.dirname(__file__)
    sqlpath = path.join(basepath, '../common/mock_db_load.sql')
    sql = open(sqlpath, 'r').read()
    dbconn.executescript(sql)
    return res
