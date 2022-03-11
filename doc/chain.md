# Chain

- [Chain](#chain)
  - [Introduction](#introduction)
  - [Usage with Python SDK](#usage-with-python-sdk)
    - [Properties](#properties)
      - [Api](#api)
      - [Chain ID](#chain-id)
      - [Height](#height)
      - [Last block](#last-block)
    - [Actions](#actions)
      - [Get the Block at a Certain Height](#get-the-block-at-a-certain-height)
      - [Get Blocks within a Certain Range](#get-blocks-within-a-certain-range)

## Introduction
Chain is a logical concept that represents the abstract data structure where transactions are packed into a block and blcoks are chained together by including the hash from the last block.

In VSYS, there are 2 types of chains:
- mainnet
- testnet

They have different chain IDs, namely `M` for mainnet & `T` for testnet, which will be used in cases like the address of an account. 

In other words, the same pair of seed and nonce will lead to different account addresses on mainnet & testnet.

## Usage with Python SDK
In Python SDK we have an `Chain` class that represents the chain.

### Properties

#### Api
The `NodeAPI` object that serves as the API wrapper for calling RESTful APIs that exposed by a node in the VSYS blockchain.

```python
import py_vsys as pv

# ch: pv.Chain
print(ch.api)
```
Example output

```
<py_vsys.api.NodeAPI object at 0x1027c1b10>
```

#### Chain ID
The chain ID.

```python
import py_vsys as pv

# ch: pv.Chain
print(ch.chain_id)
```
Example output

```
ChainID.TEST_NET
```

#### Height
The current height of blocks on the chain.

Note that it is queried by calling RESTful APIs of a node. Technically speaking, the result is of the node. It can be used as of the chain as long as the node synchronises with other nodes well.

```python
import py_vsys as pv

# ch: pv.Chain
print(await ch.height)
```
Example output

```
1355645
```

#### Last block
The last block on the chain.

Note that it is queried by calling RESTful APIs of a node. Technically speaking, the result is of the node. It can be used as of the chain as long as the node synchronises with other nodes well.

```python
import py_vsys as pv

# ch: pv.Chain
print(await ch.last_block)
```
Example output

```
{'version': 1, 'timestamp': 1646984994012980703, 'reference': 'qQf2yLJZz2bUUgcWqpSG7QsYFbL6fAbcjDRFeEFrzAThd27acBBXdH8mAuCZZ1znm9YcEpHKqrNk4vhNdwBamUk', 'SPOSConsensus': {'mintTime': 1646984994000000000, 'mintBalance': 50010579735931647}, 'resourcePricingData': {'computation': 0, 'storage': 0, 'memory': 0, 'randomIO': 0, 'sequentialIO': 0}, 'TransactionMerkleRoot': 'G2Z7rAg7WDE2jtrzEuUpTxL4uWZYpnxyWzXU5mGjD7pU', 'transactions': [{'type': 5, 'id': '6PJEcK2XsbGJfYHd7q6GS5Zc2vfGDSSy8RLaEUkbxQy2', 'recipient': 'AU4u8erPGstSFSCU1U6cLyFNeR9Cbk1x8eU', 'timestamp': 1646984994012980703, 'amount': 900000000, 'currentBlockHeight': 1355698, 'status': 'Success', 'feeCharged': 0}], 'generator': 'AU4u8erPGstSFSCU1U6cLyFNeR9Cbk1x8eU', 'signature': '4XibrP2u2FsAqgzWMwT7nuTDsALXeRscwXXMSAdQ35RixQfZbMbxeRrRZtFeQ6etAvcDovZcxwbPExdxu628hdkr', 'fee': 0, 'blocksize': 330, 'height': 1355698, 'transaction count': 1}
```

### Actions

#### Get the Block at a Certain Height
Get the block at a certain height.

```python
import py_vsys as pv

# ch: pv.Chain
print(await ch.get_block_at(1355645))
```
Example output

```
{'version': 1, 'timestamp': 1646984676006693040, 'reference': '2Z6LXeq27kPX1UGZU8eJiz72JVNSGiCC234oGQZbMaD7TniDDPjntSTp3zM3xL2MVvco1Dfm3h3PFizFL4PSRDA4', 'SPOSConsensus': {'mintTime': 1646984676000000000, 'mintBalance': 50114224369788003}, 'resourcePricingData': {'computation': 0, 'storage': 0, 'memory': 0, 'randomIO': 0, 'sequentialIO': 0}, 'TransactionMerkleRoot': 'cKWBKEtc5XQGjMobespD5cJydJpzhF1SnafBSS1q1is', 'transactions': [{'type': 5, 'id': '9e1ToB1zuCPoE7zrrj1L14gvcYJFhX9QdKd3NCyTGRG2', 'recipient': 'AU7fEwBgHpe6oeH1iuo2mE5TMCrBxPR8LFc', 'timestamp': 1646984676006693040, 'amount': 900000000, 'currentBlockHeight': 1355645, 'status': 'Success', 'feeCharged': 0}], 'generator': 'AU7fEwBgHpe6oeH1iuo2mE5TMCrBxPR8LFc', 'signature': '59enpKJUjVsvtgbChWuinj9Ds5CfUn7ChPxFgfsQZAAmsU5MGDJJGE6sn2n5UpT49URR69MkcD4ofvFf7zLt5BPq', 'fee': 0, 'blocksize': 330, 'height': 1355645, 'transaction count': 1}
```

#### Get Blocks within a Certain Range
Get blocks within a certain range.

NOTE that the max length of the range is 100.

```python
import py_vsys as pv

# ch: pv.Chain
start = 1355645
end = 1355645 + 1

print(await ch.get_blocks_within(start, end))

start = 1355645
end = 1355645 + 200

print(await ch.get_blocks_within(start, end))
```
Example output

```
[{'version': 1, 'timestamp': 1646984676006693040, 'reference': '2Z6LXeq27kPX1UGZU8eJiz72JVNSGiCC234oGQZbMaD7TniDDPjntSTp3zM3xL2MVvco1Dfm3h3PFizFL4PSRDA4', 'SPOSConsensus': {'mintTime': 1646984676000000000, 'mintBalance': 50114224369788003}, 'resourcePricingData': {'computation': 0, 'storage': 0, 'memory': 0, 'randomIO': 0, 'sequentialIO': 0}, 'TransactionMerkleRoot': 'cKWBKEtc5XQGjMobespD5cJydJpzhF1SnafBSS1q1is', 'transactions': [{'type': 5, 'id': '9e1ToB1zuCPoE7zrrj1L14gvcYJFhX9QdKd3NCyTGRG2', 'recipient': 'AU7fEwBgHpe6oeH1iuo2mE5TMCrBxPR8LFc', 'timestamp': 1646984676006693040, 'amount': 900000000, 'currentBlockHeight': 1355645, 'status': 'Success', 'feeCharged': 0}], 'generator': 'AU7fEwBgHpe6oeH1iuo2mE5TMCrBxPR8LFc', 'signature': '59enpKJUjVsvtgbChWuinj9Ds5CfUn7ChPxFgfsQZAAmsU5MGDJJGE6sn2n5UpT49URR69MkcD4ofvFf7zLt5BPq', 'fee': 0, 'blocksize': 330, 'height': 1355645, 'transaction count': 1}, {'version': 1, 'timestamp': 1646984682014519750, 'reference': '59enpKJUjVsvtgbChWuinj9Ds5CfUn7ChPxFgfsQZAAmsU5MGDJJGE6sn2n5UpT49URR69MkcD4ofvFf7zLt5BPq', 'SPOSConsensus': {'mintTime': 1646984682000000000, 'mintBalance': 50101287145150374}, 'resourcePricingData': {'computation': 0, 'storage': 0, 'memory': 0, 'randomIO': 0, 'sequentialIO': 0}, 'TransactionMerkleRoot': 'J3WDruFNxu11CKFNkNKP4Lb5YEUDV1fJntXpmmvcaLhV', 'transactions': [{'type': 5, 'id': '6YwWoTZBZAungxCyiKJY5VkFsUzb3WhioKTcATSzMQ9', 'recipient': 'ATxtBDygMvWtvh9xJaGQn5MdaHsbuQxbjiG', 'timestamp': 1646984682014519750, 'amount': 900000000, 'currentBlockHeight': 1355646, 'status': 'Success', 'feeCharged': 0}], 'generator': 'ATxtBDygMvWtvh9xJaGQn5MdaHsbuQxbjiG', 'signature': 'nytRh8LMivri3dkjHSvB6ATgKzq7A2R8jBGEtu8NaWB5jjCr4Uj4PVpystLYeQcLQP6ocSXDka2fM26PvwKUpoa', 'fee': 0, 'blocksize': 330, 'height': 1355646, 'transaction count': 1}]
{'error': 10, 'message': 'Too big sequences requested'}
```
