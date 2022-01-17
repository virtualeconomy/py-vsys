from __future__ import annotations
import abc
import enum
import struct
from typing import Dict, Any, TYPE_CHECKING

import base58

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import data_entry as de
    from py_v_sdk import contract as ctrt

from py_v_sdk import chain as ch
from py_v_sdk.utils.crypto import curve_25519 as curve


class Bytes:
    def __init__(self, data: bytes = b"") -> None:
        self.data = data

    @property
    def b58_str(self) -> str:
        return base58.b58encode(self.data).decode("latin-1")

    @property
    def bytes_with_len(self) -> bytes:
        return struct.pack(">H", len(self.data)) + self.data


class TxType(enum.Enum):
    """
    TxType is the enum class for transaction types
    """

    GENESIS = 1
    PAYMENT = 2
    LEASE = 3
    LEASE_CANCEL = 4
    MINTING = 5
    CONTEND_SLOTS = 6
    RELEASE_SLOTS = 7
    REGISTER_CONTRACT = 8
    EXECUTE_CONTRACT_FUNCTION = 9
    DB_PUT = 10

    def serialize(self) -> bytes:
        """
        serialize serializes the TxType to bytes

        Returns:
            bytes: The serilization result
        """
        return struct.pack(">B", self.value)


class TxReq(abc.ABC):
    """
    TxReq is the abstract base class for Transaction Request
    """

    @property
    def data_to_sign(self) -> bytes:
        """
        data_to_sign returns the data to be signed for this request in the format of bytes

        Raises:
            NotImplementedError: Left to be implemented by subclasses

        Returns:
            bytes: The data to be signed for this request
        """
        raise NotImplementedError

    def sign(self, key_pair: curve.KeyPair) -> bytes:
        """
        sign returns the signature for this request in the format of bytes

        Returns:
            bytes: The signature for this request
        """
        return curve.sign(key_pair.pri, self.data_to_sign)


class RegCtrtTxReq(TxReq):
    """
    RegCtrtTxReq is Register Contract Transaction Request
    """

    TX_TYPE = TxType.REGISTER_CONTRACT

    def __init__(
        self,
        data_stack: de.DataStack,
        ctrt_meta: ctrt.CtrtMeta,
        timestamp: de.Timestamp,
        description: str = "",
        fee: int = ch.Chain.Defaults.REG_CTRT_FEE,
        fee_scale: int = ch.Chain.Defaults.TX_FEE_SCALE,
    ) -> None:
        """
        Args:
            data_stack (de.DataStack): The payload of this request
            ctrt_meta (ctrt.CtrtMeta): The meta data of the contract to register
            timestamp (de.Timestamp): The timestamp of this request
            description (str, optional): The description for this request. Defaults to "".
            fee (int, optional): The fee for this request. Defaults to ch.Chain.Defaults.REG_CTRT_FEE.
            fee_scale (int, optional): The fee scale of this request. Defaults to ch.Chain.Defaults.TX_FEE_SCALE.
        """
        self.data_stack = data_stack
        self.ctrt_meta = ctrt_meta
        self.timestamp = timestamp
        self.description = description
        self.fee = fee
        self.fee_scale = fee_scale

    @property
    def data_to_sign(self) -> bytes:

        return (
            self.TX_TYPE.serialize()
            + Bytes(self.ctrt_meta.serialize()).bytes_with_len
            + Bytes(self.data_stack.serialize()).bytes_with_len
            + struct.pack(">H", len(self.description))
            + self.description.encode("latin-1")
            + struct.pack(">Q", self.fee)
            + struct.pack(">H", self.fee_scale)
            + self.timestamp.bytes
        )

    def to_broadcast_register_payload(self, key_pair: curve.KeyPair) -> Dict[str, Any]:
        """
        to_broadcast_register_payload returns the payload for node api /contract/broadcast/register

        Args:
            key_pair (curve.KeyPair): The key pair to sign the request

        Returns:
            Dict[str, Any]: The payload
        """

        return {
            "senderPublicKey": key_pair.pub_b58_str,
            "contract": Bytes(self.ctrt_meta.serialize()).b58_str,
            "initData": Bytes(self.data_stack.serialize()).b58_str,
            "description": self.description,
            "fee": self.fee,
            "feeScale": self.fee_scale,
            "timestamp": self.timestamp.data,
            "signature": Bytes(self.sign(key_pair)).b58_str,
        }


class ExecCtrtFuncTxReq(TxReq):
    """
    ExecCtrtFuncTxReq is Execute Contract Function Transaction Request
    """

    TX_TYPE = TxType.EXECUTE_CONTRACT_FUNCTION

    def __init__(
        self,
        ctrt_id: str,
        func_id: ctrt.Contract.FuncIdx,
        data_stack: de.DataStack,
        timestamp: de.Timestamp,
        attachment: str = "",
        fee: int = ch.Chain.Defaults.EXEC_CTRT_FEE,
        fee_scale: int = ch.Chain.Defaults.TX_FEE_SCALE,
    ) -> None:
        """
        Args:
            ctrt_id (str): The contract id
            func_id (ctrt.Contract.FuncIdx): The function index
            data_stack (de.DataStack): The payload of this request
            timestamp (de.Timestamp): The timestamp of this request
            attachment (str, optional): The attachment for this request. Defaults to "".
            fee (int, optional): The fee for this request. Defaults to ch.Chain.Defaults.EXEC_CTRT_FEE.
            fee_scale (int, optional): The fee scale of this request. Defaults to ch.Chain.Defaults.TX_FEE_SCALE.
        """
        self.ctrt_id = ctrt_id
        self.func_id = func_id
        self.data_stack = data_stack
        self.timestamp = timestamp
        self.attachment = attachment
        self.fee = fee
        self.fee_scale = fee_scale

    @property
    def data_to_sign(self) -> bytes:
        return (
            self.TX_TYPE.serialize()
            + base58.b58decode(self.ctrt_id)
            + self.func_id.serialize()
            + Bytes(self.data_stack.serialize()).bytes_with_len
            + struct.pack(">H", len(self.attachment))
            + self.attachment.encode("latin-1")
            + struct.pack(">Q", self.fee)
            + struct.pack(">H", self.fee_scale)
            + self.timestamp.bytes
        )

    def to_broadcast_execute_payload(self, key_pair: curve.KeyPair) -> Dict[str, Any]:
        """
        to_broadcast_execute_payload returns the payload for node api /contract/broadcast/execute

        Args:
            key_pair (curve.KeyPair): The key pair to sign the request

        Returns:
            Dict[str, Any]: The payload
        """
        return {
            "senderPublicKey": key_pair.pub_b58_str,
            "contractId": self.ctrt_id,
            "functionIndex": self.func_id.value,
            "functionData": Bytes(self.data_stack.serialize()).b58_str,
            "attachment": base58.b58encode(self.attachment).decode("latin-1"),
            "fee": self.fee,
            "feeScale": self.fee_scale,
            "timestamp": self.timestamp.data,
            "signature": Bytes(self.sign(key_pair)).b58_str,
        }
