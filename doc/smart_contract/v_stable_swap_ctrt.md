# V Stable Swap Contract

- [V Stable Swap Contract](#v-stable-swap-contract)
  - [Introduction](#introduction)
  - [Usage with Python SDK](#usage-with-python-sdk)
    - [Registration](#registration)
    - [From Existing Contract](#from-existing-contract)
    - [Querying](#querying)
      - [Maker](#maker)
      - [Base Token ID](#base-token-id)
      - [Target Token ID](#target-token-id)
      - [Base Token Contract](#base-token-contract)
      - [Target Token Contract](#target-token-contract)
      - [Base Token Unit](#base-token-unit)
      - [Target Token Unit](#target-token-unit)
      - [Max Order Limit Per User](#max-order-limit-per-user)
      - [Unit of Price of Base Token](#unit-of-price-of-base-token)
      - [Unit of Price of Target Token](#unit-of-price-of-target-token)
      - [Base Token Balance](#base-token-balance)
      - [Target Token Balance](#target-token-balance)
      - [User Orders](#user-orders)
      - [Order Owner](#order-owner)
      - [Base Token Fee](#base-token-fee)
      - [Target Token Fee](#target-token-fee)
      - [Base Token Minimum Trading Amount](#base-token-minimum-trading-amount)
      - [Base Token Maximum Trading Amount](#base-token-maximum-trading-amount)
      - [Target Token Minimum Trading Amount](#target-token-minimum-trading-amount)
      - [Target Token Maximum Trading Amount](#target-token-maximum-trading-amount)
      - [Base Token Price](#base-token-price)
      - [Target Token Price](#target-token-price)
      - [Base Token Locked Amount](#base-token-locked-amount)
      - [Target Token Locked Amount](#target-token-locked-amount)
      - [Order Status](#order-status)
    - [Actions](#actions)
      - [Supersede](#supersede)
      - [Set Order](#set-order)
      - [Update Order](#update-order)
      - [Deposit to Order](#deposit-to-order)
      - [Withdraw from Order](#withdraw-from-order)
      - [Close Order](#close-order)
      - [Swap Base Tokens to Target Tokens](#swap-base-tokens-to-target-tokens)
      - [Swap Target Tokens to Base Tokens](#swap-target-tokens-to-base-tokens)

## Introduction
The V Stable Swap contract supports creating a liquidity pool of 2 kinds of tokens for exchange on VSYS. The fee is fixed.

The order created in the contract acts like a liquidity pool for two kinds of tokens(i.e. the base token & the target token). Traders are free to take either side of the trade(i.e. base to target or target to base).

The V Stable Swap contract can accept any type of token in the VSYS blockchain, including option tokens created through the V Option Contract.

## Usage with Python SDK

### Registration
Register a contract instance.

```python
# acnt: pv.Account
# base_tok_id: str E.g. "TWssXmoLvyB3ssAaJiKk5d7ambFHBxcmr9sMRtPLa"
# target_tok_id: str E.g. "TWtoBbmn5UgQd9KgtbWkBY96hiUJWzeTTggGrb8ba"

ssc = await pv.VStableSwapCtrt.register(
    by=acnt,
    base_tok_id=base_tok_id,
    target_tok_id=target_tok_id,
    max_order_per_user=5,
    base_price_unit=1,
    target_price_unit=1,
)         
```
Example output

```
CtrtID(CF4T3EVdaDcu5Y2xMbYKZ1xs1jBsfxGDf29)
```

### From Existing Contract
Get an object for an existing contract instance.

```python
import py_v_sdk as pv

# ch: pv.Chain

ssc_id = "CF4T3EVdaDcu5Y2xMbYKZ1xs1jBsfxGDf29"
ssc = pv.VStableSwapCtrt(ctrt_id=ssc_id, chain=ch)
```

### Querying

#### Maker
The address that made this contract instance.

```python
# ssc: pv.VStableSwapCtrt

print(await ssc.maker)
```

Example output

```
Addr(AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD)
```

#### Base Token ID
The token ID of the base token in the contract instance.

```python
# ssc: pv.VStableSwapCtrt

print(await ssc.base_tok_id)
```
Example output

```
TokenID(TWssXmoLvyB3ssAaJiKk5d7ambFHBxcmr9sMRtPLa)
```

#### Target Token ID
The token ID of the target token in the contract instance.

```python
# ssc: pv.VStableSwapCtrt

print(await ssc.target_tok_id)
```
Example output

```
TokenID(TWtoBbmn5UgQd9KgtbWkBY96hiUJWzeTTggGrb8ba)
```

#### Base Token Contract
The token contract object of the base token in the contract instance.

```python
# ssc: pv.VStableSwapCtrt

print(await ssc.base_tok_ctrt)
```
Example output

```
<py_vsys.contract.tok_ctrt.TokCtrtWithoutSplit object at 0x105aee680>
```

#### Target Token Contract
The token contract object of the target token in the contract instance.

```python
# ssc: pv.VStableSwapCtrt

print(await ssc.target_tok_ctrt)
```
Example output

```
<py_vsys.contract.tok_ctrt.TokCtrtWithoutSplit object at 0x103ea66b0>
```

#### Base Token Unit
The unit of the base token in the contract instance.

```python
# ssc: pv.VStableSwapCtrt

print(await ssc.base_tok_unit)
```
Example output

```
100
```

#### Target Token Unit
The unit of the target token in the contract instance.

```python
# ssc: pv.VStableSwapCtrt

print(await ssc.target_tok_unit)
```
Example output

```
100
```

#### Max Order Limit Per User
The maximum number of orders each user can create.

```python
# ssc: pv.VStableSwapCtrt

print(await ssc.max_order_per_user)
```
Example output

```
5
```

#### Unit of Price of Base Token
The unit of price of base token(i.e. how many target tokens are required to get one base token).

```python
# ssc: pv.VStableSwapCtrt

print(await ssc.base_price_unit)
```
Example output

```
1
```

#### Unit of Price of Target Token
The unit of price of target token(i.e. how many base tokens are required to get one target token).

```python
# ssc: pv.VStableSwapCtrt

print(await ssc.target_price_unit)
```
Example output

```
1
```

#### Base Token Balance
Get the base token balance of the given user.

```python
# ssc: pv.VStableSwapCtrt
# acnt: pv.Account

print(await ssc.get_base_tok_bal(acnt.addr.data))
```
Example output

```
Token(0)
```

#### Target Token Balance
Get the target token balance of the given user.

```python
# ssc: pv.VStableSwapCtrt
# acnt: pv.Account

print(await ssc.get_target_tok_bal(acnt.addr.data))
```
Example output

```
Token(0)
```

#### User Orders
Get the number of orders the user has made.

```python
# ssc: pv.VStableSwapCtrt
# acnt: pv.Account

print(await ssc.get_user_orders(acnt.addr.data))
```
Example output

```
0
```

#### Order Owner
Get the owner of the order.

```python
# ssc: pv.VStableSwapCtrt
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

print(await ssc.get_order_owner(order_id))
```
Example output

```
Addr(AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD)
```

#### Base Token Fee
Get the fee for trading base token in the given order.

```python
# ssc: pv.VStableSwapCtrt
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

print(await ssc.get_fee_base(order_id))
```
Example output

```
Token(100)
```

#### Target Token Fee
Get the fee for trading target token in the given order.

```python
# ssc: pv.VStableSwapCtrt
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

print(await ssc.get_fee_target(order_id))
```
Example output

```
Token(100)
```

#### Base Token Minimum Trading Amount
Get the minimum trading amount for base token in the given order.

```python
# ssc: pv.VStableSwapCtrt
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

print(await ssc.get_min_base(order_id))
```
Example output

```
Token(100)
```

#### Base Token Maximum Trading Amount
Get the maximum trading amount for base token in the given order.

```python
# ssc: pv.VStableSwapCtrt
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

print(await ssc.get_max_base(order_id))
```
Example output

```
Token(200)
```

#### Target Token Minimum Trading Amount
Get the minimum trading amount for target token in the given order.

```python
# ssc: pv.VStableSwapCtrt
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

print(await ssc.get_min_target(order_id))
```
Example output

```
Token(100)
```

#### Target Token Maximum Trading Amount
Get the maximum trading amount for target token in the given order.

```python
# ssc: pv.VStableSwapCtrt
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

print(await ssc.get_max_target(order_id))
```
Example output

```
Token(200)
```

#### Base Token Price
Get the price for base token in the given order.

```python
# ssc: pv.VStableSwapCtrt
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

print(await ssc.get_price_base(order_id))
```
Example output

```
Token(1)
```

#### Target Token Price
Get the price for target token in the given order.

```python
# ssc: pv.VStableSwapCtrt
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

print(await ssc.get_price_target(order_id))
```
Example output

```
Token(1)
```

#### Base Token Locked Amount
Get the locked amount of base token in the given order.

```python
# ssc: pv.VStableSwapCtrt
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

print(await ssc.get_base_tok_locked(order_id))
```
Example output

```
Token(10000)
```

#### Target Token Locked Amount
Get the locked amount of target token in the given order.

```python
# ssc: pv.VStableSwapCtrt
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

print(await ssc.get_target_tok_locked(order_id))
```
Example output

```
Token(10000)
```

#### Order Status
Get the status of the given order(i.e. if the order is active).

```python
# ssc: pv.VStableSwapCtrt
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

print(await ssc.get_order_status(order_id))
```
Example output

```
True
```

### Actions

#### Supersede
Transfer the contract right to another account.

Only the maker of the contract has the right to take this action.

```python
# ssc: pv.VStableSwapCtrt
# acnt0: pv.Account
# acnt1: pv.Account

resp = await ssc.supersede(
    by=acnt0,
    new_owner=acnt1.addr.data,
)
print(resp)
```
Example output

```
{'type': 9, 'id': '999bW989fineZ24ThKoaYxFyQt3WEsfEdXergG7gMCTh', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646897598124136960, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '5sZw4E5bikr36u4uPgVSHsN3fJGqBAwuDusvEyZQZFLqpmrncx3cjTgoBghbrP6oZ4cTzhHcvSnrasZ7H6m1pmHb'}], 'contractId': 'CF4T3EVdaDcu5Y2xMbYKZ1xs1jBsfxGDf29', 'functionIndex': 0, 'functionData': '1bscuEdeiiEkCJsLRbCmpioXRcWMkrs2oDToWe', 'attachment': ''}
```

#### Set Order
Create an order and deposit initial amounts into the order.

The transaction ID returned by this action serves as the order_id.

```python
# ssc: pv.VStableSwapCtrt
# acnt: pv.Account

resp = await ssc.set_order(
    by=acnt,
    fee_base=1,
    fee_target=1,
    min_base=1,
    max_base=2,
    min_target=1,
    max_target=2,
    price_base=1,
    price_target=1,
    base_deposit=100,
    target_deposit=100,
)
print(resp)
```
Example output

```
{'type': 9, 'id': 'JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646896041171938048, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': 'fm9t7RsBkbsAz5uR8UnvijJy13QqyvpYSr7uY5ezvDrifg2SiBHQnsV3SBRgftTkjRWt9ReMYwQUrtAFs8eXm9e'}], 'contractId': 'CF4T3EVdaDcu5Y2xMbYKZ1xs1jBsfxGDf29', 'functionIndex': 1, 'functionData': '17vgyw5jxgmT6gnum2fGA3uMgc6YBPLzZyp3gxn4n1mcNHP2UGNCFtm1pj9WtZYSUMdNyC8NMiQoy5QuXiohc8JZHxAqJkA3CVap4yZYw6X6KuLn6qakp9cdLDsju', 'attachment': ''}
```

#### Update Order
Update the order settings(e.g. fee, price)

```python
# ssc: pv.VStableSwapCtrt
# acnt: pv.Account
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

resp = await ssc.update_order(
    by=acnt,
    order_id=order_id,
    fee_base=1,
    fee_target=1,
    min_base=1,
    max_base=2,
    min_target=1,
    max_target=2,
    price_base=1,
    price_target=1,
)
print(resp)
```
Example output

```
{'type': 9, 'id': '5P15PHApe5UrVB5NVoYjCnyCDP6PzRfiaLtBjd8FF64V', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646898147352104960, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '2DcG3tsBnm8yjzqMhGGFpB8UtmLoVQg2xMzvSEpztkAN7xiMQXUPzGEJyvMy4VKteNin4pDYED3htW5pvMPzf1nG'}], 'contractId': 'CF4T3EVdaDcu5Y2xMbYKZ1xs1jBsfxGDf29', 'functionIndex': 2, 'functionData': '1G3pzCrfkdMYakxGqddXtmmcoJDxvhBGUTX944MZwrb3DUL65TP7dWAAs5XooncuzXZiRebBJDqUBpWsdEcGuTMmSCvF6iBH92xT6s2RFtvvdbrvhnxHS27qqMQ69exGAzCssLCTwf9V3fumJmbR', 'attachment': ''}
```

#### Deposit to Order
Deposit more tokens into the order.

```python
# ssc: pv.VStableSwapCtrt
# acnt: pv.Account
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

resp = await ssc.order_deposit(
    by=acnt,
    order_id=order_id,
    base_deposit=50,
    target_deposit=50,
)
print(resp)
```
Example output

```
{'type': 9, 'id': 'B7uMLxZYH3Td6Hh2ZoNeQ2GDBFUnP19iFjdTkizm8rXH', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646898549264633088, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '4KQ5kfUkpychMpzFjf1yMUxEU1FbZ8xNC7vp97qK9WDShGZvF6c69MNE2P7t7NcJEsFCGNy3Y9Nov3i6yCWcqC9Z'}], 'contractId': 'CF4T3EVdaDcu5Y2xMbYKZ1xs1jBsfxGDf29', 'functionIndex': 3, 'functionData': '1FELDymamTfKj4pKLYEPYbURQJcmrgy8t6zkQ2xsnUEXAaHmNxuFEx59CJDgVPKBofGk22Ww35', 'attachment': ''}
```

#### Withdraw from Order
Withdraw some tokens from the order.

```python
# ssc: pv.VStableSwapCtrt
# acnt: pv.Account
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

resp = await ssc.order_withdraw(
    by=acnt,
    order_id=order_id,
    base_withdraw=50,
    target_withdraw=50,
)
print(resp)
```
Example output

```
{'type': 9, 'id': 'EDt8Enj8SzTaiFJA23aRQ3yRiz6enTKewyGW1hgg42Ez', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646898443957111040, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '2jgdGG8W7PqgBh3QWaCbQfbVa6Y8c7Q3XiYiyDWH7FN3j7CRkTcaB1CUuSztzUi67BzVYmZoJyxYEQhrfG2Z6Z2Y'}], 'contractId': 'CF4T3EVdaDcu5Y2xMbYKZ1xs1jBsfxGDf29', 'functionIndex': 4, 'functionData': '1FELDymamTfKj4pKLYEPYbURQJcmrgy8t6zkQ2xsnUEXAaHmNxuFEx59CJDgVPKBofGk22Ww35', 'attachment': ''}
```

#### Close Order
Close the given order.

```python
# ssc: pv.VStableSwapCtrt
# acnt0: pv.Account
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

resp = await ssc.close_order(
    by=acnt0,
    order_id=order_id,
) 
print(resp)
```
Example output

```
{'type': 9, 'id': '6NE5DG3FStwvAyuup3ose1Sb5D4kxusgbEEto9WSs8dx', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646902167662832896, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '2pA6TN2NUHoixcuTtdtx87APRq1DPUeJQMwJquHpaJv1n6Q7KAUsWcBUqUD7kVTTGd4jk7NNUiL1NHdFHeRn1Vqc'}], 'contractId': 'CF4T3EVdaDcu5Y2xMbYKZ1xs1jBsfxGDf29', 'functionIndex': 5, 'functionData': '1TeCHpSQSfwYX5RxvpEGux8bPxuLbA2EA8M6UvsVYtaDX6XGk', 'attachment': ''}
```

#### Swap Base Tokens to Target Tokens
Trade base tokens for the target tokens.

```python
# ssc: pv.VStableSwapCtrt
# acnt1: pv.Account
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

a_day_later = int(time.time()) + 86400
resp = await ssc.swap_base_to_target(
    by=acnt1,
    order_id=order_id,
    amount=2,
    swap_fee=1,
    price=1,
    deadline=a_day_later,
) 
print(resp)
```
Example output

```
{'type': 9, 'id': 'BrdXjGfg51bQRpfS8q5ZdFfPVh6z1wnYxp1YEpetr12X', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646901807605651968, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '4Z7yUcUqa1TcHMPtp7G6XMjxTKuZWXA2hQWNz7X8XsFZ', 'address': 'AU5NsHE8eC2guo3JobD8jrGvnEDQhBP8GtW', 'signature': '5mT4xrUNtky5eqCow89ZNCQcYjAbLjBCNmh3cGmHLvGZGSSE1smtXSpRWchXxB19TgqBP7fZjEEav1gsG2rhan6J'}], 'contractId': 'CF4T3EVdaDcu5Y2xMbYKZ1xs1jBsfxGDf29', 'functionIndex': 6, 'functionData': '15KQH1wa5mfq3fSkjif5XryFTH1kfby8qFRjUXNXzoiAEvppk5eGYVUYKCX2FCSKEybH7jHgfw4GDsUcecRLAe29aHdm9CqdqMy', 'attachment': ''}
```

#### Swap Target Tokens to Base Tokens
Trade target tokens for the base tokens.

```python
# ssc: pv.VStableSwapCtrt
# acnt1: pv.Account
# order_id: str E.g. "JChwB1yFyFMUjSLCruuTDHVPWHWqvYvQBkFkinnmRmvY"

a_day_later = int(time.time()) + 86400
resp = await ssc.swap_target_to_base(
    by=acnt1,
    order_id=order_id,
    amount=2,
    swap_fee=1,
    price=1,
    deadline=a_day_later,
) 
print(resp)
```
Example output

```
{'type': 9, 'id': 'CaSgv7n6HEVUoHNHBAxMK2CgbU4q9H1ytZB1r697p8Ek', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1646901983609026048, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '4Z7yUcUqa1TcHMPtp7G6XMjxTKuZWXA2hQWNz7X8XsFZ', 'address': 'AU5NsHE8eC2guo3JobD8jrGvnEDQhBP8GtW', 'signature': '4sggSuW3tep11NhBj1HwJckqVB2ZF1oYMjgVVjzTyTkNTY4LhAYLQZ3XZ4kpwchMh7YUJUA5bxP4CtZBsxybpVwd'}], 'contractId': 'CF4T3EVdaDcu5Y2xMbYKZ1xs1jBsfxGDf29', 'functionIndex': 7, 'functionData': '15KQH1wa5mfq3fSkjif5XryFTH1kfby8qFRjUXNXzoiAEvppk5eGYVUYKCX2FCSKEybH7jHgfw4GDsUcecRLAe29aHdmDpz9qcb', 'attachment': ''}
```
