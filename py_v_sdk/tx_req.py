import abc
import enum
from typing import Dict, Any

from py_v_sdk import model as md
from py_v_sdk import contract as ctrt
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

    def serialize(self) -> md.Bytes:
        """
        serialize serializes the TxType to md.Bytes

        Returns:
            md.Bytes: The serilization result
        """
        return md.Bytes(md.UnChar(self.value).bytes)


class TxReq(abc.ABC):
    """
    TxReq is the abstract base class for Transaction Request
    """

    @property
    def data_to_sign(self) -> md.Bytes:
        """
        data_to_sign returns the data to be signed for this request in the format of md.Bytes

        Raises:
            NotImplementedError: Left to be implemented by subclasses

        Returns:
            md.Bytes: The data to be signed for this request
        """
        raise NotImplementedError

    def sign(self, key_pair: md.KeyPair) -> md.Bytes:
        """
        sign returns the signature for this request in the format of md.Bytes

        Returns:
            md.Bytes: The signature for this request
        """
        b = curve.sign(key_pair.pri.bytes, self.data_to_sign.bytes)
        return md.Bytes(b)


class RegCtrtTxReq(TxReq):
    """
    RegCtrtTxReq is Register Contract Transaction Request
    """

    TX_TYPE = TxType.REGISTER_CONTRACT
    TX_FEE = md.TxFee(100 * md.TxFee.VSYS)

    def __init__(
        self,
        data_stack: md.DataStack,
        ctrt_meta: ctrt.CtrtMeta,
        timestamp: md.Timestamp,
        description: md.String = md.String.default(),
        fee: md.TxFee = TX_FEE,
        fee_scale: md.TxFeeScale = md.TxFeeScale.default(),
    ) -> None:
        """
        Args:
            data_stack (md.DataStack): The payload of this request
            ctrt_meta (ctrt.CtrtMeta): The meta data of the contract to register
            timestamp (md.Timestamp): The timestamp of this request
            description (md.String, optional): The description for this request. Defaults to md.String.default().
            fee (md.TxFee, optional): The fee for this request. Defaults to TX_FEE.
            fee_scale (md.TxFeeScale, optional): The fee scale of this request. Defaults to md.TxFeeScale.default().
        """
        self.data_stack = data_stack
        self.ctrt_meta = ctrt_meta
        self.timestamp = timestamp
        self.description = description
        self.fee = fee
        self.fee_scale = fee_scale

    @property
    def data_to_sign(self) -> md.Bytes:
        b = (
            self.TX_TYPE.serialize().bytes
            + self.ctrt_meta.serialize().serialize(with_size=True).bytes
            + self.data_stack.serialize().bytes
            + self.description.serialize_with_str_size().bytes
            + self.fee.bytes
            + self.fee_scale.bytes
            + self.timestamp.bytes
        )
        return md.Bytes(b)

    def to_broadcast_register_payload(self, key_pair: md.KeyPair) -> Dict[str, Any]:
        """
        to_broadcast_register_payload returns the payload for node api /contract/broadcast/register

        Args:
            key_pair (md.KeyPair): The key pair to sign the request

        Returns:
            Dict[str, Any]: The payload
        """
        return {
            "senderPublicKey": key_pair.pub.b58_str,
            "contract": self.ctrt_meta.serialize().b58_str,
            "initData": self.data_stack.serialize(with_bytes_len=False).b58_str,
            "description": self.description.data,
            "fee": self.fee.data,
            "feeScale": self.fee_scale.data,
            "timestamp": self.timestamp.data,
            "signature": self.sign(key_pair).b58_str,
        }


class ExecCtrtFuncTxReq(TxReq):
    """
    ExecCtrtFuncTxReq is Execute Contract Function Transaction Request
    """

    TX_TYPE = TxType.EXECUTE_CONTRACT_FUNCTION
    TX_FEE = md.TxFee(int(0.3 * md.TxFee.VSYS))

    def __init__(
        self,
        ctrt_id: md.B58Str,
        func_id: ctrt.Contract.FuncIdx,
        data_stack: md.DataStack,
        timestamp: md.Timestamp,
        attachment: md.String = md.String.default(),
        fee: md.TxFee = TX_FEE,
        fee_scale: md.TxFeeScale = md.TxFeeScale.default(),
    ) -> None:
        """
        Args:
            ctrt_id (md.B58Str): The contract id
            func_id (ctrt.Contract.FuncIdx): The function index
            data_stack (md.DataStack): The payload of this request
            timestamp (md.Timestamp): The timestamp of this request
            attachment (md.String, optional): The attachment for this request. Defaults to md.String.default().
            fee (md.TxFee, optional): The fee for this request. Defaults to TX_FEE.
            fee_scale (md.TxFeeScale, optional): The fee scale of this request. Defaults to md.TxFeeScale.default().
        """
        self.ctrt_id = ctrt_id
        self.func_id = func_id
        self.data_stack = data_stack
        self.timestamp = timestamp
        self.attachment = attachment
        self.fee = fee
        self.fee_scale = fee_scale

    @property
    def data_to_sign(self) -> md.Bytes:
        b = (
            self.TX_TYPE.serialize().bytes
            + self.ctrt_id.bytes
            + md.UnShort(self.func_id.value).bytes
            + self.data_stack.serialize().bytes
            + self.attachment.serialize_with_str_size().bytes
            + self.fee.bytes
            + self.fee_scale.bytes
            + self.timestamp.bytes
        )
        return md.Bytes(b)

    def to_broadcast_execute_payload(self, key_pair: md.KeyPair) -> Dict[str, Any]:
        """
        to_broadcast_execute_payload returns the payload for node api /contract/broadcast/execute

        Args:
            key_pair (md.KeyPair): The key pair to sign the request

        Returns:
            Dict[str, Any]: The payload
        """
        return {
            "senderPublicKey": key_pair.pub.b58_str,
            "contractId": self.ctrt_id.data,
            "functionIndex": self.func_id.value,
            "functionData": self.data_stack.serialize(with_bytes_len=False).b58_str,
            "attachment": self.attachment.b58_str,
            "fee": self.fee.data,
            "feeScale": self.fee_scale.data,
            "timestamp": self.timestamp.data,
            "signature": self.sign(key_pair).b58_str,
        }
