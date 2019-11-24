# NetSuite Database Connector

*Warning*: This project is undergoing active development and is not yet production-grade. Please mail the author if you want to find out more

Connects NetSuite to a database to transfer information to and fro.

## Installation

This project requires [Python 3+](https://www.python.org/downloads/).

1. Download this project and use it (copy it in your project, etc).
2. Install it from [pip](https://pypi.org).

        $ pip install netsuite-db-connector

## Usage

To use this connector you'll need connect to a NetSuite account via Token-based Authentication (TBA).

First, setup TBA credentials using environment variables.

```
# TBA credentials
export NS_ACCOUNT=xxxx
export NS_CONSUMER_KEY=xxxx
export NS_CONSUMER_SECRET=xxxx
export NS_TOKEN_KEY=xxxx
export NS_TOKEN_SECRET=xxxx

```

Here's example usage. 

```python
import os
import sqlite3
from netsuitesdk import NetSuiteConnection
from netsuite_db_connector import NetSuiteExtractConnector, NetSuiteLoadConnector

def ns_connect():
    NS_ACCOUNT = os.getenv('NS_ACCOUNT')
    NS_CONSUMER_KEY = os.getenv('NS_CONSUMER_KEY')
    NS_CONSUMER_SECRET = os.getenv('NS_CONSUMER_SECRET')
    NS_TOKEN_KEY = os.getenv('NS_TOKEN_KEY')
    NS_TOKEN_SECRET = os.getenv('NS_TOKEN_SECRET')
    nc = NetSuiteConnection(account=NS_ACCOUNT, consumer_key=NS_CONSUMER_KEY, consumer_secret=NS_CONSUMER_SECRET,                   token_key=NS_TOKEN_KEY, token_secret=NS_TOKEN_SECRET)
    return nc

ns = ns_connect()

dbconn = sqlite3.connect('/tmp/ns.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
x = NetSuiteExtractConnector(ns=ns, dbconn=dbconn)
x.create_tables()

x.extract_currencies()
x.extract_accounts()
x.extract_departments()
x.extract_locations()
x.extract_vendors()
x.extract_classifications()

y = NetSuiteLoadConnector(ns=ns, dbconn=dbconn)
y.create_tables()

# do some transformations and populated vendor bills related load tables
for vendor_bill_external_id in y.get_vendor_bill_external_ids():
    internal_id = y.load_vendor_bill(vendor_bill_external_id=vendor_bill_external_id)
    print(f'posted vendor_bill_id {vendor_bill_external_id} for which NS returned {internal_id}')
```

## Contribute

To contribute to this project follow the steps

* Fork and clone the repository.
* Run `pip install -r requirements.txt`
* Setup pylint precommit hook
    * Create a file `.git/hooks/pre-commit`
    * Copy and paste the following lines in the file - 
        ```bash
        #!/usr/bin/env bash 
        git-pylint-commit-hook
        ```
* Make necessary changes
* Run unit tests to ensure everything is fine

## Unit Tests

To run unit tests, run pytest in the following manner:

```
python -m pytest test/unit
```

You should see something like this:
```
...
```

## Integration Tests

To run unit tests, you will need to connect to a real NetSuite account. Set the following environment variables before running the integration tests:

```
# TBA credentials
export NS_ACCOUNT=xxxx
export NS_CONSUMER_KEY=xxxx
export NS_CONSUMER_SECRET=xxxx
export NS_TOKEN_KEY=xxxx
export NS_TOKEN_SECRET=xxxx

```

## Code coverage

To get code coverage report, run this command:

```python
python -m pytest --cov=netsuite_db_connector

<snipped output>

```

To get an html report, run this command:

```python
python -m pytest --cov=netsuite_db_connector --cov-report html:cov_html
```

We want to maintain code coverage of more than 95% for this project at all times.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
