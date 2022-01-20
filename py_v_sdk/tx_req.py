"""
tx_req contains Transaction requests
"""
from __future__ import annotations
import abc
import enum
import struct
from typing import Dict, Any, TYPE_CHECKING

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import data_entry as de
    from py_v_sdk import contract as ctrt

from py_v_sdk import model as md
from py_v_sdk.utils.crypto import curve_25519 as curve


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

    FEE_SCALE = 100

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

    def sign(self, key_pair: md.KeyPair) -> bytes:
        """
        sign returns the signature for this request in the format of bytes

        Returns:
            bytes: The signature for this request
        """
        return curve.sign(key_pair.pri.bytes, self.data_to_sign)


class RegCtrtTxReq(TxReq):
    """
    RegCtrtTxReq is Register Contract Transaction Request
    """

    TX_TYPE = TxType.REGISTER_CONTRACT

    def __init__(
        self,
        data_stack: de.DataStack,
        ctrt_meta: ctrt.CtrtMeta,
        timestamp: md.VSYSTimestamp,
        description: md.Str = md.Str(),
        fee: md.RegCtrtFee = md.RegCtrtFee(),
    ) -> None:
        """
        Args:
            data_stack (de.DataStack): The payload of this request
            ctrt_meta (ctrt.CtrtMeta): The meta data of the contract to register
            timestamp (md.VSYSTimestamp): The timestamp of this request
            description (md.Str, optional): The description for this request. Defaults to md.Str().
            fee (md.Fee, optional): The fee for this request.
                Defaults to md.RegCtrtFee().
        """
        self.data_stack = data_stack
        self.ctrt_meta = ctrt_meta
        self.timestamp = timestamp
        self.description = description
        self.fee = fee

    @property
    def data_to_sign(self) -> bytes:
        """
        data_to_sign returns the data to be signed for this request in the format of bytes

        Returns:
            bytes: The data to be signed for this request
        """
        ctrt_meta = self.ctrt_meta.serialize()
        data_stack = self.data_stack.serialize()

        return (
            self.TX_TYPE.serialize()
            + struct.pack(">H", len(ctrt_meta))
            + ctrt_meta
            + struct.pack(">H", len(data_stack))
            + data_stack
            + struct.pack(">H", len(self.description.data))
            + self.description.bytes
            + struct.pack(">Q", self.fee.data)
            + struct.pack(">H", self.FEE_SCALE)
            + struct.pack(">Q", self.timestamp.data)
        )

    def to_broadcast_register_payload(self, key_pair: md.KeyPair) -> Dict[str, Any]:
        """
        to_broadcast_register_payload returns the payload for node api /contract/broadcast/register

        Args:
            key_pair (md.KeyPair): The key pair to sign the request

        Returns:
            Dict[str, Any]: The payload
        """

        return {
            "senderPublicKey": key_pair.pub.data,
            "contract": md.Bytes(self.ctrt_meta.serialize()).b58_str,
            "initData": md.Bytes(self.data_stack.serialize()).b58_str,
            "description": self.description.data,
            "fee": self.fee.data,
            "feeScale": self.FEE_SCALE,
            "timestamp": self.timestamp.data,
            "signature": md.Bytes(self.sign(key_pair)).b58_str,
        }


class ExecCtrtFuncTxReq(TxReq):
    """
    ExecCtrtFuncTxReq is Execute Contract Function Transaction Request
    """

    TX_TYPE = TxType.EXECUTE_CONTRACT_FUNCTION

    def __init__(
        self,
        ctrt_id: md.CtrtID,
        func_id: ctrt.Ctrt.FuncIdx,
        data_stack: de.DataStack,
        timestamp: md.VSYSTimestamp,
        attachment: md.Str = md.Str(),
        fee: md.ExecCtrtFee = md.ExecCtrtFee(),
    ) -> None:
        """
        Args:
            ctrt_id (md.CtrtID): The contract id
            func_id (ctrt.Ctrt.FuncIdx): The function index
            data_stack (de.DataStack): The payload of this request
            timestamp (md.VSYSTimestamp): The timestamp of this request
            attachment (md.Str, optional): The attachment for this request. Defaults to md.Str().
            fee (md.ExecCtrtFee, optional): The fee for this request.
                Defaults to md.ExecCtrtFee().
        """
        self.ctrt_id = ctrt_id
        self.func_id = func_id
        self.data_stack = data_stack
        self.timestamp = timestamp
        self.attachment = attachment
        self.fee = fee

    @property
    def data_to_sign(self) -> bytes:
        """
        data_to_sign returns the data to be signed for this request in the format of bytes

        Returns:
            bytes: The data to be signed for this request
        """
        data_stack = self.data_stack.serialize()

        return (
            self.TX_TYPE.serialize()
            + self.ctrt_id.bytes
            + self.func_id.serialize()
            + struct.pack(">H", len(data_stack))
            + data_stack
            + struct.pack(">H", len(self.attachment.data))
            + self.attachment.bytes
            + struct.pack(">Q", self.fee.data)
            + struct.pack(">H", self.FEE_SCALE)
            + struct.pack(">Q", self.timestamp.data)
        )

    def to_broadcast_execute_payload(self, key_pair: md.KeyPair) -> Dict[str, Any]:
        """
        to_broadcast_execute_payload returns the payload for node api /contract/broadcast/execute

        Args:
            key_pair (md.KeyPair): The key pair to sign the request

        Returns:
            Dict[str, Any]: The payload
        """
        return {
            "senderPublicKey": key_pair.pub.data,
            "contractId": self.ctrt_id.data,
            "functionIndex": self.func_id.value,
            "functionData": md.Bytes(self.data_stack.serialize()).b58_str,
            "attachment": self.attachment.b58_str,
            "fee": self.fee.data,
            "feeScale": self.FEE_SCALE,
            "timestamp": self.timestamp.data,
            "signature": md.Bytes(self.sign(key_pair)).b58_str,
        }
