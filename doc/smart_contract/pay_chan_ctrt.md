# Payment Channel Contract

- [Payment Channel Contract](#payment-channel-contract)
  - [Introduction](#introduction)
  - [Usage with Python SDK](#usage-with-python-sdk)
    - [Registration](#registration)
    - [From Existing Contract](#from-existing-contract)
    - [Querying](#querying)
      - [Maker](#maker)
      - [Token id](#token-id)
      - [Contract balance](#contract-balance)
      - [channel creator](#channel-creator)
      - [channel creator's public key](#channel-creator's-public-key)
      - [channel recipient](#channel-recipient)
      - [channel accumulated load](#channel-accumulated-load)
      - [channel accumulated payment](#channel-accumulated-payment)
      - [channel expiration time](#channel-expiration-time)
      - [channel status](#channel-status)
    - [Actions](#actions)
      - [Create and load](#create-and-load)
      - [extend expiration time](#extend-expiration-time)
      - [load](#load)
      - [abort](#abort)
      - [unload](#unload)
      - [collect payment](#collect-payment)
      - [generate the signature for off chain payments](#generate-the-signature-for-off-chain-payments)
      - [verify the signature](#verify-the-signature)


## Introduction

Payment Channels have been implemented in a large number of blockchains as a method to increase the scalability of any protocol. By taking a large number of the transactions between two parties off-chain, it can significantly reduce the time and money cost of transactions.

The payment channel contract in VSYS is a one-way payment channel, which means that the paying user is considered as `sender` and the receiving user is `receiver`.

## Usage with Python SDK

### Registration

`tok_id` is the token id of the token that deposited into this payment channel contract.

For testing purpose, you can create a new [token contract]() , then [issue]() some tokens and [deposit]() into the payment channel contract.

```python
import py_v_sdk as pv

# acnt: pv.Account
# tok_id: str

# Register a new Payment Channel contract
nc = await pv.PayChanCtrt.register(by=acnt,tok_id=tok_id)
print(nc.ctrt_id) # print the id of the newly registered contract
```

Example output

```
CtrtID(CFF4SuQRfkbWzNQx3NdykwZf1kfrZGHwzek)
```

### From Existing Contract

nc_id is the payment channel contract's id.

```python
import py_v_sdk as pv

# ch: pv.Chain
# nc_id: str

nc_id = "CFF4SuQRfkbWzNQx3NdykwZf1kfrZGHwzek"
nc = pv.PayChanCtrt(ctrt_id=nc_id, chain=ch)
```

### Querying

#### Maker

The address that made this payment channel contract instance.

```python
# nc: pv.PayChanCtrt

print(await nc.maker)
```

Example output

```
Addr(AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu)
```

#### Token id

The token id of the token that deposited into this payment channel contract.

```python
# nc: pv.PayChanCtrt

print(await nc.tok_id)
```

Example output

```
TokenID(TWuf34jWfwQGyvqo1LeQjBHsiGcKqEmFKkNhTNb69)
```

#### Contract balance

The token balance within this contract. 

```python
# nc: pv.PayChanCtrt
# acnt: pv.Account

print(await nc.get_ctrt_bal(addr=acnt.addr.data))
```

Example output

```
Token(300)
```

#### Channel creator

The channel creator.

```python
# nc: pv.PayChanCtrt
# chan_id: str

print(await nc.get_chan_creator(chan_id=chan_id))
```

Example output

```
VSYSTimestamp(1646387206000000000)
```

#### Channel creator's public key

The channel creator's public key.

```python
# nc: pv.PayChanCtrt
# chan_id: str

print(await nc.get_chan_creator_pub_key(chan_id=chan_id))
```

Example output

```
PubKey(AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot)
```

#### Channel recipient

The recipient of the channel.

```python
# nc: pv.PayChanCtrt
# chan_id: str

print(await nc.get_chan_recipient(chan_id=chan_id))
```

Example output

```
Addr(AUCzwTg7EjGoa68nRy27873LY5LtvKmQy2H)
```

#### Channel accumulated load

The accumulated load of the channel.

```python
# nc: pv.PayChanCtrt
# chan_id: str

print(await nc.get_chan_accum_load(chan_id=chan_id))
```

Example output

```
Token(300)
```

#### Channel accumulated payment

The  accumulated payment of the channel.

```python
# nc: pv.PayChanCtrt
# chan_id: str

print(await nc.get_chan_accum_pay(chan_id=chan_id))
```

Example output

```
Token(200)
```

#### Channel expiration time

The expiration time of the channel.

```python
# nc: pv.PayChanCtrt
# chan_id: str

print(await nc.get_chan_exp_time(chan_id=chan_id))
```

Example output

```
VSYSTimestamp(1646388206000000000)
```

#### Channel status

The channel status.(check if the channel is still alive)

```python
# nc: pv.PayChanCtrt
# chan_id: str

print(await nc.get_chan_status(chan_id=chan_id))
```

Example output

```
True
```



### Actions

#### Create and load

Create the payment channel and loads an amount into it.

Note that this transaction id is the channel id.

```python
import py_v_sdk as pv

# acnt: pv.Account
# receipt: str
# amount: Union[int,float]
# expired_time: int

resp = await nc.create_and_load(by=acnt,recipient=recipient,amount=amount,expire_at=expired_time)
print(resp)
```

Example output

```
{'type': 9, 'id': 'AGLuGRH5K6LVpcUZhhGJLxM8URDTDKMZk8FAjojSaYhx', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646641706708560896, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': 'uMvBdJk863Jdaiej9g3E37gAtusZYwgRKxo5bqRLJ8JuTtUTmqcxGm14KjRhjk8WYNi521Rtm8jJN9pJc6MgoQZ'}], 'contractId': 'CFF4SuQRfkbWzNQx3NdykwZf1kfrZGHwzek', 'functionIndex': 0, 'functionData': '1L43p64yHMPat2p2xM8uoxm9A9aR7BzHvnXFMjafacWNMJBuR3YUPwBKfDLzveK', 'attachment': ''}
```

#### Extend expiration time

Extend the expiration time of the channel to the new input timestamp.

```python
import py_v_sdk as pv

# acnt: pv.Account
# chan_id: str
# expired_time: int

resp = await nc.extend_exp_time(by=acnt,chan_id=chan_id,expire_at=expired_time)
print(resp)
```

Example output

```
{'type': 9, 'id': '8N26vnjUHXtpcLFZNoucmET9NQot3z5tU6pdxt4iD3Kn', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646658977262811904, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '5dXguDMnAKJ6d5ugJzRzgkoTtTATaGS1LmLYQLjTK1mV6z3HXDrZnSF1XhjJH53heumh4Kbxq6BVPX9y6CmnWdV9'}], 'contractId': 'CFF4SuQRfkbWzNQx3NdykwZf1kfrZGHwzek', 'functionIndex': 1, 'functionData': '13w3j8QMzeBg98nBdVyxoh6aDnahzCE3iskT4zBBCkLhA5TeVZXssugQ7Aggym', 'attachment': ''}
```

#### Load

Load more tokens into the channel.

```python
import py_v_sdk as pv

# acnt: pv.Account
# chan_id: str
# amount: Union[int,float]

resp = await nc.load(by=acnt,chan_id=chan_id,amount=amount)
print(resp)
```

Example output

```
{'type': 9, 'id': 'CLSkJwqfKq8PTwXnyMqhMod7fedBjXRU6jTEdc5zghSh', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646659010501829888, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '2uUj2RzuYwaRNuLK9wQURxKhyAgqK7GbqkmML3yKox9ZrtFN4CBftbWA6DvGxcZkxAfPPyVd63RX77gFGTr1Kcmy'}], 'contractId': 'CFF4SuQRfkbWzNQx3NdykwZf1kfrZGHwzek', 'functionIndex': 2, 'functionData': '13w3j8QMzeBg98nBdVyxoh6aDnahzCE3iskT4zBBCkLhA5TeVZTP96HfcGSe5H', 'attachment': ''}
```

#### Abort

Abort the channel, triggering a 2-day grace period where the recipient can still collect payments. After 2 days, the payer can unload all the remaining funds that was locked in the channel.

```python
import py_v_sdk as pv

# acnt: pv.Account
# chan_id: str

resp = await nc.abort(by=acnt,chan_id=chan_id)
print(resp)
```

Example output

```
{'type': 9, 'id': 'CtuWHyQc7NswFVfAVkVeR3vucYY6nxBXsiLCdShybyUo', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646661785957097984, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '2ShNWoDJg5CrKk6WGGvmk5iFMuP3xF6rYS5qC46rnJi52tvT9fuWHzSxEFzGsSTrsvaeZa4Hkcs5ESLQRM6nMpJ1'}], 'contractId': 'CFF4SuQRfkbWzNQx3NdykwZf1kfrZGHwzek', 'functionIndex': 3, 'functionData': '1TeCHgW3QmLrLRGwwuQRGnuxF6aCL89vmR7XeVFUxubACFJ4A', 'attachment': ''}
```

#### Unload

Unload all the funcs locked in the channel (only works if the channel has expired).

```python
import py_v_sdk as pv

# acnt: pv.Account
# chan_id: str

resp = await nc.unload(by=acnt,chan_id=chan_id)
print(resp)
```

Example output

```
{'type': 9, 'id': '5AMVPv6mhaWSmRPb9iYGoufREtFggrbmXEKSPNgEZ2B5', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646660540282042880, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': 'NDL3j3yXPXrUyogryxb4XAo2GvK7th6NsSz7FUyq4TiCK28zsMiNcUqwYuWTTRdPqcSzhoPM8xjZAuEmchHnJZR'}], 'contractId': 'CFF4SuQRfkbWzNQx3NdykwZf1kfrZGHwzek', 'functionIndex': 4, 'functionData': '1TeCHgW3QmLrLRGwwuQRGnuxF6aCL89vmR7XeVFUxubACFJ4A', 'attachment': ''}
```

#### Collect payment

Collect the payment from the channel (only works if the channel has expired).

```python
import py_v_sdk as pv

# acnt: pv.Account
# chan_id: str
# amount: Union[int,float]
# signature: str

resp = await nc.collect_payment(by=acnt,chan_id=chan_id,amount=amount,signature=signature)
print(resp)
```

Example output

```
{'type': 9, 'id': 'Cvoga5EYH7XEetKW972TkY2hPrhUAKfSrqsWRwEgY3bw', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646660721929943040, 'proofs': [{'proofType': 'Curve25519', 'publicKey': 'AGy4ASY2CmVPSjQX4rNHrSHmcYAL4DNBawdyKT7p8vot', 'address': 'AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu', 'signature': '2FvBPw9gHSEk2wVdWVL1cNoUcdF79mwEavqcnQDtUmihf5d78wumJkTAsRyKc6CXuAswC9sFPwFyppiQgHGfs3FB'}], 'contractId': 'CFF4SuQRfkbWzNQx3NdykwZf1kfrZGHwzek', 'functionIndex': 5, 'functionData': '1a8vFbntDanX1XowEXaTicnG3JdfcjbrUoEiCdxX8Yceqpo8eZ44WazR1yK1MnjZaQJ5GfJiyu53ZdRaWPGCXij87buUM3cKNswKswiRgmgCPGaHV6pa2ZE2G8BfTFZa1kurQUyVTJqMiTry2VmZFnBvq', 'attachment': ''}
```

#### Generate the signature for off chain payments

Generate the offchain payment signature.

```python
import py_v_sdk as pv

# key_pair: md.KeyPair
# chan_id: str
# amount: Union[int,float]

resp = await nc.offchain_pay(key_pair=key_pair,chan_id=chan_id,amount=amount)
print(resp)
```

Example output

```
2NreuGDAcLCfUnUkCMny9NSHJguWKQPZTZusxHP4uDyDfo9xBAGB2EuQ975KtHgzJGCAqWa1E1APnMJwbbfY6SmF
```

#### Verify the signature

Verify the payment signature.

```python
import py_v_sdk as pv

# chan_id: str
# amount: Union[int,float]
# signature: str

resp = await nc.verify_sig(chan_id=chan_id,amount=amount,signature=signature)
print(resp)
```

Example output

```
True
```
