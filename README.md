# Prosper API client for Python

Python trading library for Prosper.com

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/grahamtt/prosper-api/build-and-release.yml?logo=github)
![PyPI - Version](https://img.shields.io/pypi/v/prosper-api?label=prosper-api)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/prosper-api)
![PyPI - License](https://img.shields.io/pypi/l/prosper-api)
![Code Climate coverage](https://img.shields.io/codeclimate/coverage/grahamtt/prosper-api?logo=codeclimate)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability-percentage/grahamtt/prosper-api?logo=codeclimate)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/m/grahamtt/prosper-api?logo=github)
![GitHub issues](https://img.shields.io/github/issues-raw/grahamtt/prosper-api?logo=github)


## Installation

### With Pip
```commandline
pip install prosper-api
```

#### Optional `keyring` support
```commandline
pip install 'prosper-api[secure]'
```

### With Poetry
```commandline
poetry add prosper-api
```

#### Optional `keyring` support
```commandline
poetry add 'prosper-api[secure]'
```



## Setup
> ℹ️ The library currently only supports personal use, where the client id and credentials are from the same account. Support
for multi-account mode is [planned](https://github.com/grahamtt/prosper-api/issues/3).

### Default

Create a file at `$HOME/.prosper-api/config.toml` with the following contents:

```toml
[credentials]
client-id = "0123456789abcdef0123456789abcdef"
client-secret = "fedcba9876543210fedcba9876543210"
username = "PROBABLY_YOUR_EMAIL_ADDRESS"
password = "AWESOME_PASSWORD"
```

### More secure

> ℹ️ You must have installed `keyring` or used the '[secure]' mode when installing the library.

Remove the `client-secret` and `password` portions of the config:

```toml
[credentials]
client-id = "0123456789abcdef0123456789abcdef"
username = "PROBABLY_YOUR_EMAIL_ADDRESS"
```

Run the following to store your credentials securely in your OS credentials storage, e.g. Keychain for MacOS, etc.
For each command, you will be prompted to enter the corresponding secret. For 'CLIENT_ID', enter the client secret. For
'USERNAME' enter the corresponding password.

```commandline
keyring set prosper-api {CLIENT_ID}
keyring set prosper-api {USERNAME}
```

## Use

See [a sample bot](https://github.com/grahamtt/prosper-auto-invest) for concrete usage.

### Get account details
The following will get the details of your account, including available cash and investment allocations.

```python
from prosper_api.client import Client, Account

client = Client()
account: Account = client.get_account_info()
```

### Search listings
The following will get all the current listings you haven't invested in.

```python
from prosper_api.client import Client, Listing, SearchListingsRequest, SearchListingsResponse
from typing import List

PAGE_SIZE=25
client = Client()
listings: List[Listing] = []
offset = 0
while True:
    result: SearchListingsResponse = client.search_listings(SearchListingsRequest(invested=False, biddable=True, limit=PAGE_SIZE, offset=offset))
    listings += result.result
    offset += PAGE_SIZE
    if len(listings) >= result.total_count or len(result.result) < PAGE_SIZE:
        break
```

> ℹ️ The full set of filters listed in the [Prosper API docs](https://developers.prosper.com/docs/investor/listings-api/)
>  are available

### Place order
The following will place an order, given a listing id.

```python
from prosper_api.client import Client, Order

client = Client()
listing_id: int = 12341234
order_dollar_amount: float = 25
order_result: Order = client.order(listing_id, order_dollar_amount)
```

### List notes
The following will list all the notes in your account. The same pattern can be used to list orders, loans, and payments.

```python
from prosper_api.client import Client, Note, ListNotesRequest, ListNotesResponse
from typing import List

client = Client()
notes: List[Note] = []
PAGE_SIZE = 25
offset = 0
while True:
    result: ListNotesResponse = client.list_notes(ListNotesRequest(limit=PAGE_SIZE, offset=offset, sort_by="age_in_months", sort_dir="asc"))
    notes += result.result
    offset += PAGE_SIZE
    if len(notes) >= result.total_count or len(result.result) < PAGE_SIZE:
        break
```