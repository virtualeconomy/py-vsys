from __future__ import annotations
import abc
import time
from typing import Any, NamedTuple

import base58

from py_v_sdk import chain as ch
from py_v_sdk.utils.crypto import hashes as hs


class Model(abc.ABC):
    def __init__(self, data: Any) -> None:
        self.data = data
        self.validate()

    @abc.abstractmethod
    def validate(self) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        cls_name = self.__class__.__name__
        return f"{cls_name}({self.data})"


class Str(Model):
    def __init__(self, data: str = "") -> None:
        self.data = data
        self.validate()

    @classmethod
    def from_bytes(cls, b: bytes) -> Str:
        return cls(b.decode("latin-1"))

    @property
    def bytes(self) -> bytes:
        return self.data.encode("latin-1")

    @property
    def b58_str(self) -> str:
        return base58.b58encode(self.data).decode("latin-1")

    def validate(self) -> None:
        cls_name = self.__class__.__name__

        if not isinstance(self.data, str):
            raise TypeError(f"Data in {cls_name} must be a str")


class B58Str(Str):
    @classmethod
    def from_bytes(cls, b: bytes) -> B58Str:
        return cls(base58.b58encode(b).decode("latin-1"))

    @property
    def bytes(self) -> bytes:
        return base58.b58decode(self.data)

    def validate(self) -> None:
        super().validate()
        cls_name = self.__class__.__name__

        try:
            self.bytes
        except ValueError:
            raise ValueError(f"Data in {cls_name} must be base58-decodable")


class FixedSizeB58Str(B58Str):
    BYTES_LEN = 0

    def validate(self) -> None:
        super().validate()
        cls_name = self.__class__.__name__

        if not len(self.bytes) == self.BYTES_LEN:
            raise ValueError(
                f"Data in {cls_name} must be exactly {self.BYTES_LEN} bytes after base58 decode"
            )


class Addr(FixedSizeB58Str):

    VER = 5
    VER_BYTES_LEN = 1
    CHAIN_ID_BYTES_LEN = 1
    PUB_KEY_HASH_BYTES_LEN = 20
    CHECKSUM_BYTES_LEN = 4
    BYTES_LEN = (
        VER_BYTES_LEN + CHAIN_ID_BYTES_LEN + PUB_KEY_HASH_BYTES_LEN + CHECKSUM_BYTES_LEN
    )

    @property
    def version(self) -> int:
        return self.bytes[0]

    @property
    def chain_id(self) -> str:
        return chr(self.bytes[1])

    @property
    def pub_key_hash(self) -> bytes:
        prev_len = self.VER_BYTES_LEN + self.CHAIN_ID_BYTES_LEN
        b = self.bytes[prev_len:]
        return b[: self.PUB_KEY_HASH_BYTES_LEN]

    @property
    def checksum(self) -> bytes:
        return self.bytes[-self.CHECKSUM_BYTES_LEN :]

    def must_on(self, chain: ch.Chain):
        if self.chain_id != chain.chain_id.value:
            raise ValueError(
                f"Addr is not on the chain. The Addr has chain_id '{self.chain_id}' while the chain expects '{chain.chain_id.value}'"
            )

    def validate(self) -> None:
        super().validate()
        cls_name = self.__class__.__name__

        if self.version != self.VER:
            raise ValueError(f"Data in {cls_name} has invalid address version")

        chain_id_valid = any([self.chain_id == c.value for c in ch.ChainID])
        if not chain_id_valid:
            raise ValueError(f"Data in {cls_name} has invalid chain_id")

        def ke_bla_hash(b: bytes) -> bytes:
            return hs.keccak256_hash(hs.blake2b_hash(b))

        cl = self.CHECKSUM_BYTES_LEN
        if self.bytes[-cl:] != ke_bla_hash(self.bytes[:-cl])[:cl]:
            raise ValueError(f"Data in {cls_name} has invalid checksum")


class CtrtID(FixedSizeB58Str):
    BYTES_LEN = 26


class TokenID(FixedSizeB58Str):
    BYTES_LEN = 30


class PubKey(FixedSizeB58Str):
    BYTES_LEN = 32


class PriKey(FixedSizeB58Str):
    BYTES_LEN = 32


class Int(Model):
    def __init__(self, data: int = 0) -> None:
        self.data = data
        self.validate()

    def validate(self) -> None:
        cls_name = self.__class__.__name__
        if not isinstance(self.data, int):
            raise TypeError(f"Data in {cls_name} must be an int")


class NonNegativeInt(Int):
    def validate(self) -> None:
        super().validate()
        cls_name = self.__class__.__name__

        if not self.data >= 0:
            raise ValueError(f"Data in {cls_name} must be non negative")


class TokenIdx(NonNegativeInt):
    pass


class Nonce(NonNegativeInt):
    pass


class VSYSTimestamp(NonNegativeInt):

    SCALE = 1_000_000_000

    @classmethod
    def from_unix_ts(cls, ux_ts: int | float) -> VSYSTimestamp:
        if not (isinstance(ux_ts, int) or isinstance(ux_ts, float)):
            raise TypeError("ux_ts must be an int or float")

        if ux_ts <= 0:
            raise ValueError("ux_ts must be greater than 0")

        return cls(int(ux_ts * cls.SCALE))

    @classmethod
    def now(cls) -> VSYSTimestamp:
        return cls(int(time.time() * cls.SCALE))

    def validate(self) -> None:
        super().validate()
        cls_name = self.__class__.__name__

        if self.data <= self.SCALE:
            raise ValueError(f"Data in {cls_name} must be greater than {self.SCALE}")


class VSYS(NonNegativeInt):

    UNIT = 1_00_000_000

    @classmethod
    def one(cls) -> VSYS:
        return cls(cls.UNIT)

    @property
    def amount(self) -> float:
        return self.data / self.UNIT

    def __mul__(self, quantity: int | float) -> VSYS:
        return self.__class__(int(self.data * quantity))


class Fee(VSYS):

    DEFAULT = int(VSYS.UNIT * 0.1)

    def __init__(self, data: int = 0) -> None:
        if data == 0:
            data = self.DEFAULT
        super().__init__(data)

    def validate(self) -> None:
        super().validate()
        cls_name = self.__class__.__name__

        if not self.data >= self.DEFAULT:
            raise ValueError(
                f"Data in {cls_name} must be equal or greater than {self.DEFAULT}"
            )


class RegCtrtFee(Fee):

    DEFAULT = VSYS.UNIT * 100


class ExecCtrtFee(Fee):

    DEFAULT = int(VSYS.UNIT * 0.3)


class ContendSlotsFee(Fee):

    DEFAULT = VSYS.UNIT * 50_000


class DBPutFee(Fee):

    DEFAULT = VSYS.UNIT


class Bytes(Model):
    def __init__(self, data: bytes = b"") -> None:
        self.data = data
        self.validate()

    @property
    def b58_str(self) -> str:
        return base58.b58encode(self.data).decode("latin-1")

    def validate(self) -> None:
        cls_name = self.__class__.__name__

        if not isinstance(self.data, bytes):
            raise TypeError(f"Data in {cls_name} must be bytes")


class Bool(Model):
    def __init__(self, data: bool = False) -> None:
        self.data = data
        self.validate()

    def validate(self) -> None:
        cls_name = self.__class__.__name__

        if not isinstance(self.data, bool):
            raise TypeError(f"Data in {cls_name} must be a bool")


class KeyPair(NamedTuple):
    pub: PubKey
    pri: PriKey
