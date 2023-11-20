# Prosper API client for Python

Python trading library for Prosper.com

[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/grahamtt/prosper-api/build-and-release.yml?logo=github)](https://github.com/grahamtt/prosper-api)
[![PyPI - Version](https://img.shields.io/pypi/v/prosper-api?label=prosper-api)](https://pypi.org/project/prosper-api/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/prosper-api)
![PyPI - License](https://img.shields.io/pypi/l/prosper-api)
[![Code Climate coverage](https://img.shields.io/codeclimate/coverage/grahamtt/prosper-api?logo=codeclimate)](https://codeclimate.com/github/grahamtt/prosper-api)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability-percentage/grahamtt/prosper-api?logo=codeclimate)](https://codeclimate.com/github/grahamtt/prosper-api)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/8063/badge)](https://www.bestpractices.dev/projects/8063)
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
> for multi-account mode is [planned](https://github.com/grahamtt/prosper-api/issues/3).

### Config file location

- Linux/Unix: `$HOME/.config/prosper-api/config.toml`
- Windows: `%HOMEDIR%%HOMEPATH\AppData\Local\prosper-api\prosper-api\config.toml`
- MacOs: `$HOME/Library/Application Support/prosper-api/config.toml`

### Default

Create a config file with the following contents:

```toml
[credentials]
client-id = "0123456789abcdef0123456789abcdef"
client-secret = "fedcba9876543210fedcba9876543210"
username = "PROBABLY_YOUR_EMAIL_ADDRESS"
password = "AWESOME_PASSWORD"
```

### More secure

> ℹ️ You must have installed `keyring` or used the '\[secure\]' mode when installing the library.

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
keyring set prosper-api '{CLIENT_ID}'
keyring set prosper-api '{USERNAME}'
```

## Use

See [a sample bot](https://github.com/grahamtt/prosper-auto-invest) for concrete usage.

### Get account details

The following will get the details of your account, including available cash and investment allocations.

```python
from prosper_api.client import Client
from prosper_api.models import Account

client = Client()
account: Account = client.get_account_info()
```

### Search listings

The following will get all the current listings you haven't invested in.

```python
from prosper_api.client import Client
from prosper_api.models import Listing, SearchListingsRequest, SearchListingsResponse
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
> are available

### Place order

The following will place an order, given a listing id.

```python
from prosper_api.client import Client
from prosper_api.models import Order

client = Client()
listing_id: int = 12341234
order_dollar_amount: float = 25
order_result: Order = client.order(listing_id, order_dollar_amount)
```

### List notes

The following will list all the notes in your account. The same pattern can be used to list orders, loans, and payments.

```python
from prosper_api.client import Client
from prosper_api.models import Note, ListNotesRequest, ListNotesResponse
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

## Configuration

The following is a full list of the available configuration values:

- `auth.token-cache` (str): The path where the auth token cache should be stored. Defaults to `os.path.join(platformdirs.user_cache_dir("prosper-api"), "token-cache")`
- `client.return-floats` (bool): Indicates whether float values should be returned instead of Decimals (not recommended). Defaults to `False`.
- `client.return-strings-not-dates` (bool): Indicates whether string values should be returned instead of `date` and `datetime` objests. Defaults to `False`.
- `client.return-strings-not-enums` (bool): Indicates whether string values should be returned instead of the corresponding enum values. Defaults to `False`.
- `credentials.client-id` (str): The Prosper client id to use for authentication.
- `credentials.client-secret` (str): The Prosper client secret corresponding to the client id.
- `credentials.username` (str): The Prosper username to use for authentication.
- `credentials.password` (str): The password corresponding to the username.

## Feedback

This project uses [GitHub issues](https://github.com/grahamtt/prosper-api/issues) for feature requests and bug reports.

## Contributing

This project uses [Poetry](https://python-poetry.org/docs/) to manage dependencies and building. Follow the instructions
to install it. Then use `poetry install --all-extras` to install the project dependencies. Then run `poetry run autohooks activate`
to set up the pre-commit hooks. Please ensure the hooks pass before submitting a pull request.
