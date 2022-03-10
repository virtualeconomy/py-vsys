# Account

- [Account](#account)
  - [Introduction](#introduction)
  - [Usage with Python SDK](#usage-with-python-sdk)
    - [Properties](#properties)
      - [Chain](#chain)
      - [Api](#api)
      - [Wallet](#wallet)
      - [Nonce](#nonce)
      - [Account Seed Hash](#account-seed-hash)
      - [Key Pair](#key-pair)
      - [Address](#address)
      - [VSYS Balance](#vsys-balance)
      - [VSYS Available Balance](#vsys-available-balance)
      - [VSYS Effective Balance](#vsys-effective-balance)
    - [Actions](#actions)


## Introduction
Account is the basic entity in the VSYS blockchain that pocesses tokens & can take actions(e.g. send tokens, execute smart contracts).

There are 2 kinds of accounts:
- user account: the most common account.
- contract account: the account for a smart contract instance.

The key difference between them lies in whether they have a private key. 

## Usage with Python SDK

In Python SDK we have an `Account` class that represents a user account on the VSYS blockchain.


### Properties

#### Chain
The `Chain` object that represents the VSYS blockchain this account is on.

```python
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
# acnt: pv.Account
print(acnt.api)
```
Example output

```
<py_vsys.api.NodeAPI object at 0x1027c1b10>
```

#### Wallet
The `Wallet` object that represents the wallet that contains this account.

```python
# acnt: pv.Account
print(acnt.wallet)
```
Example output

```
<py_vsys.account.Wallet object at 0x102765540>
```

#### Nonce
The nonce of this account in the wallet.

```python
# acnt: pv.Account
print(acnt.nonce)
```
Example output

```
Nonce(0)
```

#### Account Seed Hash
Account Seed Hash is the hashing result of
- the seed of the wallet the account is in
- the nonce of the account that

Account Seed Hash can be used to generate the private/public key pair of the account.



#### Key Pair

#### Address

#### VSYS Balance

#### VSYS Available Balance

#### VSYS Effective Balance


### Actions

