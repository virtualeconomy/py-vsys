# Account

- [Account](#account)
  - [Introduction](#introduction)
  - [Usage with Python SDK](#usage-with-python-sdk)
      - [Create Account](#create-account)
      - [From Wallet](#from-wallet)
      - [From Private Key & Public Key](#from-private-key--public-key)
    - [Properties](#properties)
      - [Chain](#chain)
      - [Api](#api)
      - [Key Pair](#key-pair)
      - [Address](#address)
      - [VSYS Balance](#vsys-balance)
      - [VSYS Available Balance](#vsys-available-balance)
      - [VSYS Effective Balance](#vsys-effective-balance)
    - [Actions](#actions)
      - [Get Token Balance](#get-token-balance)
      - [Pay](#pay)
      - [Lease](#lease)
      - [Cancel Lease](#cancel-lease)
      - [DB Put](#db-put)
      - [Register Contract](#register-contract)
      - [Execute Contract](#execute-contract)


## Introduction
Account is the basic entity in the VSYS blockchain that pocesses tokens & can take actions(e.g. send tokens, execute smart contracts).

There are 2 kinds of accounts:
- user account: the most common account.
- contract account: the account for a smart contract instance.

The key difference between them lies in whether they have a private key. 

## Usage with Python SDK

In Python SDK we have an `Account` class that represents a user account on the VSYS blockchain.

### Create Account

#### From Wallet
The `Account` object can be contructed by a `Wallet` object given the `Chain` object & nonce.

```python
import py_vsys as pv
# ch: pv.Chain
# wal: pv.Wallet
acnt0 = wal.get_account(ch, 0) # get the account of nonce 0 of the wallet.
```

#### From Private Key & Public Key
The `Account` object can be constructed by a private key & opionally along with a public key.

If the public key is omitted, it will be derived from the private key.
If the public key is provided, it will be verified against the private key.

```python
import py_vsys as pv
# ch: pv.Chain
acnt0 = pv.Account.from_pri_key_str(ch, 'your_private_key')
acnt1 = pv.Account(ch, new pv.PriKey('your_private_key'))
acnt2 = pv.Account(ch, pv.PriKey('your_private_key'), pv.PubKey('your_public_key'))

### Properties

#### Chain
The `Chain` object that represents the VSYS blockchain this account is on.

```python
import py_vsys as pv

# acnt: pv.Account
print(acnt.chain)
```
Example output

```
<py_vsys.chain.Chain object at 0x1049bd600>
```

#### Api
The `NodeAPI` object that serves as the API wrapper for calling RESTful APIs that exposed by a node in the VSYS blockchain.

```python
import py_vsys as pv

# acnt: pv.Account
print(acnt.api)
```
Example output

```
<py_vsys.api.NodeAPI object at 0x1027c1b10>
```

#### Key Pair
The private/public key pair of the account.

```python
import py_vsys as pv

# acnt: pv.Account
print(acnt.key_pair)
```
Example output

```
KeyPair(pub=PubKey(E37HXTArr5mEB9evjMV3dt1av2mFudV9pqs4mVRk7Zci), pri=PriKey(2cs89wr7JMRgrhcbMcEB1gFJdeNfYZ4dDiR7k3SEY5Zt))
```

#### Address
The address of the account.

```python
import py_vsys as pv

# acnt: pv.Account
print(acnt.addr)
```
Example output

```
Addr(ATx9rN83PdwbwtXoQzpWx7sZG4xKT2mG8nX)
```

#### VSYS Balance
The VSYS ledger(regular) balance of the account.

```python
import py_vsys as pv

# acnt: pv.Account
print(await acnt.bal)
```
Example output

```
VSYS(4866410339105012)
```

#### VSYS Available Balance
The VSYS available balance(i.e. the balance that can be spent) of the account.
The amount leased out will be reflected in this balance.

```python
import py_vsys as pv

# acnt: pv.Account
print(await acnt.avail_bal)
```
Example output

```
VSYS(4866397839105012)
```

#### VSYS Effective Balance
The VSYS effective balance(i.e. the balance that counts when contending a slot) of the account.
The amount leased in & out will be reflected in this balance.

```python
import py_vsys as pv

# acnt: pv.Account
print(await acnt.eff_bal)
```
Example output

```
VSYS(4866397839105012)
```

### Actions

#### Get Token Balance
Get the account balance of the token of the given token ID.

The example below shows querying the token balance of a certain kind of token.
```python
import py_vsys as pv

# acnt0: pv.Account
tok_id = "TWu66r3ebS3twXNWh7aiAEWcNAaRPs1JxkAw2A3Hi"

print(await acnt0.get_tok_bal(tok_id))
```
Example output

```
Token(900)
```

#### Pay
Pay the VSYS coins from the action taker to the recipient.

The example below shows paying 100 VSYS coins to another account.
```python
import py_vsys as pv

# acnt0: pv.Account
# acnt1: pv.Account

resp = await acnt0.pay(
    recipient=acnt1.addr.data,
    amount=100,
)
print(resp)
```
Example output

```
{'type': 2, 'id': '6jaDmqgJi5sHzKngcFWudRNMonvYqoTG7nrZq8emCP8c', 'fee': 10000000, 'feeScale': 100, 'timestamp': 1646971877892101120, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '4PxFL3JjQDGeibWwVfvtpqqqQxdnVyjfzVzYYh4hiAyecfQmMg9fVqJLR5L578b2Y4o2W4rxfWVM8GefGZxfJRWo'}], 'recipient': 'AU5NsHE8eC2guo3JobD8jrGvnEDQhBP8GtW', 'amount': 10000000000, 'attachment': ''}
```

#### Lease
Lease the VSYS coins from the action taker to the recipient(a supernode).

Note that the transaction ID in the response can be used to cancel leasing later.

The example below shows leasing 100 VSYS coins to a supernode.

```python
import py_vsys as pv

# acnt0: pv.Account

supernode_addr = "AUA1pbbCFyFSte38uENPXSAhZa7TH74V2Tc"
resp = await acnt0.lease(
    supernode_addr=supernode_addr,
    amount=100,
)
print(resp)
```
Example output

```
{'type': 3, 'id': '3gjreLTVhHZfqLYVNwFEmUgKYJr3T6iSifi3BoMTqwyw', 'fee': 10000000, 'feeScale': 100, 'timestamp': 1646973577747307008, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': 'SostBqsKNpp41TiLwh2K3HWzSu4Djs9JNUNyUTJr57Mi4XE4Pc1bKzi8VBWPXux7HoXDEQDEcTfdefphFj7Utsi'}], 'amount': 10000000000, 'recipient': 'AUA1pbbCFyFSte38uENPXSAhZa7TH74V2Tc'}
```

#### Cancel Lease
Cancel the leasing based on the leasing transaction ID.

```python
import py_vsys as pv

# acnt0: pv.Account

leasing_tx_id = "3gjreLTVhHZfqLYVNwFEmUgKYJr3T6iSifi3BoMTqwyw"
resp = await acnt0.cancel_lease(
    leasing_tx_id=leasing_tx_id,
)
print(resp)
```
Example output

```
{'type': 4, 'id': 'Eui1yaRcE4jCnf4yBawroxSvqGa54WyQV9LjHkRHVvPd', 'fee': 10000000, 'feeScale': 100, 'timestamp': 1646974337469929984, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '3MHpURmQHBAedZ6qww5372B4gYZrVUUD7jgjChn7mecqQECxmaU1f1KURY5eK4UebaSpHQMpFbURth6EP3vL4LPL'}], 'leaseId': '3gjreLTVhHZfqLYVNwFEmUgKYJr3T6iSifi3BoMTqwyw'}
```

#### DB Put
Store the data with a key onto the chain(i.e. treat chain as a key-value store)

```python
import py_vsys as pv

# acnt: pv.Account

resp = await acnt.db_put(
    db_key="foo",
    data="bar",
)
print(resp)
```
Example output

```
{'type': 10, 'id': 'B5vxEnY1cPQ2GLQVLDRNKoXY2vtacEmqCAdyCxbPwmfK', 'fee': 100000000, 'feeScale': 100, 'timestamp': 1646975057234319104, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '37vhwQYASAwVoUENoo3xHvCJCkaAriAgnYBPdwQkt3brj4yDybhK8H1BsXpMgvvdX7ScwTQP7qtYNGeABoAzL8Qr'}], 'dbKey': 'foo', 'entry': {'data': 'bar', 'type': 'ByteArray'}}
```

The stored data can be queried by calling the node endpoint `/database/get/{addr}/{db_key}`

```bash
curl -X 'GET' \                                                                          
  'http://veldidina.vos.systems:9928/database/get/AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD/foo' \
  -H 'accept: application/json'
```
Example output

```
{
  "data" : "bar",
  "type" : "ByteArray"
}
```

Or we can use the `NodeAPI` object

```python
import py_vsys as pv

# api: pv.NodeAPI
# acnt: pv.Account

resp = await api.db.get(
    addr=acnt.addr.data,
    db_key="foo",
)
print(resp)
```
Example output

```
{'data': 'bar', 'type': 'ByteArray'}
```

#### Register Contract
The `Account` class does not provide a public interface for this action. Users should always use a contract instance object and pass in the `Account` object as the action taker instead.

See [the example of registering an NFT contract instance](./smart_contract/nft_ctrt.md#registration).

#### Execute Contract
The `Account` class does not provide a public interface for this action. Users should always use a contract instance object and pass in the `Account` object as the action taker instead.

See [the example of executing a function of an NFT instance](./smart_contract/nft_ctrt.md#issue)
