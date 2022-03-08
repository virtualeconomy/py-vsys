# Token Contract V1 Without Split

- [Token Contract V1 Without Split](#token-contract-v1-without-split)
  - [Introduction](#introduction)
  - [Usage with Python SDK](#usage-with-python-sdk)
    - [Registration](#registration)
    - [From Existing Contract](#from-existing-contract)
    - [Querying](#querying)
      - [Issuer](#issuer)
      - [Maker](#maker)
      - [Token ID](#token-id)
      - [Unit](#unit)
      - [Token Balance](#token-balance)
    - [Actions](#actions)
      - [Supersede](#supersede)
      - [Issue](#issue)
      - [Send](#send)
      - [Destroy](#destroy)
      - [Transfer](#transfer)
      - [Deposit](#deposit)
      - [Withdraw](#withdraw)

## Introduction

Token contract supports defining & managing custom tokens on VSYS blockchain.

A token is a logical entity on the blockchain. It can represent basically everything that can be stored in a database. Be it a fiat currency like USD, financial assets like a share in a company, or even reputation points of an online platform.

A contract can be thought of as a class in OOP with a bunch of methods. An instance needs to be created before using a contract. Every node will maintain the states for a contract instance. The user interacts with the contract instance by publishing transactions. Upon receiving transactions, every node will update the contract instance states accordingly.

*Token Contract V1 Without Split* is the classic version of token contracts supported by VSYS blockchain. The token unit cannot be updated once specified when registering the contract instance.

> “Unit” is the granularity of splitting a token. It can be thought of as the smallest denomination available. Let’s take real-world money as an example, if the unit is set to 100, it means the smallest denomination is a cent, and 100 cents is a dollar.
> 
> With “Unit”, float numbers can be represented in integers so as to avoid the uncertainty comes from float computation. If we set unit == 100, 1.5 tokens are actually stored as 150 on the blockchain.

## Usage with Python SDK

### Registration

The example below shows registering an instance of Token Contract V1 Without Split where the max amount is 100 & the unit is 100.

```python
import py_vsys as pv

# acnt: pv.Account

tc = await pv.TokCtrtWithoutSplit.register(
    by=acnt,
    max=100,
    unit=100,
)
print(tc.ctrt_id)
```
Example output

```
CtrtID(CF6sVHb2Y8i5Cqcw5yZL1m2PmaTvk1KdB2T)
```

### From Existing Contract

```python
import py_vsys as pv

# ch: pv.Chain

tc_id = "CF6sVHb2Y8i5Cqcw5yZL1m2PmaTvk1KdB2T"
tc = pv.TokCtrtWithoutSplit(ctrt_id=tc_id, chain=ch)
```

### Querying

#### Issuer

The address that has the issuing right of the Token contract instance.

```python
# tc: pv.TokCtrtWithoutSplit

print(await tc.issuer)
```
Example output

```
Addr(AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD)
```

#### Maker

The address that made this Token contract instance.

```python
# tc: pv.TokCtrtWithoutSplit

print(await tc.maker)
```
Example output

```
Addr(AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD)
```

#### Token ID
The token ID of the token defined in the token contract instance.

Note that theoretically a token contract instance can have multiple kinds of token, it is restricted to 1 kind of token per token contract instance. In other word, the token ID is of the token index `0`.

```python
# tc: pv.TokCtrtWithoutSplit

print(tc.tok_id)
```
Example output

```
TokenID(TWu2qeuPdfjFQ7HdZGqjSYCSTh3m9k7kCttv7NmSx)
```

#### Unit
The unit of the token defined in this token contract instance.

```python
# tc: pv.TokCtrtWithoutSplit

print(await tc.unit)
```
Example output

```
100
```

#### Token Balance
Query the balance of the token defined in the contract for the given user.

```python
# tc: pv.TokCtrtWithoutSplit
# acnt: pv.Account

print(await tc.get_tok_bal(acnt.addr.data))
```
Example output

```
Token(0)
```

### Actions

#### Supersede

Transfer the issuer role of the contract to a new user.
The maker of the contract has the privilege to take this action.

```python
import py_vsys as pv

# acnt0: pv.Account
# acnt1: pv.Account
# tc: pv.TokCtrtWithoutSplit

resp = await tc.supersede(
    by=acnt0,
    new_issuer=acnt1.addr.data,
)
print(resp)
```
Example output

```
{'type': 9, 'id': 'BMr5wn9oyqb4j3nhnZtnBeqht9zzdeXu8qqHQBjWFfPZ', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646641560702518016, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': 'gGYdunmfSmRop3oQFge1DXKVHF4AmHiVkscdd84R6ko4CKfNKYrdaXZSyNAhYVPmnwzkMjQwfbWX7mAsFctemx6'}], 'contractId': 'CF6sVHb2Y8i5Cqcw5yZL1m2PmaTvk1KdB2T', 'functionIndex': 0, 'functionData': '1bscuEdeiiEkCJsLRbCmpioXRcWMkrs2oDToWe', 'attachment': ''}
```


#### Issue

Issue the a certain amount of the token. The issued tokens will belong to the issuer.

Note that only the address with the issuer role can take this action.

```python
import py_vsys as pv

# acnt: pv.Account
# tc: pv.TokCtrtWithoutSplit

resp = await tc.issue(by=acnt, amount=50)
print(resp)
```
Example output

```
{'type': 9, 'id': 'GvgVpZEmPFo5p7N8PCRNYiSZTkeyTyZ8Hr2idcE8G2Ro', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646642183709975040, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '3DBzgSgbWaLbfST8sJbxtqjR4sg67qQj9yBFumfjf7qdaYX5F44BFcb6UR5L2PMK2PE5ZorMMw7ctmwMuo7qFeFw'}], 'contractId': 'CF6sVHb2Y8i5Cqcw5yZL1m2PmaTvk1KdB2T', 'functionIndex': 1, 'functionData': '14JDCrdo1xwuNP', 'attachment': ''}
```

#### Send
Send a certain amount of the token to another user.

```python
import py_vsys as pv

# acnt0: pv.Account
# acnt1: pv.Account
# tc: pv.TokCtrtWithoutSplit

resp = await tc.send(
  by=acnt0,
  recipient=acnt1.addr.data,
  amount=20,
)
print(resp)
```
Example output

```
{'type': 9, 'id': '2jNngUsL3L3haby6gDux1NAPKs49k7AKLb79ibiCR2QR', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646642218424199936, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': 'G7hRTNpnPgZYGtAS25ci1VbP4P2AUK83A1ope6nGrxQk1d7uMX8WfNqL7A6nWxdbWRMzQSXJ2bi9i5oUCZwcAHB'}], 'contractId': 'CF6sVHb2Y8i5Cqcw5yZL1m2PmaTvk1KdB2T', 'functionIndex': 3, 'functionData': '14uNyNpGh4D3auRE5jksKK9H7tizHT5DbNBShom8LGbHFpqi3Ub', 'attachment': ''}
```

#### Destroy
Destroy a certain amount of the token.

Note that only the address with the issuer role can take this action.

```python
import py_vsys as pv

# acnt0: pv.Account
# tc: pv.TokCtrtWithoutSplit

resp = await tc.destroy(
    by=acnt0,
    amount=10,
)
print(resp)
```
Example output

```
{'type': 9, 'id': '4DoQBSEV61EJ4DiDtUgmGjyjCXbRTJRg7BkjHvCAdo4F', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646642455891747072, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '6d278jfmS2VinpvQKxPc3DjHzyiyXKBxbbGR7FKb9qrpg1511Uxw57GSREX7ztNiA5QEzpRNEob3hhQ4LUxooDX'}], 'contractId': 'CF6sVHb2Y8i5Cqcw5yZL1m2PmaTvk1KdB2T', 'functionIndex': 2, 'functionData': '14JDCrdo1xwtBR', 'attachment': ''}
```

#### Transfer
Transfer a certain amount of the token to another account(e.g. user or contract).
`transfer` is the underlying action of `send`, `deposit`, and `withdraw`. It is not recommended to use transfer directly. Use `send`, `deposit`, `withdraw` instead when possible.

```python
import py_vsys as pv

# acnt0: pv.Account
# tc: pv.TokCtrtWithoutSplit

resp = await tc.transfer(
    by=acnt0,
    sender=acnt0.addr.data,
    recipient=acnt1.addr.data,
    amount=10,
)
print(resp)
```
Example output

```
{'type': 9, 'id': 'FHu2jZpFT1Qv6mRsqrPBpEzTG89ztsn9zohFf1rRk5kC', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646642740801181952, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '3AgDa44uN7biSNei2tZqgTXTPpDVZTAk4UsVtBkL2bgEHh8pyY3TbrZLe7tR8gYkecJSaB58DowTQa9CejShsUUn'}], 'contractId': 'CF6sVHb2Y8i5Cqcw5yZL1m2PmaTvk1KdB2T', 'functionIndex': 4, 'functionData': '14VJY1UVsRjjEvg94e3CH5K89Yz1bNaPjoKKwwVfYMFvHnKzYrLhFzpD2C2ySPoKUvUt4w61awTHWkoLB8dPrGsq', 'attachment': ''}
```

#### Deposit
Deposit a certain amount of the token into a token-holding contract instance(e.g. lock contract).

Note that only the token defined in the token-holding contract instance can be deposited into it.

```python
import py_vsys as pv

# acnt0: pv.Account
# tc: pv.TokCtrtWithoutSplit
# lc: pv.LockCtrt

lc_id = lc.ctrt_id.data

resp = await tc.deposit(
    by=acnt0,
    ctrt_id=lc_id,
    amount=5,
)
print(resp)
```
Example output

```
{'type': 9, 'id': 'GNTivdQJh5DcQKoSm7sVcHGC2ALC8t9yFUyZBdZLpy1H', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646643099545323008, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '2SmU3LHdKjL195nU9DX8eQZC8w4w1N3RFtQS2gjwAgwNgyBu1LrvxhdceEtLVYQJTnatPMsu8VcwuYMp6UDzR4oU'}], 'contractId': 'CF6sVHb2Y8i5Cqcw5yZL1m2PmaTvk1KdB2T', 'functionIndex': 5, 'functionData': '14VJY1UVsRjjEvg94e3CH5K89Yz1bNaPjoKKwwVhJdBaSWUoYMS2otaaZ4psAeLyr2KyAm5YkEaXVfAx8bDSUYZH', 'attachment': ''}
```

#### Withdraw
Withdraw a certain amount of the token from a token-holding contract instance(e.g. lock contract).

Note that only the token defined in the token-holding contract instance can be withdrawn from it.

```python
import py_vsys as pv

# acnt0: pv.Account
# tc: pv.TokCtrtWithoutSplit
# lc: pv.LockCtrt

lc_id = lc.ctrt_id.data

resp = await tc.withdraw(
    by=acnt0,
    ctrt_id=lc_id,
    amount=5,
)
print(resp)
```
Example output

```
{'type': 9, 'id': 'PZGWTQzwzCiKQZRy677mQVLFvi8teqcghF8ddXxzg9h', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646643599577479936, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '5NcR3LCnxxjsp8v55vkrhSAcxRGupjcojw1m2yRz2diUYAynPhtd274SQLRLHRueNqvnhe1Tq6NwJM2H8DoHXmbp'}], 'contractId': 'CF6sVHb2Y8i5Cqcw5yZL1m2PmaTvk1KdB2T', 'functionIndex': 6, 'functionData': '14WMYfndUwrPJtBkWS3RZbe4ofzCU6cv5jv9wLoHxGh3eK5zpQYYPMXzEURWV7cLcuf5LKUuLS2XzZUvjGvZKsw1', 'attachment': ''}
```
