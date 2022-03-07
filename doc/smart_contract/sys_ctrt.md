# System Contract

- [System Contract](#system-contract)
  - [Introduction](#introduction)
  - [Usage with Python SDK](#usage-with-python-sdk)
    - [Registration](#registration)
    - [Actions](#actions)
      - [Send](#send)
      - [Deposit](#deposit)
      - [Withdraw](#withdraw)
      - [Transfer](#transfer)


## Introduction

The System Contract on V Systems is quite unique in that it is directly included in the protocol and not registered by users. Since Contract variables and VSYS tokens use different databases, it is normally not possible for them to interact. However, the System Contract handles the mixing of these two databases, and allows users to do things such as deposit and withdraw VSYS token from contracts. 

## Usage with Python SDK

### Registration

```python
import py_vsys as pv

# acnt: pv.Account
# ch: pv.chain

# initial a new system contract on mainnet
# nc = pv.SysCtrt(ctrt_id="CCL1QGBqPAaFjYiA8NMGVhzkd3nJkGeKYBq")

# initial a new system contract on mainnet
nc = pv.SysCtrt(ctrt_id="CF9Nd9wvQ8qVsGk8jYHbj6sf8TK7MJ2GYgt",chain=ch)

print(nc.ctrt_id) # print the id of the system contract
```

Example output

```
CtrtID(CF9Nd9wvQ8qVsGk8jYHbj6sf8TK7MJ2GYgt)
```

### Actions

#### Send

Send VSYS tokens to another user.

```python
import py_vsys as pv

# acnt0: pv.Account
# acnt1: pv.Account
# amount: int | float

resp = await nc.send(
  by=acnt0,
  recipient=acnt1.addr.data,
  amount=amount,
)
print(resp)
```

Example output

```
{'type': 9, 'id': '7HEXZgYN65qHgCVNqbk8YAVyERuMEMFbWpVyyrav9nz7', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646663415956263936, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '313qGjzy6ef7QCYgcb6iqDJw7nH5Ka6Y4TiZAFshqW5oXh1UahSwzVwdV94fRneRWWodcyRHqDLWmznN4KND6iPc'}], 'contractId': 'CF9Nd9wvQ8qVsGk8jYHbj6sf8TK7MJ2GYgt', 'functionIndex': 0, 'functionData': '14uNyPF7CkATaDAHf91Jg5fmdnSKRfTghAY2BworyQ1Q62Z6fa7', 'attachment': ''}
```

#### Deposit

Deposit VSYS tokens to a token-holding contract instance(e.g. lock contract).

Note that only the token defined in the token-holding contract instance can be deposited into it.

```python
import py_vsys as pv

# acnt0: pv.Account
# nc: pv.SysCtrt
# lc: pv.LockCtrt
# amount: int | float

lc_id = lc.ctrt_id.data

resp = await nc.deposit(
    by=acnt0,
    ctrt_id=lc_id,
    amount=amount
)
print(resp)
```

Example output

```
{'type': 9, 'id': '7DxP86FzXEDxNqiNhQkehL51GXSyoeRGYH5YSHshh1ga', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646663600529510912, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '3uaoJmeUdoPGuyqAbVjt3ASbcknNMfz15XKR4ZW3UH9Hds3hj7vygsdiYVMRoYp3orp3ptvVFepX2wcisgLtZHeS'}], 'contractId': 'CF9Nd9wvQ8qVsGk8jYHbj6sf8TK7MJ2GYgt', 'functionIndex': 1, 'functionData': '14VJY1ZP9F8AxnTMyoWJiGRvyvgT7cKTmLDrGJJp1VtHTAWRFTDHsGqz5YaSHFiE33y1QtrPZwSTz5PKzi6xyv7Z', 'attachment': ''}
```

#### Withdraw

Withdraw VSYS tokens from a token-holding contract instance(e.g. lock contract).

Note that only the one who deposits the token can withdraw.

```python
import py_vsys as pv

# acnt0: pv.Account
# nc: pv.SysCtrt
# lc: pv.LockCtrt
# amount: int | float

lc_id = lc.ctrt_id.data

resp = await nc.withdraw(
    by=acnt0,
    ctrt_id=lc_id,
    amount=amount
)
print(resp)
```

Example output

```
{'type': 9, 'id': 'EF6Brq21Wi1Hv3N4z2BuVNRNfeXjb9uzv2HBVS8voRqG', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646295771726907904, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '4bEfdwPrwNzGkdLjP7JSvg2xdDnbPabtGK3fdGampaF9LySUHtsMJrD3V35F7C9zwgBrvMhEZfTfEB7iyY7SGquM'}], 'contractId': 'CEu8AuKJS2Pr67RPV9dFjPAb8TL151weQsi', 'functionIndex': 5, 'functionData': '1Y5SeLwhk5NvqLEeqZuAFHiVY6k713zijrRcTwsgJDd7gGwi9dxZpZCyGMqUWZJovQUcDw6MBsnz1AKygj', 'attachment': ''}
```

#### Transfer

Transfer the VSYS token to another account(e.g. user or contract).
`transfer` is the underlying action of `send`, `deposit`, and `withdraw`. It is not recommended to use transfer directly. Use `send`, `deposit`, `withdraw` instead when possible.

```python
import py_vsys as pv

# acnt0: pv.Account
# acnt1: pv.Account
# nc: pv.SysCtrt
# amount: int | float

resp = await nc.transfer(
  by=acnt1,
  sender=acnt1.addr.data,
  recipient=acnt0.addr.data,
  amount=amount
)
print(resp)
```

Example output

```
{'type': 9, 'id': 'CG8R8vsMFvVBdZaDKAWC9ZdTzoxvSf98raiXzUF9e3Vi', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646664197690723072, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '3b3bu31esBWgeQyFfUeYmPwPUhQpPtVJehuRpreM5pMY', 'address': 'AUCzwTg7EjGoa68nRy27873LY5LtvKmQy2H', 'signature': '51pQJhidvosvV6nDu9M2heLFjUBw3H4ihtLV69diCDgXu9cRNWbo6RxcVwxeyGJi5KdtUzPASCTCvC4FgPQvjuoA'}], 'contractId': 'CF9Nd9wvQ8qVsGk8jYHbj6sf8TK7MJ2GYgt', 'functionIndex': 3, 'functionData': '14VJY1hkohabHWAB2nkk7fwuzSiTZZq4Mk2DpK8K753q4ByccYRThsV7dTPmNSWnSHMGK6yTuKtfoThrZniwf23y', 'attachment': ''}
```

#### 