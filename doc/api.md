# Api

- [Api](#api)
  - [Introduction](#introduction)
  - [Usage with Python SDK](#usage-with-python-sdk)
    - [Instantiation](#instantiation)
    - [Properties](#properties)
      - [Session](#session)
      - [API Group: Blocks](#api-group-blocks)
      - [API Group: Utils](#api-group-utils)
      - [API Group: Node](#api-group-node)
      - [API Group: Transactions](#api-group-transactions)
      - [API Group: Contract](#api-group-contract)
      - [API Group: Addresses](#api-group-addresses)
      - [API Group: Database](#api-group-database)
      - [API Group: Leasing](#api-group-leasing)
      - [API Group: VSYS](#api-group-vsys)
    - [Actions](#actions)
      - [Make HTTP GET Request](#make-http-get-request)
      - [Make HTTP POST Request](#make-http-post-request)

## Introduction
Nodes in VSYS net can expose RESTful APIs for users to interact with the chain(e.g. query states, broadcast transactions).

## Usage with Python SDK
In Python SDK we have
-  `NodeAPI` class that serves as an API wrapper for calling node APIs.
- `APIGrp` class that represents a group of APIs that share the same prefix.

### Instantiation
Create an object of `NodeAPI`

```python
import py_vsys as pv

HOST = "http://veldidina.vos.systems:9928"
api = await pv.NodeAPI.new(HOST)
print(api)
```
Example output

```
<py_vsys.api.NodeAPI object at 0x1045e75e0>
```

### Properties

#### Session
The `aiohttp.ClientSession` object that records the HTTP session(e.g. host).

```python
import py_vsys as pv

# api: pv.NodeAPI
print(api.sess)
```
Example output

```
<aiohttp.client.ClientSession object at 0x103c5f520>
```

#### API Group: Blocks
The group of APIs that share the prefix `/blocks`

```python
import py_vsys as pv

# api: pv.NodeAPI
print(api.blocks)

# /blocks/height
resp = await api.blocks.get_height()
print(resp)
```
Example output

```
<py_vsys.api.Blocks object at 0x105b437c0>
{'height': 1356227}
```

#### API Group: Utils
The group of APIs that share the prefix `/utils`

```python
import py_vsys as pv

# api: pv.NodeAPI
print(api.utils)

# /utils/hash/fast
resp = await api.utils.hash_fast("foo")
print(resp)
```
Example output

```
<py_vsys.api.Utils object at 0x101b1fa00>
{'message': 'foo', 'hash': 'DT9CxyH887V4WJoNq9KxcpnF68622oK3BNJ41C2TvESx'}
```

#### API Group: Node
The group of APIs that share the prefix `/node`

```python
import py_vsys as pv

# api: pv.NodeAPI
print(api.node)

# /node/status
resp = await api.node.get_status()
print(resp)
```
Example output

```
<py_vsys.api.Node object at 0x10666f9a0>
{'blockchainHeight': 1356274, 'stateHeight': 1356274, 'updatedTimestamp': 1646988450024425058, 'updatedDate': '2022-03-11T08:47:30.024Z'}
```

#### API Group: Transactions
The group of APIs that share the prefix `/transactions`

```python
import py_vsys as pv

# api: pv.NodeAPI
print(api.tx)

tx_id = "Eui1yaRcE4jCnf4yBawroxSvqGa54WyQV9LjHkRHVvPd"
# /transactions/info/{tx_id}
resp = await api.tx.get_info(tx_id)
print(resp)
```
Example output

```
<py_vsys.api.Transactions object at 0x101bf3940>
{'type': 4, 'id': 'Eui1yaRcE4jCnf4yBawroxSvqGa54WyQV9LjHkRHVvPd', 'fee': 10000000, 'feeScale': 100, 'timestamp': 1646974337469929984, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '3MHpURmQHBAedZ6qww5372B4gYZrVUUD7jgjChn7mecqQECxmaU1f1KURY5eK4UebaSpHQMpFbURth6EP3vL4LPL'}], 'leaseId': '3gjreLTVhHZfqLYVNwFEmUgKYJr3T6iSifi3BoMTqwyw', 'status': 'Success', 'feeCharged': 10000000, 'lease': {'type': 3, 'id': '3gjreLTVhHZfqLYVNwFEmUgKYJr3T6iSifi3BoMTqwyw', 'fee': 10000000, 'feeScale': 100, 'timestamp': 1646973577747307008, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': 'SostBqsKNpp41TiLwh2K3HWzSu4Djs9JNUNyUTJr57Mi4XE4Pc1bKzi8VBWPXux7HoXDEQDEcTfdefphFj7Utsi'}], 'amount': 10000000000, 'recipient': 'AUA1pbbCFyFSte38uENPXSAhZa7TH74V2Tc'}, 'height': 1353923}
```

#### API Group: Contract
The group of APIs that share the prefix `/contract`

```python
import py_vsys as pv

# api: pv.NodeAPI
print(api.ctrt)

tok_id = "TWu2qeuPdfjFQ7HdZGqjSYCSTh3m9k7kCttv7NmSx"
# /contract/tokenInfo/{tok_id}
resp = await api.ctrt.get_tok_info(tok_id)
print(resp)
```
Example output

```
<py_vsys.api.Contract object at 0x1048bfa90>
{'tokenId': 'TWu2qeuPdfjFQ7HdZGqjSYCSTh3m9k7kCttv7NmSx', 'contractId': 'CF6sVHb2Y8i5Cqcw5yZL1m2PmaTvk1KdB2T', 'max': 10000, 'total': 3000, 'unity': 100, 'description': ''}
```

#### API Group: Addresses
The group of APIs that share the prefix `/addresses`

```python
import py_vsys as pv

# api: pv.NodeAPI
print(api.addr)

addr = "AUA1pbbCFyFSte38uENPXSAhZa7TH74V2Tc"
# /addresses/balance/{addr}
resp = await api.addr.get_balance(addr)
print(resp)
```
Example output

```
<py_vsys.api.Addresses object at 0x10447f820>
{'address': 'AUA1pbbCFyFSte38uENPXSAhZa7TH74V2Tc', 'confirmations': 0, 'balance': 43841972357033332}
```

#### API Group: Database
The group of APIs that share the prefix `/database`

```python
import py_vsys as pv

# api: pv.NodeAPI
print(api.db)

addr = "AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD"
db_key = "foo"
# /database/get/{addr}/{db_key}
resp = await api.db.get(addr, db_key)
print(resp)
```
Example output

```
<py_vsys.api.Database object at 0x1024cbb50>
{'data': 'bar', 'type': 'ByteArray'}
```

#### API Group: Leasing
The group of APIs that share the prefix `/leasing`

```python
import py_vsys as pv

# api: pv.NodeAPI
print(api.leasing)

payload = {
    'senderPublicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL',
    'recipient': 'AUA1pbbCFyFSte38uENPXSAhZa7TH74V2Tc',
    'amount': 10000000000,
    'fee': 10000000,
    'feeScale': 100,
    'timestamp': 1646992205900354048,
    'signature': '4FMiksAtvzhWXBVpDBWF8dXai8VXgC4yj8DFGyMdvWXcWMiaPeQYVuhpA8319UmG4z5BiQsX1KXrUm42ccwyTMWH',
}

# /leasing/broadcast/lease
resp = await api.leasing.broadcast_lease(payload)
print(resp)
```
Example output

```
<py_vsys.api.Leasing object at 0x1044cfbb0>
{'type': 3, 'id': 'Bg5dm8iqDuKCqi3gXpA2qMmNH3t66e9yrERfjTbthiCz', 'fee': 10000000, 'feeScale': 100, 'timestamp': 1646992205900354048, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '4FMiksAtvzhWXBVpDBWF8dXai8VXgC4yj8DFGyMdvWXcWMiaPeQYVuhpA8319UmG4z5BiQsX1KXrUm42ccwyTMWH'}], 'amount': 10000000000, 'recipient': 'AUA1pbbCFyFSte38uENPXSAhZa7TH74V2Tc'}
```

#### API Group: VSYS
The group of APIs that share the prefix `/vsys`

```python
import py_vsys as pv

# api: pv.NodeAPI
print(api.vsys)

payload = {
    'senderPublicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL',
    'recipient': 'AU5NsHE8eC2guo3JobD8jrGvnEDQhBP8GtW',
    'amount': 10000000000,
    'fee': 10000000,
    'feeScale': 100,
    'timestamp': 1646993201931712000,
    'attachment': '',
    'signature': 'mjmu9CwQiUhtUkgVXFefpw8GM9Zypjf64pAufuUK5SvaGc9x8m9qZo8aRprnw7DmWRT4YQyPStTCERomGncRSMd',
}
resp = await api.vsys.broadcast_payment(payload)
print(resp)
```
Example output

```
<py_vsys.api.VSYS object at 0x1020afd00>
{'type': 2, 'id': 'D2UUnSX9gWnsTWW2tEs1BoF4dgZeyZRXQETrEUjUNrns', 'fee': 10000000, 'feeScale': 100, 'timestamp': 1646993201931712000, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': 'mjmu9CwQiUhtUkgVXFefpw8GM9Zypjf64pAufuUK5SvaGc9x8m9qZo8aRprnw7DmWRT4YQyPStTCERomGncRSMd'}], 'recipient': 'AU5NsHE8eC2guo3JobD8jrGvnEDQhBP8GtW', 'amount': 10000000000, 'attachment': ''}
```

### Actions

#### Make HTTP GET Request
Make an HTTP GET request to given endpoint.

```python
import py_vsys as pv

# api: pv.NodeAPI

resp = await api.get("/node/version")
print(resp)
```
Example output

```
{'version': 'VSYS Core v0.4.1'}
```

#### Make HTTP POST Request
Make an HTTP POST request to given endpoint.

```python
import py_vsys as pv

# api: pv.NodeAPI

resp = await api.post("/utils/hash/fast", "foo")
print(resp)
```
Example output

```
{'message': 'foo', 'hash': 'DT9CxyH887V4WJoNq9KxcpnF68622oK3BNJ41C2TvESx'}
```
