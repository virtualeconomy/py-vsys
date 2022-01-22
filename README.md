# py-v-sdk
[![Python version](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/downloads/)

[![License](https://img.shields.io/badge/License-BSD_4--Clause-green.svg)](./LICENSE)

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
import asyncio

import py_v_sdk as pv

# The RESTful API host address to a node in a public test net
HOST = "http://veldidina.vos.systems:9928"
# A test net wallet seed
SEED = "amount palm soldier device cereal fashion fringe copper huge mansion animal banana ready garment setup"


def print_heading(msg: str) -> None:
    print("=" * 10, f"{msg}", "=" * 10)


async def main():
    print_heading("Try out NodeAPI")
    # NodeAPI is the wrapper for RESTful APIs
    api: pv.NodeAPI = await pv.NodeAPI.new(HOST)
    # GET /blocks/last
    print(await api.blocks.get_height())
    # GET /node/version
    print(await api.node.get_version())

    print_heading("Try out Chain")
    # Chain represents the chain itself
    chain: pv.Chain = pv.Chain(api)
    # Get chain's height
    print("Height: ", await chain.height)
    # Get chain's last block
    print("Last blcok:\n", await chain.last_block)

    print_heading("Try out Account")
    # Account represents an account in the net
    acnt: pv.Account = pv.Account(chain, SEED, nonce=0)
    # Get the account's balance
    print("Balance:", await acnt.balance)
    # Get the account's seed
    print("Seed:", acnt.seed)
    # Get the account's nonce'
    print("Nonce:", acnt.nonce)
    # Get the account's public key
    print("Public key: ", acnt.key_pair.pub.b58_str)
    # Get the account's private key
    print("Private key:", acnt.key_pair.pri.b58_str)
    # Get the account's address
    print("Account address:", acnt.addr.b58_str)

    print_heading("Try out Smart Contract")
    ctrt_id = "CFB6zvcy39FCRGhxo8HH3PE6zZEG5zXevhG"
    ctrt: pv.NFTCtrt = pv.NFTCtrt(ctrt_id, chain)
    # Get the contract's maker
    print("Maker:", await ctrt.maker)
    # Get the contract's issuer
    print("Issuer:", await ctrt.issuer)
    # Get the contract's ID
    print("Contract id: ", ctrt.ctrt_id)


if __name__ == "__main__":
    asyncio.run(main())

```

Example output
```
========== Try out NodeAPI ==========
{'height': 668531}
{'version': 'VSYS Core v0.4.1'}
========== Try out Chain ==========
Height:  668531
Last blcok:
 {'version': 1, 'timestamp': 1642861992010691002, 'reference': '39hQCUgB2zQe7NqFsYqWfY6gTv9Zf7z7vCavjaqRZi4B6qKbfxNSVeaxFndjq5y1cuRJ4FoVHkb2AytYDMeG2iaS', 'SPOSConsensus': {'mintTime': 1642861992000000000, 'mintBalance': 50030598629237850}, 'resourcePricingData': {'computation': 0, 'storage': 0, 'memory': 0, 'randomIO': 0, 'sequentialIO': 0}, 'TransactionMerkleRoot': 'FBELMGpFbVcAJse2kLXoDh7CJHcw6ZYHKLRvvfzeKijw', 'transactions': [{'type': 5, 'id': 'B6r1AuPXBvTiMLRHPe4fcMthsd6Sq35n71ZvXnqgAKoS', 'recipient': 'AU6sMeLdsswqDQrw4RDo5PVxdGh1v6JDv6t', 'timestamp': 1642861992010691002, 'amount': 900000000, 'currentBlockHeight': 668531, 'status': 'Success', 'feeCharged': 0}], 'generator': 'AU6sMeLdsswqDQrw4RDo5PVxdGh1v6JDv6t', 'signature': '2kBVPPYpkFzSZSAu1fVv85U2xBKUYqMBibtstknJYAXSaDUA6WDz31AqYrkL4Uv3SQuGxDTDSRZjqY2sADGD4r7w', 'fee': 0, 'blocksize': 330, 'height': 668531, 'transaction count': 1}
========== Try out Account ==========
Balance: 0
Seed: amount palm soldier device cereal fashion fringe copper huge mansion animal banana ready garment setup
Nonce: 0
Public key:  JyDuPhvWGQDV5SQfTQCo8yaenuY4dLF3YeZwhkhzCgz8L2xxrPevvgyzS5ze
Private key: PDUZn2xzfn8GKgKjYviTcLM24ThLffBSB8EYeba8tA7ixTuChJLmaAD4yGTw
Account address: ATrcMo5NnFECc6sN2Ca8evBr26bYJgwFnvK
========== Try out Smart Contract ==========
Maker: AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD
Issuer: AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD
Contract id:  CFB6zvcy39FCRGhxo8HH3PE6zZEG5zXevhG
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

