# Atomic Swap Contract

- [Atomic Swap Contract](#atomic-swap-contract)
  - [Introduction](#introduction)
  - [Usage with Python SDK](#usage-with-python-sdk)
    - [Registration](#registration)
    - [From Existing Contract](#from-existing-contract)
    - [Querying](#querying)
      - [Maker](#maker)
      - [Token ID](#token-id)
      - [Token Contract Instance](#token-contract-instance)
      - [Unit](#unit)
      - [Contract Balance](#contract-balance)
      - [Swap Owner](#swap-owner)
      - [Swap Recipient](#swap-recipient)
      - [Swap Puzzle](#swap-puzzle)
      - [Swap Amount](#swap-amount)
      - [Swap Expiration Time](#swap-expiration-time)
      - [Swap Status](#swap-status)
    - [Actions](#actions)
      - [Maker Lock](#maker-lock)
      - [Taker Lock](#taker-lock)
      - [Maker Solve](#maker-solve)
      - [Taker Solve](#taker-solve)
      - [Withdraw after expiration](#withdraw-after-expiration)

## Introduction

[Atomic Swap](https://en.bitcoin.it/wiki/Atomic_swap) is a general algorithm to achieve the exchange between two parties without having to trust a third party.

Atomic Swap Contract is the VSYS implementation of [Atomic Swap](https://en.bitcoin.it/wiki/Atomic_swap) which supports atomic-swapping tokens on VSYS chain with other tokens(either on VSYS chain or on other atomic-swap-supporting chain like Ethereum).

## Usage with Python SDK

### Registration
Register an Atomic Swap Contract instance.

```python
import py_vsys as pv

# acnt: pv.Account
# tok_id: str

# Register a new contract instance
nc = await pv.AtomicSwapCtrt.register(by=acnt, tok_id=tok_id)
print(nc.ctrt_id) # print the id of the newly registered contract
```
Example output

```
CtrtID(CFAAxTu44NsfwMUfpmVd6y4vuN9xQNVFtGa)
```

### From Existing Contract
Get an object for an existing contract instance.

```python
import py_vsys as pv

# ch: pv.Chain

ac_id = "CFAAxTu44NsfwMUfpmVd6y4vuN9xQNVFtGa"
ac = pv.AtomicSwapCtrt(ctrt_id=ac_id, chain=ch)
```

### Querying

#### Maker
The address that made this contract instance.

```python
# ac: pv.AtomicSwapCtrt

print(await ac.maker)
```

Example output

```
Addr(AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD)
```

#### Token ID
The token ID of the token deposited into this contract.

```python
# ac: pv.AtomicSwapCtrt

print(await ac.tok_id)
```
Example output

```
TokenID(TWsSkEv5w3Bkb7fhBhUcZr7X69We5ST2GuwmbuMrR)
```

#### Token Contract Instance
The token contract insance object of the token deposited into this contract.

```python
# ac: pv.AtomicSwapCtrt

print(await ac.tok_ctrt)
```
Example output

```
<py_vsys.contract.tok_ctrt.TokCtrtWithoutSplit object at 0x105b8aaa0>
```

#### Unit
The unit of the token deposited into this contract.

```python
# ac: pv.AtomicSwapCtrt

print(await ac.unit)
```
Example output

```
100
```

#### Contract Balance
The balance of the token deposited into this contract for the given user.

```python
# ac: pv.AtomicSwapCtrt
# acnt: pv.Account

print(await ac.get_ctrt_bal(addr=acnt.addr.data))
```
Example output

```
Token(10000)
```

#### Swap Owner
Get the owner of the swap based on the given token-locking transaction ID(e.g. the transaction ID obtained from taking the maker locking action).

```python
# ac: pv.AtomicSwapCtrt
# maker_lock_tx_id: str E.g. "FHZdvf3yyWuDnNTYeR6MZKTEqLJ1QxKfrDBqFrHDVBeJ"

print(await ac.get_swap_owner(maker_lock_tx_id))
```
Example output

```
Addr(AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD)
```

#### Swap Recipient
Get the recipient of the swap based on the given token-locking transaction ID(e.g. the transaction ID obtained from taking the maker locking action).

```python
# ac: pv.AtomicSwapCtrt
# maker_lock_tx_id: str E.g. "FHZdvf3yyWuDnNTYeR6MZKTEqLJ1QxKfrDBqFrHDVBeJ"

print(await ac.get_swap_recipient(maker_lock_tx_id))
```
Example output

```
Addr(AU5NsHE8eC2guo3JobD8jrGvnEDQhBP8GtW)
```

#### Swap Puzzle
Get the hashed puzzle(i.e. secret) of the swap based on the given token-locking transaction ID(e.g. the transaction ID obtained from taking the maker locking action).

```python
# ac: pv.AtomicSwapCtrt
# maker_lock_tx_id: str E.g. "FHZdvf3yyWuDnNTYeR6MZKTEqLJ1QxKfrDBqFrHDVBeJ"

print(await ac.get_swap_puzzle(maker_lock_tx_id))
```
Example output

```
DYu3G8aGTMBW1WrTw76zxQJQU4DHLw9MLyy7peG4LKkY
```

#### Swap Amount
Get the token amount locked into the swap based on the given token-locking transaction ID(e.g. the transaction ID obtained from taking the maker locking action).

```python
# ac: pv.AtomicSwapCtrt
# maker_lock_tx_id: str E.g. "FHZdvf3yyWuDnNTYeR6MZKTEqLJ1QxKfrDBqFrHDVBeJ"

print(await ac.get_swap_amount(maker_lock_tx_id))
```
Example output

```
Token(10000)
```

#### Swap Expiration Time
Get the expiration time of the swap based on the given token-locking transaction ID(e.g. the transaction ID obtained from taking the maker locking action).

```python
# ac: pv.AtomicSwapCtrt
# maker_lock_tx_id: str E.g. "FHZdvf3yyWuDnNTYeR6MZKTEqLJ1QxKfrDBqFrHDVBeJ"

print(await ac.get_swap_expired_time(maker_lock_tx_id))
```
Example output

```
VSYSTimestamp(1646984339000000000)
```

#### Swap Status

Get the status of the swap(if the swap is active) based on the given token-locking transaction ID(e.g. the transaction ID obtained from taking the maker locking action).

```python
# ac: pv.AtomicSwapCtrt
# maker_lock_tx_id: str E.g. "FHZdvf3yyWuDnNTYeR6MZKTEqLJ1QxKfrDBqFrHDVBeJ"

print(await ac.get_swap_status(maker_lock_tx_id))
```
Example output

```
True
```

### Actions

#### Maker Lock
The maker locks tokens into the contract with the recipient, secret, and expiration time specified.

```python
# ac: pv.AtomicSwapCtrt
# maker: pv.Account
# taker: pv.Account

secret = "abc"
two_days_later = int(time.time()) + 86400 * 2

resp = await ac.maker_lock(
    by=maker,
    amount=100,
    recipient=taker.addr.data,
    secret=secret,
    expire_time=two_days_later,
)        
print(resp)
```
Example output

```
{'type': 9, 'id': 'FHZdvf3yyWuDnNTYeR6MZKTEqLJ1QxKfrDBqFrHDVBeJ', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646811541818733056, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '26gn57S3xmf1XVcrhcnmSEp82j6v7sMsskBj1pc8NZt5Gd5jKijkmUwgb52LLsnPepWfj7VH1TurTCcp3GrJSsMf'}], 'contractId': 'CFAAxTu44NsfwMUfpmVd6y4vuN9xQNVFtGa', 'functionIndex': 0, 'functionData': '1CC6B9Tu94MJrtVckkunxuvwR4ixhCVVLeT4ZX9NUBN6KUifUdbuevxsezvw45po5HFnmyFYAchxWVfwG3zAdK5H729k8VxbmehT2pTXJ1T2xKh', 'attachment': ''}
```

#### Taker Lock
The taker locks tokens into the contract after the maker has locked the tokens.

```python
# ac: pv.AtomicSwapCtrt
# maker: pv.Account
# taker: pv.Account
# maker_ac_id: str E.g. "CFAAxTu44NsfwMUfpmVd6y4vuN9xQNVFtGa"
# maker_lock_tx_id: str E.g. "FHZdvf3yyWuDnNTYeR6MZKTEqLJ1QxKfrDBqFrHDVBeJ"

a_day_later = int(time.time()) + 86400

resp = await ac.taker_lock(
    by=taker,
    amount=100,
    maker_swap_ctrt_id=maker_ac_id,
    recipient=maker.addr.data,
    maker_lock_tx_id=maker_lock_tx_id,
    expire_time=a_day_later,
)
print(resp)
```
Example output

```
{'type': 9, 'id': 'D5ZPPhw7y4eWcL6zBNWNHdWf9jGxPAi5XCP5KxuZzirP', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646818399218075904, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '4Z7yUcUqa1TcHMPtp7G6XMjxTKuZWXA2hQWNz7X8XsFZ', 'address': 'AU5NsHE8eC2guo3JobD8jrGvnEDQhBP8GtW', 'signature': '4XMYEJU4LiPzahzS6r9WfM6iaBaBSyQdicgimSgKRStjMPc5e4GYGoapRhpsXw2rL6gbdEYtxA52By4bAsajnBu9'}], 'contractId': 'CF8rnUdzqVczGideBebaLPAa73HEQnxBu8E', 'functionIndex': 0, 'functionData': '1CC6B9Tu94MJrtVckkvwhYn3EkvQmqoxs9Y789QGQ1Xe753PsmJiVZ23HYoZxUzUAdS3Vfc5JB7wWs5wa7oEcanxGqBNfbmJPyjm4mErHCZDiTR', 'attachment': ''}
```

#### Maker Solve
The maker takes the tokens locked by the taker and reveals the plain text of the hashed secret.

```python
# ac: pv.AtomicSwapCtrt
# maker: pv.Account
# taker: pv.Account
# taker_ac_id: str E.g. "CF8rnUdzqVczGideBebaLPAa73HEQnxBu8E"
# taker_lock_tx_id: str E.g. "D5ZPPhw7y4eWcL6zBNWNHdWf9jGxPAi5XCP5KxuZzirP"
# secret: str E.g. "abc"

resp = await ac.maker_solve(
    by=maker,
    taker_ctrt_id=taker_ac_id,
    tx_id=taker_lock_tx_id,
    secret=secret,
)
print(resp)
```
Example output

```
{'type': 9, 'id': 'JsMcYQGcTEFw3LUG3PGUjSRJVvXkb3xcwabHrPzaZXk', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646818867232348928, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': 'B9hWAijnuCZnvEy9wZpvLkUcX9Rerptxma32tgai628Hax9Xyx5TAhJMt7CNP39DYYFrmR4b7RLeukvNrKyXiTq'}], 'contractId': 'CF8rnUdzqVczGideBebaLPAa73HEQnxBu8E', 'functionIndex': 1, 'functionData': '12yhZiQ65kxBjM5KFWFGfsfpKQ9AmFtdWZKYUvT6KZ1kb3XaeW4RZ7XJZp', 'attachment': ''}
```

#### Taker Solve
The taker gets the revealed plain text of hased secret from the maker's solving transaction ID and then takes the tokens locked by the maker.

```python
# ac: pv.AtomicSwapCtrt
# maker: pv.Account
# taker: pv.Account
# maker_ac_id: str E.g. "CFAAxTu44NsfwMUfpmVd6y4vuN9xQNVFtGa"
# maker_lock_tx_id: str E.g. "FHZdvf3yyWuDnNTYeR6MZKTEqLJ1QxKfrDBqFrHDVBeJ"
# maker_solve_tx_id: str E.g. "JsMcYQGcTEFw3LUG3PGUjSRJVvXkb3xcwabHrPzaZXk"

resp = await ac.taker_solve(
    by=taker,
    maker_ctrt_id=maker_ac_id,
    maker_lock_tx_id=maker_lock_tx_id,
    maker_solve_tx_id=maker_solve_tx_id,
)
print(resp)
```
Example output

```
{'type': 9, 'id': 'DJvrQBbFArmqWA9pLpiaM3WkKn4Xr8i9Gaw31T1EooSh', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646819256795354880, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '4Z7yUcUqa1TcHMPtp7G6XMjxTKuZWXA2hQWNz7X8XsFZ', 'address': 'AU5NsHE8eC2guo3JobD8jrGvnEDQhBP8GtW', 'signature': 'V8wH4Co3WSvS3UjQhe3H6PDXTFGXvgg5kcLzfB5fYcZBLzrZFypUYDDgzo4hM8T1mRmbQfjQVBTWVD9znADhKMM'}], 'contractId': 'CFAAxTu44NsfwMUfpmVd6y4vuN9xQNVFtGa', 'functionIndex': 1, 'functionData': '12yhZiUwRpJMDzLKRqEkacsJ5ZcDSHrj9DpHSZ6P4AkTUHYuooPWv1e63L', 'attachment': ''}
```

#### Withdraw after expiration
Either the maker or taker withdraws the tokens from the contract after the expiration time.

The example below shows the withdraw after expiration by the maker. It is the same for the taker.

```python
# ac: pv.AtomicSwapCtrt
# maker_lock_tx_id: str E.g. "FHZdvf3yyWuDnNTYeR6MZKTEqLJ1QxKfrDBqFrHDVBeJ"

resp = await ac.exp_withdraw(
    by=acnt0,
    tx_id=maker_lock_tx_id,
)
print(resp)
```
Example output

```
{'type': 9, 'id': 'FKSpw247kNSNSWyBo3q8c4UwB4w4N8wKyC5wE9wN4rKQ', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646822309320972032, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '28nBpoKFHjdpZzoYzsXaCdMnkBeGXyoaQtjAJqKEpYBMV8iAhQC3Fx58xvsK1vhPPtKnbH9231HHF9gBT5BnFhcu'}], 'contractId': 'CEwifKGjBsE4MXj7FrhVF7ruvYcAuJ3bj3K', 'functionIndex': 2, 'functionData': '1TeCHZdsT9rN5FbvR5Bc5BFuMaGckQ2ags2NPTQq51cw6N4Yt', 'attachment': ''}
```
