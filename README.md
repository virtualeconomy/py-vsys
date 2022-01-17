# py-v-sdk
[![Python version](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)

> ***Under active development. Contributions are always welcome!***

The official Python SDK for VSYS APIs. The [old Python SDK](https://github.com/virtualeconomy/pyvsystems) is deprecated and will be archived soon.



- [py-v-sdk](#py-v-sdk)
  - [Installation](#installation)
  - [Quick Example](#quick-example)
  - [Logging](#logging)
  - [Usage](#usage)
    - [Smart Contracts](#smart-contracts)
  - [Contributing](#contributing)


## Installation

> Will be published to PYPI soon

```bash
pip install git+https://github.com/virtualeconomy/py-v-sdk.git@main
```

`@mian` is necessary as the default branch is `develop`

If you are using `pipenv`, try

```bash
pipenv install git+https://github.com/virtualeconomy/py-v-sdk.git@main#egg=py_v_sdk
```


## Quick Example

```python
import py_v_sdk as pv

# The RESTful API host to a public test net
NODE_HOST = "http://veldidina.vos.systems:9928"
# A test net wallet
WALLET_SEED = "amount palm soldier device cereal fashion fringe copper huge mansion animal banana ready garment setup"

# NodeAPI is the wrapper for RESTful APIs
api: pv.NodeAPI = pv.NodeAPI(NODE_HOST)

# Chain represents the chain itself
chain: pv.Chain = pv.Chain(api)

# Account represents an account in the net
acnt: pv.Account = pv.Account(chain, WALLET_SEED)

ctrt_id = "CFB6zvcy39FCRGhxo8HH3PE6zZEG5zXevhG"
ctrt: pv.NFTCtrt = pv.NFTCtrt(ctrt_id, chain)


def try_api():
    # GET /blocks/last
    print(api.blocks.get_last_block())
    # GET /node/version
    print(api.node.get_version())


def try_chain():
    # Get chain's height
    print(chain.height)
    # Get chain's last block
    print(chain.last_block)


def try_acnt():
    # Get the account's balance
    print(acnt.balance)
    # Get the account's seed
    print(acnt.seed)
    # Get the account's nonce'
    print(acnt.nonce)
    # Get the account's public key
    print(acnt.key_pair.pub_b58_str)
    # Get the account's private key
    print(acnt.key_pair.pri_b58_str)
    # Get the account's address
    print(acnt.addr_b58_str)


def try_ctrt():
  print(ctrt.maker)
  print(ctrt.issuer)
  print(ctrt.ctrt_id)


try_api()
try_chain()
try_acnt()
try_ctrt()
```


## Logging
Logging for `py-v-sdk` is supported by [loguru](https://github.com/Delgan/loguru) and is disabled by default.
To enable it, add the following to your codes.

```python
from loguru import logger
logger.enable("py_v_sdk")
```

## Usage

> The complete documentation is on the way

### Smart Contracts
- [NFT Contract](./doc/smart_contract/NFT_contract.md)


## Contributing

**Contributions are always welcome!**

See [the development documentation](./doc/dev.md) for more details and please adhere to conventions mentioned in it.

