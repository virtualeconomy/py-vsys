# Token Contract V2 Without Split

- [Token Contract V2 Without Split](#token-contract-v2-without-split)
  - [Introduction](#introduction)
  - [Usage with Python SDK](#usage-with-python-sdk)
    - [Registration](#registration)
    - [From Existing Contract](#from-existing-contract)
    - [Querying](#querying)
      - [Issuer](#issuer)
      - [Maker](#maker)
      - [Regulator](#regulator)
      - [Token ID](#token-id)
      - [Unit](#unit)
      - [Token Balance](#token-balance)
    - [Actions](#actions)
      - [Supersede](#supersede)
      - [Issue](#issue)
      - [Add/remove a user from the list](#addremove-a-user-from-the-list)
      - [Add/remove a contract from the list](#addremove-a-contract-from-the-list)
      - [Send](#send)
      - [Destroy](#destroy)
      - [Transfer](#transfer)
      - [Deposit](#deposit)
      - [Withdraw](#withdraw)

## Introduction

*Token Contract V2 Without Split* adds additional whitelist/blacklist regulation feature upon *[Token Contract V1 Without Split](./tok_ctrt_no_split.md)*

For the whitelist flavor, only users & contracts included in the list can interact with the contract instance.

For the blacklist flavor, only users & contracts excluded from the list can interact with the contract instance.

## Usage with Python SDK

### Registration

The example below shows registering an instance of Token Contract V2 Without Split with whitelist where the max amount is 100 & the unit is 100.

The usage of the blacklist one is very similiar.

```python
import py_vsys as pv

# acnt: pv.Account

tc = await pv.TokCtrtWithoutSplitV2Whitelist.register(
    by=acnt,
    max=100,
    unit=100,
)
print(tc.ctrt_id)
```
Example output

```
CtrtID(CFAqvw8z97XFvbMd5w2xMLi8tAXkXGYKR2x)
```

### From Existing Contract

```python
import py_vsys as pv

# ch: pv.Chain

tc_id = "CFAqvw8z97XFvbMd5w2xMLi8tAXkXGYKR2x"
tc = pv.TokCtrtWithoutSplitV2Whitelist(ctrt_id=tc_id, chain=ch)
```

### Querying

#### Issuer

The address that has the issuing right of the Token contract instance.

```python
# tc: pv.TokCtrtWithoutSplitV2Whitelist

print(await tc.issuer)
```
Example output

```
Addr(AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD)
```

#### Maker

The address that made this Token contract instance.

```python
# tc: pv.TokCtrtWithoutSplitV2Whitelist

print(await tc.maker)
```
Example output

```
Addr(AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD)
```

#### Regulator
The address that serves as the regulator of the contract instance.

The maker becomes the regulator by default.

```python
# tc: pv.TokCtrtWithoutSplitV2Whitelist

print(await tc.regulator)
```
Example output

```
Addr(AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD)
```


#### Token ID
The token ID of the token defined in the token contract instance.

Note that theoretically a token contract instance can have multiple kinds of token, it is restricted to 1 kind of token per token contract instance. In other word, the token ID is of the token index `0`.

```python
# tc: pv.TokCtrtWithoutSplitV2Whitelist

print(tc.tok_id)
```
Example output

```
TokenID(TWuUqazJzimNYkD5Be8GvDSsRaLE7wRjT7qbfxXqE)
```

#### Unit
The unit of the token defined in this token contract instance.

```python
# tc: pv.TokCtrtWithoutSplitV2Whitelist

print(await tc.unit)
```
Example output

```
100
```

#### Token Balance
Query the balance of the token defined in the contract for the given user.

```python
# tc: pv.TokCtrtWithoutSplitV2Whitelist
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
# acnt2: pv.Account
# tc: pv.TokCtrtWithoutSplitV2Whitelist

resp = await tc.supersede(
    by=acnt0,
    new_issuer=acnt1.addr.data,
    new_regulator=acnt2.addr.data,
)
print(resp)
```
Example output

```
{{'type': 9, 'id': '7vnuBV7kTT7vWXuRGsxGkLA3NrEcZCEdG8SMgywYKGUa', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646719340336879104, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '5dVqvGU6mnwPJhKeeAoWbrtyJLN78TNKDoeWpEMWEi3JFUVSjvxsexq7s3qs35zkmLHgyWPVUbfottqsdb7dfy8Y'}], 'contractId': 'CFAqvw8z97XFvbMd5w2xMLi8tAXkXGYKR2x', 'functionIndex': 0, 'functionData': '1iSib21mKY5QhoPcoPYTNqwSv8VaM5AN4wzmCcod4q7P4NEy1A7sr4j4F6tfxVkycuJifHWcLMR', 'attachment': ''}
```

#### Issue
Issue a certain amount of the token. The issued tokens will belong to the issuer.

Note that only the address with the issuer role can take this action.

```python
import py_vsys as pv

# acnt: pv.Account
# tc: pv.TokCtrtWithoutSplitV2Whitelist

resp = await tc.issue(by=acnt, amount=50)
print(resp)
```
Example output

```
{'type': 9, 'id': '3AMC4ggfMiNgp52dBKza7vfxFSg7kKfFdjF3atNhgAa4', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646719955803010048, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': 'XTxiAz87rBo8CSLM1hcM9413G7SiNZ2oqcqDrVvAwXGiRNQ1Zgs7F27nuPw5HYnKsTf2SWWApHoE5kdE7JXv58Q'}], 'contractId': 'CFAqvw8z97XFvbMd5w2xMLi8tAXkXGYKR2x', 'functionIndex': 1, 'functionData': '14JDCrdo1xwuNP', 'attachment': ''}
```

#### Add/remove a user from the list
Add/remove a user from the whitelist/blacklist.

Note the regulator has the privilege to take this action.

```python
import py_vsys as pv

# acnt0: pv.Account
# acnt1: pv.Account
# tc: pv.TokCtrtWithoutSplitV2Whitelist

resp = await tc.update_list_user(
    by=acnt0,
    addr=acnt1.addr.data,
    val=True, # False to remove
)
print(resp)
```
Example output

```
{'type': 9, 'id': 'C4rJjRM1LfZqgD2MJHDAkrj89Hq48fvfp6RhLovSgiuj', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646720333520907008, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '5gyt3svRjWZWMMjJxoWm6K2CJYfgmGudMJrxnr1HBz3pqkB3wwVo2VXF4EhWrZNjjVvnKzUMxX4Ee3rVyLfkCEQT'}], 'contractId': 'CFAqvw8z97XFvbMd5w2xMLi8tAXkXGYKR2x', 'functionIndex': 3, 'functionData': '1QLRyUKuvAg1foWyW4NLRc14fe8HLzgbs9ZeHYNK2', 'attachment': ''}
```

#### Add/remove a contract from the list
Add/remove a contract from the whitelist/blacklist.

Note the regulator has the privilege to take this action.

```python
import py_vsys as pv

# acnt0: pv.Account
# acnt1: pv.Account
# nc: pv.TokCtrtWithoutSplitV2Whitelist

arbitrary_ctrt_id = "CF5Zkj2Ycx72WrBnjrcNHvJRVwsbNX1tjgT"

resp = await nc.update_list_ctrt(
    by=acnt0,
    addr=arbitrary_ctrt_id,
    val=True, # False to remove
)
print(resp)
```
Example output

```
{'type': 9, 'id': 'G5pxgD6L19mX2MnxXRKoaRLQKdk9tHmenHKRKcd6h7rX', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646721282372962048, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': 'ehDBud1UvisScQrvmAZAf8ewYFrVc9wQmR2CmMsnxhFieKeXAfMgH45aLRYHgLP4AXVmPhRT42QXXCBAc7XUZsN'}], 'contractId': 'CFAqvw8z97XFvbMd5w2xMLi8tAXkXGYKR2x', 'functionIndex': 3, 'functionData': '1QWyS5TmAbHA8jyaykmqtcJz5oezpMiXGSM4JZMyJ', 'attachment': ''}
```

#### Send
Send a certain amount of the token to another user.

```python
import py_vsys as pv

# acnt0: pv.Account
# acnt1: pv.Account
# tc: pv.TokCtrtWithoutSplitV2Whitelist

resp = await tc.send(
  by=acnt0,
  recipient=acnt1.addr.data,
  amount=20,
)
print(resp)
```
Example output

```
{'type': 9, 'id': 'EJgdFrbTrFccHzEhdTsrZY7mTkv3M1ZwxkzPWuEr4hyN', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646721384360334080, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '2JEP7pLpnqhewos9X3Gpak2smHoWBLA4g2pF7kxawNvtDi3ESnn6wgMmg4XbkQe712ckiuZ3Vv76aCJriVXxDVGb'}], 'contractId': 'CFAqvw8z97XFvbMd5w2xMLi8tAXkXGYKR2x', 'functionIndex': 4, 'functionData': '14uNyNpGh4D3auRE5jksKK9H7tizHT5DbNBShom8LGbHFpqi3Ub', 'attachment': ''}
```

#### Destroy
Destroy a certain amount of the token.

Note that only the address with the issuer role can take this action.

```python
import py_vsys as pv

# acnt0: pv.Account
# tc: pv.TokCtrtWithoutSplitV2Whitelist

resp = await tc.destroy(
    by=acnt0,
    amount=10,
)
print(resp)
```
Example output

```
{'type': 9, 'id': 'AHfXy1LrXXnb2kPS4HiJb3bUJgUa7cNdx1ENRdXHxchp', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646722638325474048, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '8hbLGyg1HHbrPGbgW3a3AU8ZWNL55p1dn7aJyv3oabDyh6bGaYhCs5taLFqPQHtFPtG6Psz7ViKVNWokXfVAkK8'}], 'contractId': 'CFAqvw8z97XFvbMd5w2xMLi8tAXkXGYKR2x', 'functionIndex': 2, 'functionData': '14JDCrdo1xwtBR', 'attachment': ''}
```

#### Transfer
Transfer a certain amount of the token to another account(e.g. user or contract).
`transfer` is the underlying action of `send`, `deposit`, and `withdraw`. It is not recommended to use transfer directly. Use `send`, `deposit`, `withdraw` instead when possible.

```python
import py_vsys as pv

# acnt0: pv.Account
# tc: pv.TokCtrtWithoutSplitV2Whitelist

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
{'type': 9, 'id': '4kuzPtiHigRcuyTQtm1U6CG9QhgDgTEArjuoSBCfyunj', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646722691839205120, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': 'K1NJ5NgqgsSSYs3FwXTxdFhxiqVuwQBbT9ZPZoyg1hYQWjL8idHLPjTAd7t6vnPoGXWqftByCbLEK8CeAdgEGrU'}], 'contractId': 'CFAqvw8z97XFvbMd5w2xMLi8tAXkXGYKR2x', 'functionIndex': 5, 'functionData': '14VJY1UVsRjjEvg94e3CH5K89Yz1bNaPjoKKwwVfYMFvHnKzYrLhFzpD2C2ySPoKUvUt4w61awTHWkoLB8dPrGsq', 'attachment': ''}
```

#### Deposit
Deposit a certain amount of the token into a token-holding contract instance(e.g. lock contract).

Note that only the token defined in the token-holding contract instance can be deposited into it.

```python
import py_vsys as pv

# acnt0: pv.Account
# tc: pv.TokCtrtWithoutSplitV2Whitelist
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
{'type': 9, 'id': '34Jf8eXrGuQeRhvkkfsqgKK43iS5mtxAWTS4xuHHoS2j', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646722889180108032, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '3hD8fyatUevBGRjNnnsyJBA19YXCYVyeBg3FrNgEJLzewzCZLSXAr3Kud5W5P1K3JEP4SVi1TB4ks5CCyxsFRM3f'}], 'contractId': 'CFAqvw8z97XFvbMd5w2xMLi8tAXkXGYKR2x', 'functionIndex': 6, 'functionData': '14VJY1UVsRjjEvg94e3CH5K89Yz1bNaPjoKKwwVhJdBKLG2G197xDoFzg6GKpAbUvVU4FGzJhi57yeKaJWWFqfwZ', 'attachment': ''}
```

#### Withdraw
Withdraw a certain amount of the token from a token-holding contract instance(e.g. lock contract).

Note that only the token defined in the token-holding contract instance can be withdrawn from it.

```python
import py_vsys as pv

# acnt0: pv.Account
# tc: pv.TokCtrtWithoutSplitV2Whitelist
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
{'type': 9, 'id': '7cu8UgWA17xXpiYFXe6q6LoPcR7ydx12hBJsbrGVJbe2', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646722948926309120, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '5ZkuYBX3YNo3diEbuhogXWSfq35XuVvAAbEtRV6FrZSFzFmqLS9BbH3BKaTXjoHAs8SSTPK5T8WWvkRK5gLETSTb'}], 'contractId': 'CFAqvw8z97XFvbMd5w2xMLi8tAXkXGYKR2x', 'functionIndex': 7, 'functionData': '14WMYfdcm4GTekR7iGMXb4Nv2gcSM5t1ZobHn1yMogSWS55WujjJ7rvXnXq8EmxJ7pX4EGyqMXTrNn7J4yzYgj9M', 'attachment': ''}
```
