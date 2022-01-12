# NFT Contract

- [NFT Contract](#nft-contract)
  - [Register](#register)
  - [Issue](#issue)


## Register
The sample codes below show how to register an NFT contract.

```python
import py_v_sdk.contract.nft_ctrt as nft_ctrt

acnt = pv.Account(chain, seed)
nc = nft_ctrt.NFTCtrt.register(by=acnt)
print(nc.ctrt_id)
```

## Issue
(Will be completed soon)
