# py-vsys
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/downloads/) [![License](https://img.shields.io/badge/License-BSD_4--Clause-green.svg)](./LICENSE)

> ***Under active development. Contributions are always welcome!***

The official Python SDK for VSYS APIs. The [old Python SDK](https://github.com/virtualeconomy/pyvsystems) is deprecated and will be archived soon.



- [py-vsys](#py-vsys)
  - [Installation](#installation)
    - [Pip](#pip)
    - [Pipenv](#pipenv)
  - [Quick Example](#quick-example)
  - [Docs](#docs)
    - [Smart Contracts](#smart-contracts)
  - [Run Tests](#run-tests)
    - [Functional Tests](#functional-tests)
  - [Logging](#logging)
  - [Contributing](#contributing)


## Installation

> Will be published to PYPI soon

### Pip
```bash
pip install git+https://github.com/virtualeconomy/py-vsys.git@main
```

`@main` is necessary as the default branch is `develop`

If installing from the `develop` branch is desired, run

```bash
pip install git+https://github.com/virtualeconomy/py-vsys.git
```

### Pipenv

```bash
pipenv install git+https://github.com/virtualeconomy/py-vsys.git@main#egg=py_vsys
```

`@main` is necessary as the default branch is `develop`


If installing from the `develop` branch is desired, run

```bash
pipenv install git+https://github.com/virtualeconomy/py-vsys.git#egg=py_vsys
```

## Quick Example

```python
import asyncio
import py_vsys as pv

# The RESTful API host address to a node in a public test net
HOST = "http://veldidina.vos.systems:9928"
# A test net wallet seed
SEED = ""


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
    wallet: pv.Wallet = pv.Wallet.from_seed_str(SEED)
    acnt: pv.Account = wallet.get_account(chain, nonce=0)
    # Get the account's balance
    print("Balance:", await acnt.bal)
    # Get the account's nonce'
    print("Nonce:", acnt.nonce)
    # Get the account's public key
    print("Public key: ", acnt.key_pair.pub)
    # Get the account's private key
    print("Private key:", acnt.key_pair.pri)
    # Get the account's address
    print("Account address:", acnt.addr)

    print_heading("Try out Smart Contract")
    ctrt_id = "CFB6zvcy39FCRGhxo8HH3PE6zZEG5zXevhG"
    ctrt: pv.NFTCtrt = pv.NFTCtrt(ctrt_id, chain)
    # Get the contract's maker
    print("Maker:", await ctrt.maker)
    # Get the contract's issuer
    print("Issuer:", await ctrt.issuer)
    # Get the contract's ID
    print("Contract id: ", ctrt.ctrt_id)

    await api.sess.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Example output
```
========== Try out NodeAPI ==========
{'height': 1294386}
{'version': 'VSYS Core v0.4.1'}
========== Try out Chain ==========
Height:  1294386
Last blcok:
 {'version': 1, 'timestamp': 1646617122022012339, 'reference': '5iCNrcmHAd7ksnsKbt793DbyeRhheNLuxqzo1CRspYrkPL1oXcqSwb3jdEb5nKra9XFvnqPXHS4R6fsRzEdqDFwx', 'SPOSConsensus': {'mintTime': 1646617122000000000, 'mintBalance': 50097894873482088}, 'resourcePricingData': {'computation': 0, 'storage': 0, 'memory': 0, 'randomIO': 0, 'sequentialIO': 0}, 'TransactionMerkleRoot': 'gSDLiXotSAb8iTqZynm13syWGEg2t22sqxsnExLZwLA', 'transactions': [{'type': 5, 'id': 'FE4gbQwmg8cUPHeEmbiGH4HdjD7d7GN1Y6Xvhv4AQsu4', 'recipient': 'ATxtBDygMvWtvh9xJaGQn5MdaHsbuQxbjiG', 'timestamp': 1646617122022012339, 'amount': 900000000, 'currentBlockHeight': 1294386, 'status': 'Success', 'feeCharged': 0}], 'generator': 'ATxtBDygMvWtvh9xJaGQn5MdaHsbuQxbjiG', 'signature': '4Q9LwLEJgQmUv5iQqWbt1ScDBYyNq1d3KcZUdUvEbUNsH3zJmdvRg4BvAVoBrb82NGLTrX8pPwpWMCseWraGbi5u', 'fee': 0, 'blocksize': 330, 'height': 1294386, 'transaction count': 1}
========== Try out Account ==========
Balance: VSYS(4867193229105012)
Nonce: Nonce(0)
Public key:  PubKey(6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL)
Private key: PriKey(BHpnszuqFHXuwesGbvrozYpevZiMsL29vLvud1zScqEK)
Account address: Addr(AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD)
========== Try out Smart Contract ==========
Maker: Addr(AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD)
Issuer: Addr(AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD)
Contract id:  CtrtID(CFB6zvcy39FCRGhxo8HH3PE6zZEG5zXevhG)
```

## Docs

### Smart Contracts
- [NFT Contract V1](./doc/smart_contract/nft_ctrt.md)
- [NFT Contract V2](./doc/smart_contract/nft_ctrt_v2.md)
- [Token Contract V1 without split](./doc/smart_contract/tok_ctrt_no_split.md)
- [Token Contract V1 with split](./doc/smart_contract/tok_ctrt_split.md)
- [Token Contract V2 without split](./doc/smart_contract/tok_ctrt_no_split_v2.md)
- [Atomic Swap Contract](./doc/smart_contract/atomic_swap_ctrt.md)
- [Payment Channel Contract](./doc/smart_contract/pay_chan_ctrt.md)
- [Lock Contract](./doc/smart_contract/lock_ctrt.md)
- [System Contract](./doc/smart_contract/sys_ctrt.md)


## Run Tests

### Functional Tests
Functional tests are scripts that simulate the behaviour of a normal user to interact wtih `py_vsys`(e.g. register a smart contract & call functions of it).

To run it, ensure that you have `pytest` properly installed(it is a development dependency of `py_vsys` and can be installed via `pipenv install -d`).

> NOTE that the test environment defined as global variables in [conftest.py](./test/func_test/conftest.py) has to be configured through environment vairables before the test cases can be executed.

Then go to the root of the of the project and run.

```bash
python -m pytest -v test/func_test
```

The above command will test each aspect(e.g. function `send` of NFT contract) individually and have required resources set up before testing(e.g. register a new contract, issue a token, etc). It's good for testing a specific aspect while it might consume too much resources to test every aspect in this way.

To test as a whole, use the `whole` marker like below.

```bash
python -m pytest -v test/func_test -m whole
```
Take NFT contract for an example, it will register a contract first and then execute functions like `send`, `transfer`, `deposit`, etc in a pre-orchestrated manner so that some common set up(e.g. register a contract) will be done only once.

To run a single test, say method `test_pay` of class `TestAccount`, run

```bash
python -m pytest -v test/func_test/test_acnt.py::TestAccount::test_pay
```


## Logging
Logging for `py-vsys` is supported by [loguru](https://github.com/Delgan/loguru) and is disabled by default.
To enable it, add the following to your codes.

```python
from loguru import logger
logger.enable("py_vsys")
```


## Contributing

**Contributions are always welcome!**

See [the development documentation](./doc/dev.md) for more details and please adhere to conventions mentioned in it.

