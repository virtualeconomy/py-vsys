# Token Contract V1 With Split

- [Token Contract V1 With Split](#token-contract-v1-with-split)
  - [Introduction](#introduction)
  - [Usage with Python SDK](#usage-with-python-sdk)
    - [Work flow of the contract](#work-flow-of-the-contract)
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
      - [Split](#split)

## Introduction

*Token Contract V1 with Split* is the twin case for *[Token Contract V1 Without Split](./tok_ctrt_no_split.md)*.
The token unit can be updated at any time after the contract instance is registered.

## Usage with Python SDK

### Work flow of the contract

Remember to comment out the previous transaction when acting on the new transaction. Before start the new transaction, wait 6 seconds until the transaction is completely on blockchain.

First [register](#registration) a token contract with split, Keep a record of the contract id.

[Issue](issue) the tokens. The max issue amount is defined when the token contract is registered.

Now the tokens can be [deposited](#deposit) into(and [withdrawed](#withdraw) from) other smart contracts(except for token contract and system contract).

The contract also provide some optional functions. For example, [supersede](#supersede) is to transfer the owner right to another account, [transfer](#transfer) is a combination of deposit and withdraw, [destroy](#destroy) is to destroy a certain amount of the tokens, [split](#split) is to use the new unit of the token.

### Registration

The example below shows registering an instance of Token Contract V1 With Split where the max amount is 100 & the unit is 100.

```python
import py_vsys as pv

# acnt: pv.Account

tc = await pv.TokCtrtWithSplit.register(
    by=acnt,
    max=100,
    unit=100,
)
print(tc.ctrt_id)
```

Example output

```
CtrtID(CF1ZfEK9mch8mVv3Vg2qMMdt1BLpRf2oPv5)
```

### From Existing Contract

```python
import py_vsys as pv

# ch: pv.Chain

tc_id = "CF1ZfEK9mch8mVv3Vg2qMMdt1BLpRf2oPv5"
tc = pv.TokCtrtWithSplit(ctrt_id=tc_id, chain=ch)
```

### Querying

#### Issuer

The address that has the issuing right of the Token contract instance.

```python
# tc: pv.TokCtrtWithSplit

print(await tc.issuer)
```

Example output

```
Addr(AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD)
```

#### Maker

The address that made this Token contract instance.

```python
# tc: pv.TokCtrtWithSplit

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
# tc: pv.TokCtrtWithSplit

print(tc.tok_id)
```

Example output

```
TokenID(TWtS7LFdWTiyWvMJSBThL1Jz6z5WgKX6ECfxhYRcL)
```

#### Unit

The unit of the token defined in this token contract instance.

```python
# tc: pv.TokCtrtWithSplit

print(await tc.unit)
```

Example output

```
100
```

#### Token Balance

Query the balance of the token defined in the contract for the given user.

```python
# tc: pv.TokCtrtWithSplit
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
# tc: pv.TokCtrtWithSplit

resp = await tc.supersede(
    by=acnt0,
    new_issuer=acnt1.addr.data,
)
print(resp)
```

Example output

```
{'type': 9, 'id': '4j9tUbmzfMCuJKQ3sJiwoAjno8HRhmR5WHzTCMYUtLPw', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646705515857213952, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '2KCRJV4656drusZ4zxpNabigNnFESM6qMxewTBWaCeqctyPPPncTHsxBSHkheQ5GvpHEycb542bB5jWgz519XSDM'}], 'contractId': 'CF1ZfEK9mch8mVv3Vg2qMMdt1BLpRf2oPv5', 'functionIndex': 0, 'functionData': '1bscuEdeiiEkCJsLRbCmpioXRcWMkrs2oDToWe', 'attachment': ''}
```

#### Issue

Issue the a certain amount of the token. The issued tokens will belong to the issuer.

Note that only the address with the issuer role can take this action.

```python
import py_vsys as pv

# acnt: pv.Account
# tc: pv.TokCtrtWithSplit

resp = await tc.issue(by=acnt, amount=50)
print(resp)
```

Example output

```
{'type': 9, 'id': '3uHBo2Ghu5GBXCbxwdYSYmeyA2YbXAzUk6DXGybecTCo', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646705683303595008, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '3RG8vdULcsKDwt35J2Lj7So75sxYbcpf4U6JHGw3nKUZ7QwKA3QVyqSUYX9k7dZf2TxDqasG95DSCAyRKvsDZbgb'}], 'contractId': 'CF1ZfEK9mch8mVv3Vg2qMMdt1BLpRf2oPv5', 'functionIndex': 1, 'functionData': '14JDCrdo1xwuNP', 'attachment': ''}
```

#### Send

Send a certain amount of the token to another user.

```python
import py_vsys as pv

# acnt0: pv.Account
# acnt1: pv.Account
# tc: pv.TokCtrtWithSplit

resp = await tc.send(
  by=acnt0,
  recipient=acnt1.addr.data,
  amount=20,
)
print(resp)
```

Example output

```
{'type': 9, 'id': 'FutdE6MRi2fHQijq9gdA8XMRPgGmqQ2MX7u9hmKhLjpa', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646705781399777024, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '4yEvWDmUpZUq4WTebd5wtUjWWcDfpeVsKJAvxYJjVV9ZuazNAbpkEps2G6NcABaMMsBWrqudXpj9zARb4mC1b2dC'}], 'contractId': 'CF1ZfEK9mch8mVv3Vg2qMMdt1BLpRf2oPv5', 'functionIndex': 4, 'functionData': '14uNyNpGh4D3auRE5jksKK9H7tizHT5DbNBShom8LGbHFpqi3Ub', 'attachment': ''}
```

#### Destroy

Destroy a certain amount of the token.

Note that only the address with the issuer role can take this action.

```python
import py_vsys as pv

# acnt0: pv.Account
# tc: pv.TokCtrtWithSplit

resp = await tc.destroy(
    by=acnt0,
    amount=10,
)
print(resp)
```

Example output

```
{'type': 9, 'id': 'EwC1DNVthb5riGhzMu6xGLQcmEhokqsnzeYSS8chpYfW', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646705839798230016, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': 'XGtbSNUBUTEoUEqDYYTyk9dTDTraTqbULvkN81HwSvR8hNCRu8gFY9CeTQX4yTT7fSK5y2sXqP77sm7cy4xB23E'}], 'contractId': 'CF1ZfEK9mch8mVv3Vg2qMMdt1BLpRf2oPv5', 'functionIndex': 2, 'functionData': '14JDCrdo1xwtBR', 'attachment': ''}
```

#### Transfer

Transfer a certain amount of the token to another account(e.g. user or contract).
`transfer` is the underlying action of `send`, `deposit`, and `withdraw`. It is not recommended to use transfer directly. Use `send`, `deposit`, `withdraw` instead when possible.

```python
import py_vsys as pv

# acnt0: pv.Account
# tc: pv.TokCtrtWithSplit

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
{'type': 9, 'id': 'GGkPTgdFKTjC1AUSaWK1wLER8qcH2TgdKCVuEjPDjp4M', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646705914248229120, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '28v3yugPArZdpgAUxv98UGeiUvarJj5G2vF5EGiCnbbcoKUc4gVK7ujSgyZHgqqBPHJiKHHNebwUmVFoykaoCVhD'}], 'contractId': 'CF1ZfEK9mch8mVv3Vg2qMMdt1BLpRf2oPv5', 'functionIndex': 5, 'functionData': '14VJY1UVsRjjEvg94e3CH5K89Yz1bNaPjoKKwwVfYMFvHnKzYrLhFzpD2C2ySPoKUvUt4w61awTHWkoLB8dPrGsq', 'attachment': ''}
```

#### Deposit

Deposit a certain amount of the token into a token-holding contract instance(e.g. lock contract).

Note that only the token defined in the token-holding contract instance can be deposited into it.

```python
import py_vsys as pv

# acnt0: pv.Account
# tc: pv.TokCtrtWithSplit
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
{'type': 9, 'id': 'HPtbLKGB28aspgzzLSyBPEkQ13aGK5TEuouUq4FLCnMm', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646706036678279936, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': 'wfCkYQ3GmJLKhuxpCiwLs7jB9zofqpPyKCevBwNXPiNPktNGbhJLu6n6dkCepGpnjshP2dLCq2XWgMWJprtznHX'}], 'contractId': 'CF1ZfEK9mch8mVv3Vg2qMMdt1BLpRf2oPv5', 'functionIndex': 6, 'functionData': '14VJY1UVsRjjEvg94e3CH5K89Yz1bNaPjoKKwwVhJdAXJNcQrSwo7xeNEEVxASYu6FbzN2zkWRvtw37yAGCP9jFZ', 'attachment': ''}
```

#### Withdraw

Withdraw a certain amount of the token from a token-holding contract instance(e.g. lock contract).

Note that only the token defined in the token-holding contract instance can be withdrawn from it.

```python
import py_vsys as pv

# acnt0: pv.Account
# tc: pv.TokCtrtWithSplit
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
{'type': 9, 'id': 'Fbj8Ytvfh6TGxURD459tatPPpkHfYzaUxANvBbU1um7M', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646706081220137984, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '2LduSyCLRqSenHTJ1FUg5Ai2KPP9ocrUJwCNeCa9iNLibPm4BgRWfNL4xfnU63AoD29G3RYtcJiupo7afqgX33UH'}], 'contractId': 'CF1ZfEK9mch8mVv3Vg2qMMdt1BLpRf2oPv5', 'functionIndex': 7, 'functionData': '14WMYfAA41WAkgHsbs6UuSqKdhZnsf6LcNTr9qbLYJ5KFBdCuStnNnFYNXxFJvLLstov3P4zZ4YBbUmgmVU98bHM', 'attachment': ''}
```

#### Split

Update the unit of the token.

The address with the issuer & maker role can take this action.

```python
import py_vsys as pv

# acnt0: pv.Account
# tc: pv.TokCtrtWithSplit

resp = await tc.split(
    by=acnt0,
    new_unit=10,
)
print(resp)
```

Example output

```
{'type': 9, 'id': 'Fxm4sNdwmerXU9QC92eRjGhsP2AVJUdTdykLkxDroKD4', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646706321708814080, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '3WTNR67buoA4znuoXir1wrCUU3Nu4Nidqc4otpY4JGn5EYDwxEMi17Wmyr5axpXA9q63N3WvZdiMCj4WeHMwj1md'}], 'contractId': 'CF1ZfEK9mch8mVv3Vg2qMMdt1BLpRf2oPv5', 'functionIndex': 3, 'functionData': '14JDCrdo1xwstM', 'attachment': ''}
```