# V Option Contract

- [V Option Contract](#v-option-contract)
  - [Introduction](#introduction)
  - [Usage with Python SDK](#usage-with-python-sdk)
    - [Registration](#registration)
    - [From Existing Contract](#from-existing-contract)
    - [Querying](#querying)
      - [Maker](#maker)
      - [Base token ID](#base-token-id)
      - [Target token ID](#target-token-id)
      - [Option token ID](#option-token-id)
      - [Proof token ID](#proof-token-id)
      - [Execute time](#execute-time)
      - [Execute deadline](#execute-deadline)
      - [Option status](#option-status)
      - [Max issue num](#max-issue-num)
      - [Reserved option](#reserved-option)
      - [Reserved proof](#reserved-proof)
      - [Price](#price)
      - [Price unit](#price-unit)
      - [Token locked](#token-locked)
      - [Token collected](#token-collected)
      - [Base token balance](#base-token-balance)
      - [Target token balance](#target-token-balance)
      - [Option token balance](#option-token-balance)
      - [Proof token balance](#proof-token-balance)
    - [Actions](#actions)
      - [Supersede](#supersede)
      - [Activate](#activate)
      - [Mint](#mint)
      - [Unlock](#unlock)
      - [Execute](#execute)
      - [Collect](#collect)

## Introduction

[Option contract](https://en.wikipedia.org/wiki/Option_contract) is defined as "a promise which meets the requirements for the formation of a contract and limits the promisor's power to revoke an offer".

Option Contract in VSYS provides an opportunity for the interested parties to buy or sell a VSYS underlying asset based on the determined agreement(e.g., pre-determined price, execute timestamp and so on). It allows users to create option tokens on the VSYS blockchain, and buyers holding these option tokens have the right to buy or sell some underlying asset at some point in the future. Different from the traditional option market, everyone can buy or sell option tokens to join the option market at any time without any contractual relationship with an exchange.

## Usage with Python SDK

### Registration

Register an V Option Contract instance.

```python
import py_v_sdk as pv

# acnt: pv.Account
# base_tok_id: str
# target_tok_id: str
# option_tok_id: str
# proof_tok_id: str
# exe_time: int
# exe_ddl: int

# Register a new contract instance
nc = await pv.VOptionCtrt.register(by=acnt, base_tok_id=base_tok_id,target_tok_id=target_tok_id,option_tok_id=option_tok_id,proof_tok_id=proof_tok_id,execute_time=exe_time,execute_deadline=exe_ddl)
print(nc.ctrt_id) # print the id of the newly registered contract
```

Example output

```
CtrtID(CEyb8Q7A1kQw62vem1Jz5gmQFVrK28iny9b)
```

### From Existing Contract

Get an object for an existing contract instance.

```python
import py_v_sdk as pv

# ch: pv.Chain

ac_id = "CFAAxTu44NsfwMUfpmVd6y4vuN9xQNVFtGa"
ac = pv.VOptionCtrt(ctrt_id=ac_id, chain=ch)
```

### Querying

#### Maker

The address that made this contract instance.

```python
# ac: pv.VOptionCtrt

print(await ac.maker)
```

Example output

```
Addr(AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu)
```

#### Base token ID

The base token ID.

```python
# ac: pv.VOptionCtrt

print(await ac.base_token_id)
```

Example output

```
TokenID(TWuWjii3qajEFXMBVot25Bhmnt7bK2njHFnZTYLQo)
```

#### Target token ID

The target token ID.

```python
# ac: pv.VOptionCtrt

print(await ac.target_token_id)
```

Example output

```
TokenID(TWsnKQT4z2BrmZVZYgPzBzbH6oroZR8Leow8JL7wz)
```

#### Option token ID

The option token ID.

```python
# ac: pv.VOptionCtrt

print(await ac.option_token_id)
```

Example output

```
TokenID(TWsne6ivnYPgy2oP87vbHKfxMzTu1umRD4wq8B93k)
```

#### Proof token ID

The proof token ID.

```python
# ac: pv.VOptionCtrt

print(await ac.proof_token_id)
```

Example output

```
TokenID(TWuVbHKomdtKFSyDTN3XhfX7qrQSt8ssLZVe3boVN)
```

#### Execute time

The execute time.

```python
# ac: pv.VOptionCtrt

print(await ac.execute_time)
```

Example output

```
VSYSTimestamp(1646898300000000000)
```

#### Execute deadline

The execute deadline.

```python
# ac: pv.VOptionCtrt

print(await ac.execute_deadline)
```

Example output

```
VSYSTimestamp(1646899200000000000)
```

#### Option status

The option contract's status.(check if it is still alive)

```python
# ac: pv.VOptionCtrt

print(await ac.option_status)
```

Example output

```
true
```

#### Max issue num

The maximum issue of the option tokens.

```python
# ac: pv.VOptionCtrt

print(await ac.max_issue_num)
```

Example output

```
Token(1000)
```

#### Reserved option

The reserved option tokens remaining in the pool.

```python
# ac: pv.VOptionCtrt

print(await ac.reserved_option)
```

Example output

```
Token(900)
```

#### Reserved proof

The reserved proof tokens remaining in the pool.

```python
# ac: pv.VOptionCtrt

print(await ac.reserved_proof)
```

Example output

```
Token(900)
```

#### Price

The price of the contract creator.

```python
# ac: pv.VOptionCtrt

print(await ac.price)
```

Example output

```
Token(10)
```



#### Price unit

The price unit of the contract creator.

```python
# ac: pv.VOptionCtrt

print(await ac.price_unit)
```

Example output

```
Token(1)
```

#### Token locked

The locked token amount.

```python
# ac: pv.VOptionCtrt

print(await ac.token_locked)
```

Example output

```
Token(100)
```

#### Token collected

The amount of the base tokens in the pool.

```python
# ac: pv.VOptionCtrt

print(await ac.token_collected)
```

Example output

```
Token(100)
```

#### Base token balance

Get the balance of the available base tokens.

```python
# ac: pv.VOptionCtrt
# addr: str

print(await ac.get_base_tok_bal(addr))
```

Example output

```
Token(1000)
```

#### Target token balance

Get the balance of the available target tokens.

```python
# ac: pv.VOptionCtrt
# addr: str

print(await ac.get_target_tok_bal(addr))
```

Example output

```
Token(1000)
```

#### Option token balance

Get the balance of the available option tokens.

```python
# ac: pv.VOptionCtrt
# addr: str

print(await ac.get_option_tok_bal(addr))
```

Example output

```
Token(1000)
```

#### Proof token balance

Get the balance of the available proof tokens.

```python
# ac: pv.VOptionCtrt
# addr: str

print(await ac.get_proof_tok_bal(addr))
```

Example output

```
Token(1000)
```



### Actions

#### Supersede

Transfer the ownership of the contract to another account.

```python
# acnt: pv.Account
# new_owner: str

resp = await ac.supersede(
    by=acnt,
    new_owner=new_owner
)        
print(resp)
```

Example output

```
{'type': 9, 'id': 'FHZdvf3yyWuDnNTYeR6MZKTEqLJ1QxKfrDBqFrHDVBeJ', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646811541818733056, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '26gn57S3xmf1XVcrhcnmSEp82j6v7sMsskBj1pc8NZt5Gd5jKijkmUwgb52LLsnPepWfj7VH1TurTCcp3GrJSsMf'}], 'contractId': 'CFAAxTu44NsfwMUfpmVd6y4vuN9xQNVFtGa', 'functionIndex': 0, 'functionData': '1CC6B9Tu94MJrtVckkunxuvwR4ixhCVVLeT4ZX9NUBN6KUifUdbuevxsezvw45po5HFnmyFYAchxWVfwG3zAdK5H729k8VxbmehT2pTXJ1T2xKh', 'attachment': ''}
```

#### Activate

Activate the V Option contract to store option token and proof token into the pool.

```python
# ac: pv.VOptionCtrt
# max_issue_num: int | float
# price: int | float
# price_unit: int | float

resp = await ac.activate(
    by=taker,
    max_issue_num=max_issue_num,
  	price=price,
    price_unit=price_unit
)
print(resp)
```

Example output

```
{'type': 9, 'id': 'GSvfYox5vLADXAUYyu5Bm3VUKjyDwGvme2TBzDbSFfgS', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646897374037286912, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '3QzPAmP2yLqX1xaoFnYKMapPYgMHbB2Dsd3HFhgKyu5tZSbxmVuFqK9vxRZ1Aq4w3oDNwRWWrE3VvkcSQ1N8c29H'}], 'contractId': 'CEyb8Q7A1kQw62vem1Jz5gmQFVrK28iny9b', 'functionIndex': 1, 'functionData': '12oCrKY2h2JDu8D8RTzEMDhUcrQ8dYoVQvjhPd2', 'attachment': ''}
```

#### Mint

Mint target tokens into the pool to get option tokens and proof tokens.

```python
# acnt: pv.Account
# amount: int | float

resp = await ac.mint(
    by=acnt,
  	amount=amount
)
print(resp)
```

Example output

```
{'type': 9, 'id': 'AAnv8tdQfPvnuqxnbk7WvbvuRm4qZrLcaL9KMRbYLoPi', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646897448154491904, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '2KRogFF3Ws2govyDWN2CEEdPm7XQ7Mr83E4TTNz5kMomPtB36p1atnr9H96gduSKUTJSZS83Z8idywmrKbTTDcV8'}], 'contractId': 'CEyb8Q7A1kQw62vem1Jz5gmQFVrK28iny9b', 'functionIndex': 2, 'functionData': '14JDCrdo1xwsuu', 'attachment': ''}
```

#### Unlock

Get the remaining option tokens and proof tokens from the pool before the execute time.

```python
# acnt: pv.Account
# amount: int | float

resp = await ac.unlock(
    by=acnt,
  	amount=amount
)
print(resp)
```

Example output

```
{'type': 9, 'id': '8PAsLgoAtFrn2kV3BTeoACyFW51vnFGNbEe97G6AhrjT', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646897501076599040, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '4Vjg1mDE7TwPn4VmP4DN8cRjnUciRU6iLbV3vG7BNYc8Z5LtCExs2TtTvJBP2axEkwtBAaqdqgtNWmDrNQbY1h3B'}], 'contractId': 'CEyb8Q7A1kQw62vem1Jz5gmQFVrK28iny9b', 'functionIndex': 3, 'functionData': '14JDCrdo1xwsuu', 'attachment': ''}
```

#### Execute

Execute the V Option contract to get target token after execute time.

```python
# acnt: pv.Account
# amount: int | float

resp = await ac.execute(
    by=acnt,
  	amount=amount
)
print(resp)
```

Example output

```
{'type': 9, 'id': '6RyJ3reSorSmP6QuoS3A2p4tPJg7AAxKMcZqfvC7CnwM', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646898377867204096, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '5zW6HWiSHGePiSTpN53mfUKqJNo8XTjXjkXsyBXGNtH8wh9mSMzKbZiryTuf6vE6zvc1QnoszkaHGGhH4JxoShus'}], 'contractId': 'CEyb8Q7A1kQw62vem1Jz5gmQFVrK28iny9b', 'functionIndex': 4, 'functionData': '14JDCrdo1xwstM', 'attachment': ''}
```

#### Collect

Collect the base tokens or/and target tokens from the pool depending on the amount of proof tokens after execute deadline.

```python
# acnt: pv.Account
# amount: int | float

resp = await ac.collect(
    by=acnt,
  	amount=amount
)
print(resp)
```

Example output

```
{'type': 9, 'id': 'D3KUN1JnteKE6vdqzSzg9xJUNDXDE7AUFyZ7vmqHoQvT', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646898410086354944, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': 'XbmHoY36np9aRU9iZnSPpH4BZbSrtEBwof2uunRAGMcqnBiXo5zohX85sQxgtgi12SagJjpzaoXjyn3ZXCdSnH7'}], 'contractId': 'CEyb8Q7A1kQw62vem1Jz5gmQFVrK28iny9b', 'functionIndex': 5, 'functionData': '14JDCrdo1xwsuu', 'attachment': ''}
```

