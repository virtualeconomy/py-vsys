# NFT Contract

- [NFT Contract](#nft-contract)
  - [Register](#register)
  - [Create an Instance for an Existing NFT Contract](#create-an-instance-for-an-existing-nft-contract)
  - [Issue](#issue)


## Register

```python
import py_v_sdk as pv
import py_v_sdk.contract.nft_ctrt as nft_ctrt

# chain: pv.Chain
# seed: str
# acnt: pv.Account

# Register a new NFT contract
nc = nft_ctrt.NFTCtrt.register(by=acnt)
print(nc.ctrt_id.data) # print the id of the newly registered contract
```
Example output

```
CF6jEF52DZgn8qjQL2oYdvUT34fgHyU4PWN
```

## Create an Instance for an Existing NFT Contract 
```python
import py_v_sdk as pv
import py_v_sdk.contract.nft_ctrt as nft_ctrt

# chain: pv.Chain
# acnt: pv.Account

# An example NFT contract id
# ctrt_id = "CF6jEF52DZgn8qjQL2oYdvUT34fgHyU4PWN"

# Create a representative instance for an existing NFT contract
nc = nft_ctrt.NFTCtrt(
  pv.B58Str(ctrt_id),
  chain,
)
```

## Issue

```python
import py_v_sdk as pv
import py_v_sdk.contract.nft_ctrt as nft_ctrt

# nc: nft_ctrt.NFTCtrt

resp = nc.issue(by=acnt)
print(resp)
```

Example output
```
{'type': 9, 'id': 'DyFKAkv6xSWuPjau3k8YXoPG4Awk2DL1iCK62Tch8k9u', 'fee': 30000000, 'feeScale': 100, 'timestamp': 1642064271931793920, 'proofs': [{'proofType': 'Curve25519', 'publicKey': '6gmM7UxzUyRJXidy2DpXXMvrPqEF9hR1eAqsmh33J6eL', 'address': 'AU6BNRK34SLuc27evpzJbAswB6ntHV2hmjD', 'signature': '5bVP3Krrddg8Z5J2XDcKb8MHfjqdhhFH6S3rh1pnj2wJde8YsatkBLHhyUs5f4LgqJHKK1zYVaUpdzF5Py2xUS27'}], 'contractId': 'CEvfK7Jw8ZxnbxZjEW8Ejumco5u4YSDKbYi', 'functionIndex': 1, 'functionData': '12Wfh1', 'attachment': ''}
```
