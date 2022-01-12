import enum
from typing import Dict, Any

from loguru import logger

from py_v_sdk import account as acnt
from py_v_sdk import tx_req
from py_v_sdk import model as md

from . import *


class NFTCtrt(Contract):
    """
    NFTContract is the class that encapsulates behaviours of the VSYS NFT contract V1
    """

    CTRT_META = CtrtMeta.from_b58_str(
        "VJodouhmnHVDwtkBZ2NdgahT7NAgNE9EpWoZApzobhpua2nDL9D3sbHSoRRk8bEFeme2BHrXPdcq5VNJcPdGMUD54Smwatyx74cPJyet6bCWmLciHE2jGw9u5TmatjdpFSjGKegh76GvJstK3VaLagvsJJMaaKM9MNXYtgJyDr1Zw7U9PXV7N9TQnSsqz6EHMgDvd8aTDqEG7bxxAotkAgeh4KHqnk6Ga117q5AJctJcbUtD99iUgPmJrC8vzX85TEXgHRY1psW7D6daeExfVVrEPHFHrU6XfhegKv9vRbJBGL861U4Qg6HWbWxbuitgtKoBazSp7VofDtrZebq2NSpZoXCAZC8DRiaysanAqyCJZf7jJ8NfXtWej8L9vg8PVs65MrEmK8toadcyCA2UGzg6pQKrMKQEUahruBiS7zuo62eWwJBxUD1fQ1RGPk9BbMDk9FQQxXu3thSJPnKktq3aJhD9GNFpvyEAaWigp5nfjgH5doVTQk1PgoxeXRAWQNPztjNvZWv6iD85CoZqfCWdJbAXPrWvYW5FsRLW1xJ4ELRUfReMAjCGYuFWdA3CZyefpiDEWqVTe5SA6J6XeUppRyXKpKQTc6upesoAGZZ2NtFDryq22izC6D5p1i98YpC6Dk1qcKevaANKHH8TfFoQT717nrQEY2aLoWrA1ip2t5etdZjNVFmghxXEeCAGy3NcLDFHmAfcBZhHKeJHp8H8HbiMRtWe3wmwKX6mPx16ahnd3dMGCsxAZfjQcy4J1HpuCm7rHMULkixUFYRYqx85c7UpLcijLRybE1MLRjEZ5SEYtazNuiZBwq1KUcNipzrxta9Rpvt2j4WyMadxPf5r9YeAaJJp42PiC6SGfyjHjRQN4K3pohdQRbbG4HQ95NaWCy7CAwbpXRCh9NDMMQ2cmTfB3KFW2M"
    )

    class FuncIdx(Contract.FuncIdx):
        SUPERSEDE = 0
        ISSUE = 1
        SEND = 2
        TRANSFER = 3
        DEPOSIT = 4
        WITHDRAW = 5

    class DBKey(enum.Enum):
        ISSUER = 0
        MAKER = 1

        def serialize(self) -> md.Bytes:
            return md.Bytes(md.UnChar(self.value).bytes)

        @property
        def b58_str(self) -> str:
            return self.serialize().b58_str

    @classmethod
    def register(cls, by: acnt.Account) -> "NFTCtrt":
        data = by.register_contract(
            tx_req.RegCtrtTxReq(
                data_stack=md.DataEntries.default(),
                ctrt_meta=cls.CTRT_META,
                timestamp=md.Timestamp.default(),
            )
        )
        logger.debug(data)

        return cls(
            ctrt_id=md.B58Str(data["contractId"]),
            chain=by.chain,
        )

    @property
    def issuer(self) -> str:
        data = self.chain.api.ctrt.get_contract_data(
            ctrt_id=self.ctrt_id.data,
            db_key=self.DBKey.ISSUER.b58_str,
        )
        logger.debug(data)
        return data["value"]

    @property
    def maker(self) -> str:
        data = self.chain.api.ctrt.get_contract_data(
            ctrt_id=self.ctrt_id.data,
            db_key=self.DBKey.MAKER.b58_str,
        )
        logger.debug(data)
        return data["value"]

    def issue(self, by: acnt.Account, description: str = "") -> Dict[str, Any]:
        data = by.execute_contract(
            tx_req.ExecCtrtFuncTxReq(
                ctrt_id=self.ctrt_id,
                func_id=self.FuncIdx.ISSUE,
                data_stack=md.DataEntries([
                    md.String(description),
                ]),
                timestamp=md.Timestamp.default(),
                attachment=md.String(description),
            )
        )
        logger.debug(data)
        return data
