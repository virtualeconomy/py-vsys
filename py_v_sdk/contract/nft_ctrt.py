from __future__ import annotations
import enum
import struct
from typing import Dict, Any, TYPE_CHECKING

from loguru import logger


# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import account as acnt

from py_v_sdk import data_entry as de
from py_v_sdk import tx_req as tx

from . import Bytes, CtrtMeta, Contract


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

        def serialize(self) -> bytes:
            return struct.pack(">B", self.value)

        @property
        def b58_str(self) -> str:
            return Bytes(self.serialize()).b58_str

    @classmethod
    def register(cls, by: acnt.Account) -> NFTCtrt:
        data = by.register_contract(
            tx.RegCtrtTxReq(
                data_stack=de.DataStack(),
                ctrt_meta=cls.CTRT_META,
                timestamp=de.Timestamp.now(),
            )
        )
        logger.debug(data)

        return cls(
            data["contractId"],
            chain=by.chain,
        )

    @property
    def issuer(self) -> str:
        data = self.chain.api.ctrt.get_contract_data(
            ctrt_id=self.ctrt_id,
            db_key=self.DBKey.ISSUER.b58_str,
        )
        logger.debug(data)
        return data["value"]

    @property
    def maker(self) -> str:
        data = self.chain.api.ctrt.get_contract_data(
            ctrt_id=self.ctrt_id,
            db_key=self.DBKey.MAKER.b58_str,
        )
        logger.debug(data)
        return data["value"]

    def issue(self, by: acnt.Account, description: str = "") -> Dict[str, Any]:
        data = by.execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self.ctrt_id,
                func_id=self.FuncIdx.ISSUE,
                data_stack=de.DataStack(
                    de.String(description),
                ),
                timestamp=de.Timestamp.now(),
                attachment=description,
            )
        )
        logger.debug(data)
        return data

    def send(self, by: acnt.Account, recipient: str, tok_idx: int, attachment: str = "") -> Dict[str, Any]:
        """
        send sends the NFT token from the action taker to the recipient

        Args:
            by (acnt.Account): The action taker
            recipient (str): The account address of the recipient
            tok_idx (int): The index of the token within this contract to operate
            attachment (str): The attachment of this action
        """
        data = by.execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self.ctrt_id,
                func_id=self.FuncIdx.SEND,
                data_stack=de.DataStack(
                    de.Addr(recipient),
                    de.INT32(tok_idx),
                ),
                timestamp=de.Timestamp.now(),
                attachment=attachment,
            )
        )
        logger.debug(data)
        return data
