# V Swap Contract

- [Payment Channel Contract](#payment-channel-contract)
  - [Introduction](#introduction)
  - [Usage with Python SDK](#usage-with-python-sdk)
    - [Registration](#registration)
    - [From Existing Contract](#from-existing-contract)
    - [Querying](#querying)
      - [Maker](#maker)
      - [Token A's id](#token-A's-id)
      - [Token B's id](#token-B's-id)
      - [Liquidity token's id](#Liquidity_token's-id)
      - [Swap status](#Swap-status)
      - [Minimum liquidity](#Minimum-liquidity)
      - [Token A reserved](#Token-A-reserved)
      - [Token B reserved](#Token-B-reserved)
      - [Total supply](#Total-supply)
      - [Liquidity token left](#Liquidity-token-left)
      - [Token A's balance](#Token-A's-balance)
      - [Token B's balance](#Token-B's-balance)
      - [Liquidity's balance](#Liquidity's-balance)
    - [Actions](#actions)
      - [Supersede](#Supersede)
      - [Set swap](#Set-swap)
      - [Add Liquidity](#Add-Liquidity)
      - [Remove liquidity](#Remove-liquidity)
      - [Swap token for exact base token](#Swap-token-for-exact-base-token)
      - [Swap exact token for base token](#Swap-exact-token-for-base-token)
      - [Swap token for exact target token](#Swap-token-for-exact-target-token)
      - [Swap exact token for target token](#Swap-exact-token-for-base-token)


## Introduction

V Swap is an automated market making protocol. Prices are regulated by a constant product formula, and requires no action from the liquidity provider to maintain prices.

The contract allows completely decentralised exchanges to be formed, and allows anyone to be a liquidity provider as long as they have tokens on both sides of the swap.

## Usage with Python SDK

### Registration

`tok_id` is the token id of the token that deposited into this V Swap contract.

For testing purpose, you can create a new [token contract]() , then [issue]() some tokens and [deposit]() into the V Swap contract.

```python
import py_vsys as pv

# acnt: pv.Account
# tok_a_id: str
# tok_b_id: str
# liq_tok_id: str
# min_liq: int

# Register a new V Swap contract
nc = await pv.VSwapCtrt.register(by=acnt,tok_a_id=tok_a_id,tok_b_id=tok_b_id,liq_tok_id=liq_tok_id,min_liq=min_liq)
print(nc.ctrt_id) # print the id of the newly registered contract
```

Example output

```
CtrtID(CF5XanD64XpzMZPoaMZ1svYrAriaqsUDeSb)
```

### From Existing Contract

nc_id is the V Swap contract's id.

```python
import py_vsys as pv

# ch: pv.Chain
# nc_id: str

nc_id = "CF5XanD64XpzMZPoaMZ1svYrAriaqsUDeSb"
nc = pv.VSwapCtrt(ctrt_id=nc_id, chain=ch)
```

### Querying

#### Maker

The address that made this V Swap contract instance.

```python
# nc: pv.VSwapCtrt

print(await nc.maker)
```

Example output

```
Addr(AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu)
```

#### Token A's id

The token A's id.

```python
# nc: pv.VSwapCtrt

print(await nc.tok_a_id)
```

Example output

```
TokenID(TWtWBUVbAv4NJrkTZU5hH9HJ5631xXrT398kYdGBm)
```

#### Token B's id

The token B's id.

```python
# nc: pv.VSwapCtrt

print(await nc.tok_b_id)
```

Example output

```
TokenID(TWtKvyVhYPTa1pPberGr4y86iqS2Wt8nLxMCV9Jo8)
```

#### Liquidity token's id

The liquidity token's id.

```python
# nc: pv.VSwapCtrt

print(await nc.liq_tok_id)
```

Example output

```
TokenID(TWu1M1qnhFzoMJFFTjtVjHwo2zHRxeWkmrDGXyq7r)
```

#### Swap status

The swap status of whether or not the swap is currently active. 

```python
# nc: pv.VSwapCtrt
# acnt: pv.Account

print(await nc.is_swap_active)
```

Example output

```
True
```

#### Minimum liquidity

The minimum liquidity for the pool. This liquidity cannot be withdrawn.

```python
# nc: pv.VSwapCtrt

print(await nc.min_liq)
```

Example output

```
Token(100)
```

#### Token A reserved

The amount of token A inside the pool.

```python
# nc: pv.VSwapCtrt

print(await nc.tok_a_reserved)
```

Example output

```
Token(0)
```

#### Token B reserved

the amount of token B inside the pool.

```python
# nc: pv.VSwapCtrt

print(await nc.tok_b_reserved)
```

Example output

```
Token(0)
```

#### Total supply

The total amount of liquidity tokens that can be minted.

```python
# nc: pv.VSwapCtrt

print(await nc.total_liq_tok_supply)
```

Example output

```
Token(300)
```

#### Liquidity token left

The amount of liquidity tokens left to be minted.

```python
# nc: pv.VSwapCtrt
# chan_id: str

print(await nc.get_chan_accum_pay(chan_id=chan_id))
```

Example output

```
Token(100)
```

#### Token A's balance

The balance of token A stored within the contract belonging to the given user address.

```python
# nc: pv.VSwapCtrt
# acnt: pv.Account

print(await nc.get_tok_a_bal(acnt.addr.data))
```

Example output

```
Token(1000)
```

#### Token B's balance

The balance of token B stored within the contract belonging to the given user address.

```python
# nc: pv.VSwapCtrt
# acnt: pv.Account

print(await nc.get_tok_b_bal(acnt.addr.data))
```

Example output

```
Token(1000)
```

#### Liquidity's balance

The balance of liquidity token stored within the contract belonging to the given user address.

```python
# nc: pv.VSwapCtrt
# acnt: pv.Account

print(await nc.get_liq_tok_bal(acnt.addr.data))
```

Example output

```
Token(1000)
```



### Actions

#### Supersede

Transfer the contract rights of the contract to a new account.

```python
import py_vsys as pv

# acnt0: pv.Account
# acnt1: pv.Account

resp = await nc.supersede(by=acnt,new_owner=acnt1.addr.data)
print(resp)
```

Example output

```
{'type': 9, 'id': 'AGLuGRH5K6LVpcUZhhGJLxM8URDTDKMZk8FAjojSaYhx', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646641706708560896, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': 'uMvBdJk863Jdaiej9g3E37gAtusZYwgRKxo5bqRLJ8JuTtUTmqcxGm14KjRhjk8WYNi521Rtm8jJN9pJc6MgoQZ'}], 'contractId': 'CFF4SuQRfkbWzNQx3NdykwZf1kfrZGHwzek', 'functionIndex': 0, 'functionData': '1L43p64yHMPat2p2xM8uoxm9A9aR7BzHvnXFMjafacWNMJBuR3YUPwBKfDLzveK', 'attachment': ''}
```

#### Set swap

Create a swap and deposit initial amounts into the pool.

```python
import py_vsys as pv

# acnt: pv.Account
# amount_a: int | float
# amount_b: int | float

resp = await nc.set_swap(acnt,amount_a=amount_a,amount_b=amount_b)
print(resp)
```

Example output

```
{'type': 9, 'id': 'HkkPF9aZgZPW9zcZuUQMKuaNbCD8XcbdWpkjdnyCC2bj', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646750242564954880, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '4kLMY15QJBfoiSvnCKzA6BRrco2NBA6vPVk5FJ9UmwCJimQ7dfV76PjxpaPMavz8CeRsTYFT25ap92YasJtzaCKD'}], 'contractId': 'CF5XanD64XpzMZPoaMZ1svYrAriaqsUDeSb', 'functionIndex': 1, 'functionData': '1NMvHJqnrtUFrg5Y9jz2PsmaMV', 'attachment': ''}
```

#### Add Liquidity

Adds liquidity to the pool. The final added amount of token A & B will be in the same proportion as the pool at that moment as the liquidity provider shouldn't change the price of the token while the price is determined by the ratio between A & B.

```python
import py_vsys as pv

# acnt: pv.Account
# amount_a: int | float
# amount_b: int | float
# amount_a_min: int | float
# amount_b_min: int | float
# ddl: int

resp = await nc.add_liquidity(acnt,amount_a=amount_a,amount_b=amount_b,amount_a_min=amount_a_min,amount_b_min=amount_b_min,deadline=ddl)
print(resp)
```

Example output

```
{'type': 9, 'id': '9qPbSARZNbRPejXturjFD8oqSMG4Fi5Y99fqHadDX9cw', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646750678165733888, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '3iX53Tom7zBkmC3D5Jv7vbVGZDoxbGLbK6CXLnwLioUV9tEL8Hp95HPP5YZ89ZbTwoFQNarYZfdYEUhuN2EihZ2R'}], 'contractId': 'CF5XanD64XpzMZPoaMZ1svYrAriaqsUDeSb', 'functionIndex': 2, 'functionData': '1YkDihBAK4EBxo5ZQLxHEYePHibL6E3zZwTp3niNCCgSf5uXiFVUxBCcYyAdJUF', 'attachment': ''}
```

#### Remove liquidity

Remove liquidity from the pool by redeeming token A & B with liquidity tokens.

```python
import py_vsys as pv

# acnt: pv.Account
# amount_liq: int | float
# amount_a_min: int | float
# amount_b_min: int | float

resp = await nc.remove_liquidity(by=acnt,amount_liq=amount_liq,amount_a_min=amount_a_min,amount_b_min=amount_b_min)
print(resp)
```

Example output

```
{'type': 9, 'id': '4N3KrtBjcfjhWw17jaQChge28j8K5sBYJ3bBcGa6m1GZ', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646751831698266112, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '3LVKU382LmBNdtNuvBLch6NVDN49w4V4oQuvj2d5VzmEP61HcQVU8JCVuC9Yq91gV8xr52ksUBvYsmYrXYVhC9Dy'}], 'contractId': 'CF5XanD64XpzMZPoaMZ1svYrAriaqsUDeSb', 'functionIndex': 3, 'functionData': '18oJLXPeLXM58Dy52J6Vf6vXv2ThDMNHffq2iLUxWtkAGL1YKeX', 'attachment': ''}
```

#### Swap token for exact base token

Swap token B for token A where the desired amount of token A is fixed.

```python
import py_vsys as pv

# acnt: pv.Account
# amount_a: int | float
# amount_b_max: int | float
# ddl: int

resp = await nc.swap_b_for_exact_a(by=acnt,amount_a=amount_a,amount_b_max=amount_b_max,deadline=ddl)
print(resp)
```

Example output

```
{'type': 9, 'id': 'GyFxdveSBubqSC1ecFqggKMajd5YxJhRgWCVZYmLpdgt', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646751159738810112, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '4yusBVpfWFvJeJDaUp5K61c2rfsVfaQ75kzJyz3GA4a8BrUiFP7Vhh8QMSqFkwM8cN1n16EiKwxHzA4XBpdUuUtY'}], 'contractId': 'CF5XanD64XpzMZPoaMZ1svYrAriaqsUDeSb', 'functionIndex': 4, 'functionData': '12oCrKY2h2JDrHSpggsjRgLgWhBWn6hzfVbqTrX', 'attachment': ''}
```

####  Swap exact token for base token

Swap token B for token A where the amount of token B to pay is fixed.

```python
import py_vsys as pv

# acnt: pv.Account
# amount_a_min: int | float
# amount_b: int | float
# ddl: int

resp = await nc.swap_exact_b_for_a(by=acnt,amount_a_min=amount_a_min,amount_b=amount_b,deadline=ddl)
print(resp)
```

Example output

```
{'type': 9, 'id': 'BwgqHZ16GKotSJLHUDUyRghk7yX8CjTNiXYif3T1pc1t', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646751699139240960, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '242YDuBKjo2x48JMxjMCNKAw2xg6PttQckjTFXZNv97wX5BmvnjHvrBwoFyk5ckopVwLaEGMWXS4h8wxRQbCe2gR'}], 'contractId': 'CF5XanD64XpzMZPoaMZ1svYrAriaqsUDeSb', 'functionIndex': 5, 'functionData': '12oCrKY2h2JDrHSpggsjRgLgWhBWn6hzuhr9shR', 'attachment': ''}
```

#### Swap token for exact target token

Swap token A for token B where the desired amount of token B is fixed.

```python
import py_vsys as pv

# acnt: pv.Account
# amount_b: int | float
# amount_a_max: int | float
# ddl: int

resp = await nc.swap_a_for_exact_b(by=acnt,amount_b=amount_b,amount_a_max=amount_a_max,deadline=ddl)
print(resp)
```

Example output

```
{'type': 9, 'id': 'GP7ve9jRGBbvdVqNE1GFRdmKvSJyXA6LcgUkeBTy22xe', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646751738105092096, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '4uVAaJnCjm1zRpuvtJ5CaiECMSGb8die2EBE5Q47FUPMKyniNoWFjWd1RpzvuRegpWe1v9vTuA8z48mGwxWDf6FV'}], 'contractId': 'CF5XanD64XpzMZPoaMZ1svYrAriaqsUDeSb', 'functionIndex': 6, 'functionData': '12oCrKY2h2JDrHSpggsjRgLgWhBWn6hzvgDiYdu', 'attachment': ''}
```

#### Swap exact token for target token

Swap token B for token B where the amount of token A to pay is fixed.

```python
import py_vsys as pv

# acnt: pv.Account
# amount_b_min: int | float
# amount_a: int | float
# ddl: int

resp = await nc.swap_exact_a_for_b(by=acnt,amount_b_min=amount_b_min,amount_a=amount_a,deadline=ddl)
print(resp)
```

Example output

```
{'type': 9, 'id': '3hUtP18hEDrrhgJC11e6hjrZ37iffKiGi86JG5B2kxFH', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646751751630425088, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '2mQ4hTAc692dLxYB631mN3rbKDGEn1QmWD1dZRaDTt9Vorumo51PLmPX889ngYTmVXeKyGbeGZGsmcGPxfyVn2xb'}], 'contractId': 'CF5XanD64XpzMZPoaMZ1svYrAriaqsUDeSb', 'functionIndex': 7, 'functionData': '12oCrKY2h2JDrHSpggsjRgLgWhBWn6hzw3YrCtF', 'attachment': ''}
```