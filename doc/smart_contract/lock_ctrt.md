# Lock Contract

- [Lock Contract](#lock-contract)
  - [Introduction](#introduction)
  - [Usage with Python SDK](#usage-with-python-sdk)
    - [Registration](#registration)
    - [From Existing Contract](#from-existing-contract)
    - [Querying](#querying)
      - [Maker](#maker)
      - [Token_id](#Token_id)
      - [Contract balance](#Contract balance)
      - [Lock time](#Lock time)
    - [Actions](#actions)
      - [Lock](#Lock)


## Introduction

Lock contract allows users to lock a specific token in the contract for some period of time. This allows users to guarantee they have a certain amount of funds upon lock expiration. This may be helpful in implementing some kinds of staking interactions with users of a VSYS token for instance.

## Usage with Python SDK

### Registration

`tok_id` is the token id of the token that deposited into this lock contract.

For testing purpose, you can create a new [token contract]() , then [issue]() some tokens and [deposit]() into the lock contract.

```python
import py_v_sdk as pv

# acnt: pv.Account
# tok_id: str

# Register a new Lock contract
nc = await pv.LockCtrt.register(by=acnt,tok_id=tok_id)
print(nc.ctrt_id) # print the id of the newly registered contract
```

Example output

```
CEvsegnqoPWF1e4ATyvmqx5PxDcEy6G6vZa
```

### From Existing Contract

```python
import py_v_sdk as pv

# ch: pv.Chain

nc_id = "CEvsegnqoPWF1e4ATyvmqx5PxDcEy6G6vZa"
nc = pv.LockCtrt(ctrt_id=nc_id, chain=ch)
```

### Querying

#### Maker

The address that made this lock contract instance.

```python
# nc: pv.LockCtrt

print(await nc.maker)
```

Example output

```
Addr(AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu)
```

#### Token id

The token id of the token that deposited into this lock contract.

```python
# nc: pv.LockCtrt

print(await nc.tok_id)
```

Example output

```
TokenID(TWsYWZR551kGnQ7waH2i9mGEfcDS4r5QLn5Z2igyr)
```

#### Contract balance

The token balance within this contract. 

Note that the balance is the same no matter the token is locked or not.

```python
# nc: pv.LockCtrt
# acnt: pv.Account

print(await nc.get_ctrt_bal(addr=acnt.addr.data))
```

Example output

```
Token(200)
```

#### Lock time

The expire timestamp.

```python
# nc: pv.LockCtrt
# acnt: pv.Account

print(await nc.get_ctrt_lock_time(addr=acnt.addr.data))
```

Example output

```
VSYSTimestamp(1646387206000000000)
```

### Actions

#### Lock

Lock the token until the expire time. The token can't be withdrawn before the expire time.

```python
import py_v_sdk as pv

# acnt: pv.Account
# expire_time: int

expire_time = int(time.time())+600 # for 10 mins
resp = await nc.lock(by=acnt,expire_at=expire_time)
print(resp)
```

Example output

```
{'type': 9, 'id': 'DXPuKGAf27AY5t6oc8beSxJyXAE4AsoP7XqWDMdWoVTp', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646386606987950080, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '5zLVSpA9rsoWArCAfpUuxRGyirfRd2s9wv9Rdy2FVNPJRMFoWuAJjkHACnQmVyKoaC7tXYsZjV3KRWFY3BqVVPpj'}], 'contractId': 'CEvsegnqoPWF1e4ATyvmqx5PxDcEy6G6vZa', 'functionIndex': 0, 'functionData': '14Nhwdtu2ifVeF', 'attachment': ''}
```

