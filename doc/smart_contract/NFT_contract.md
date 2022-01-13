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
(Will be completed soon)
