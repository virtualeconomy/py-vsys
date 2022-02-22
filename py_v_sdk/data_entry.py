"""
data_entry contains DataEntry-related resources.
"""
from __future__ import annotations
import abc
import struct
from typing import Tuple, List, Union, Type

from py_v_sdk import model as md


class DataEntry(abc.ABC):
    """
    DataEntry is the container for data used in interacting with smart contracts.
    """

    IDX = 0
    SIZE = 0

    @property
    def idx_bytes(self) -> bytes:
        """
        idx_bytes returns the index in bytes

        Returns:
            bytes: The index in bytes
        """
        return struct.pack(">B", self.IDX)

    @classmethod
    @abc.abstractmethod
    def from_bytes(cls, b: bytes) -> DataEntry:
        """
        from_bytes parses the given bytes and constructs a DataEntry instance
        It is assumed that the given bytes contains only data(i.e. no other meta info like length)

        Args:
            b (bytes): The bytes to parse

        Returns:
            DataEntry: The DataEntry instance
        """

    @classmethod
    @abc.abstractmethod
    def deserialize(cls, b: bytes) -> DataEntry:
        """
        deserialize parses the given bytes and constructs a DataEntry instance
        It is assumed that the given bytes has meta bytes
        (e.g. data entry index, size, etc) at its front.

        Args:
            b (bytes): The bytes to parse

        Returns:
            DataEntry: The DataEntry instance
        """

    @property
    @abc.abstractmethod
    def bytes(self) -> bytes:
        """
        bytes returns the bytes representation of the DataEntry
        It converts the data to bytes only.

        Returns:
            bytes: The bytes representation of the DataEntry
        """

    @abc.abstractmethod
    def serialize(self) -> bytes:
        """
        serialize serializes the containing data to bytes

        Returns:
            bytes: The serialization result
        """


class B58Str(DataEntry):
    """
    B58Str is the data entry base class for a base58 string.
    """

    MODEL = md.B58Str

    def __init__(self, data: md.B58Str = md.B58Str()) -> None:
        """
        Args:
            data (md.B58Str, optional): The containing data. Defaults to md.B58Str().
        """
        self.data = data

    @classmethod
    def from_bytes(cls, b: bytes) -> B58Str:
        return cls(cls.MODEL.from_bytes(b))

    @classmethod
    def deserialize(cls, b: bytes) -> B58Str:
        return cls.from_bytes(b[1 : 1 + cls.SIZE])

    @property
    def bytes(self) -> bytes:
        return self.data.bytes

    def serialize(self) -> bytes:
        return self.idx_bytes + self.bytes


class PubKey(B58Str):
    """
    PubKey is the data entry for a public key.
    """

    MODEL = md.PubKey

    IDX = 1
    SIZE = 32

    def __init__(self, data: md.PubKey) -> None:
        """
        Args:
            data (md.PubKey): The containing data.
        """
        self.data = data


class Addr(B58Str):
    """
    Addr is the data entry for an address.
    """

    MODEL = md.Addr

    IDX = 2
    SIZE = 26

    def __init__(self, data: md.Addr) -> None:
        """
        Args:
            data (md.Addr): The containing data.
        """
        self.data = data


class Int(DataEntry):
    """
    Int is the data entry base class for an integer.
    """

    def __init__(self, data: md.Int = md.Int()) -> None:
        """
        Args:
            data (md.Int, optional): The containing data. Defaults to md.Int().
        """
        self.data = data


class Long(Int):
    """
    Long is the data entry base class for a 8-bytes integer.
    """

    SIZE = 8

    @classmethod
    def from_bytes(cls, b: bytes) -> Long:
        i = struct.unpack(">Q", b)[0]
        return cls(md.Int(i))

    @classmethod
    def deserialize(cls, b: bytes) -> Long:
        return cls.from_bytes(b[1 : 1 + cls.SIZE])

    @property
    def bytes(self) -> bytes:
        return struct.pack(">Q", self.data.data)

    def serialize(self) -> bytes:
        return self.idx_bytes + self.bytes


class Amount(Long):
    """
    Amount is the data entry for amount.
    """

    IDX = 3

    def __init__(self, data: md.Int) -> None:
        self.data = data

    @classmethod
    def for_vsys_amount(cls, amount: Union[int, float]) -> Amount:
        """
        for_vsys_amount is the handy method to get an Amount for VSYS coins given
        the desired VSYS coins amount.

        Args:
            amount (Union[int, float]): The desired VSYS coins amount.

        Returns:
            Amount: The Amount instance.
        """
        return cls(md.VSYS.for_amount(amount))

    @classmethod
    def for_tok_amount(cls, amount: Union[int, float], unit: int) -> Amount:
        """
        for_tok_amount is the handy method to get an Amount for tokens given
        the desired token amount.

        Args:
            amount (Union[int, float]): The desired tokens amount.
            unit (int): The unit for the token.

        Returns:
            Amount: The Amount instance.
        """
        return cls(md.Token.for_amount(amount, unit))


class INT32(Int):
    """
    INT32 is the data entry for a 4-bytes integer.
    """

    IDX = 4
    SIZE = 4

    @classmethod
    def from_bytes(cls, b: bytes) -> INT32:
        i = struct.unpack(">I", b)[0]
        return cls(md.Int(i))

    @classmethod
    def deserialize(cls, b: bytes) -> INT32:
        return cls.from_bytes(b[1 : 1 + cls.SIZE])

    @property
    def bytes(self) -> bytes:
        return struct.pack(">I", self.data.data)

    def serialize(self) -> bytes:
        return self.idx_bytes + self.bytes


class Text(DataEntry):
    """
    Text is the data entry base class for texts(e.g. string, bytes)
    """

    @classmethod
    def deserialize(cls, b: bytes) -> String:
        l = struct.unpack(">H", b[1:3])[0]
        return cls.from_bytes(b[3 : 3 + l])

    @property
    def len_bytes(self) -> bytes:
        """
        len_bytes returns the length of the bytes representation of the containing data in bytes

        Returns:
            bytes: The length in bytes
        """
        return struct.pack(">H", len(self.bytes))

    def serialize(self) -> bytes:
        return self.idx_bytes + self.len_bytes + self.bytes


class String(Text):
    """
    String is the data entry for a string.
    """

    IDX = 5

    def __init__(self, data: md.Str = md.Str()):
        """
        Args:
            data (md.Str, optional): The containing data. Defaults to md.Str().
        """
        self.data = data

    @classmethod
    def from_bytes(cls, b: bytes) -> String:
        return cls(md.Str.from_bytes(b))

    @property
    def bytes(self) -> bytes:
        return self.data.bytes


class CtrtAcnt(B58Str):
    """
    CtrtAcnt is the data entry for contract account.
    """

    MODEL = md.CtrtID

    IDX = 6
    SIZE = 26

    def __init__(self, data: md.CtrtID) -> None:
        """
        Args:
            data (md.CtrtID): The containing data.
        """
        self.data = data


class Acnt(B58Str):
    """
    Acnt is the data entry for account.
    """

    MODEL = md.Addr

    IDX = 7
    SIZE = 26

    def __init__(self, data: md.Addr) -> None:
        """
        Args:
            data (md.Addr): The containing data.
        """
        self.data = data


class TokenID(B58Str):
    """
    TokenID is the data entry for token ID.
    """

    MODEL = md.TokenID

    IDX = 8
    SIZE = 30

    def __init__(self, data: md.TokenID) -> None:
        """
        Args:
            data (md.TokenID): The containing data.
        """
        self.data = data


class Timestamp(Long):
    """
    Timestamp is the data entry for timestamp.
    """

    IDX = 9

    def __init__(self, data: md.VSYSTimestamp) -> None:
        """
        Args:
            data (md.VSYSTimestamp): The containing data.
        """
        self.data = data

    @classmethod
    def now(cls) -> Timestamp:
        """
        now returns the Timestamp with the current unix timestamp

        Returns:
            Timestamp: The current Timestamp
        """
        n = md.VSYSTimestamp.now()
        return cls(n)


class Bool(DataEntry):
    """
    Bool is the data entry for a boolean value.
    """

    IDX = 10
    SIZE = 1

    def __init__(self, data: md.Bool = md.Bool()) -> None:
        """
        Args:
            data (md.Bool, optional): The containing data. Defaults to md.Bool().
        """
        self.data = data

    @classmethod
    def from_bytes(cls, b: bytes) -> Bool:
        v = struct.unpack(">?", b)[0]
        return cls(md.Bool(v))

    @classmethod
    def deserialize(cls, b: bytes) -> Bool:
        return cls.from_bytes(b[1 : 1 + cls.SIZE])

    @property
    def bytes(self) -> bytes:
        return struct.pack(">?", self.data.data)

    def serialize(self) -> bytes:
        return self.idx_bytes + self.bytes


class Bytes(Text):
    """
    Bytes is the data entry for bytes
    """

    IDX = 11

    def __init__(self, data: md.Bytes = md.Bytes()) -> None:
        """
        Args:
            data (md.Bytes, optional): The containing data. Defaults to md.Bytes().
        """
        self.data = data

    @classmethod
    def from_bytes(cls, b: bytes) -> Bytes:
        return cls(md.Bytes(b))

    @property
    def bytes(self) -> bytes:
        return self.data.data

    @classmethod
    def for_str(cls, str: str) -> Bytes:
        """
        for_str is the handy method to get the data entry for a string.

        Returns:
        The Bytes instance.
        """
        return cls(md.Bytes.from_str(str))

    @classmethod
    def for_base58_str(cls, str: str) -> Bytes:
        """
        for_base58_str is the handy method to get the data entry for a b58 string.

        Returns:
        The Bytes instance.
        """
        return cls(md.Bytes.from_b58_str(str))


class Balance(Long):
    """
    Balance is the data entry for balance.
    """

    IDX = 12


class IndexMap:
    """
    IndexMap is the map between the data entry index & corresponding data entry class.
    """

    MAP = {
        1: PubKey,
        2: Addr,
        3: Amount,
        4: INT32,
        5: String,
        6: CtrtAcnt,
        7: Acnt,
        8: TokenID,
        9: Timestamp,
        10: Bool,
        11: Bytes,
        12: Balance,
    }

    @classmethod
    def get_de_cls(cls, idx: int) -> Type[DataEntry]:
        """
        get_de_cls gets DataEntry Class as per the given index

        Args:
            idx (int): The data entry index.

        Returns:
            DataEntry: The DataEntry class
        """
        return cls.MAP[idx]


class DataStack:
    """
    DataStack is the collection of DataEntry(s)
    """

    def __init__(self, *data_entries: Tuple[DataEntry]) -> None:
        """
        Args:
            *data_entries: (Tuple[DataEntry]): Data entries to contain.
        """
        self.entries: List[DataEntry] = list(data_entries)

    @classmethod
    def deserialize(cls, b: bytes) -> DataStack:
        """
        deserialize deserializes the given bytes and creates a DataStack object.

        Args:
            b (bytes): The bytes to deserialize.

        Returns:
            DataStack: The DataStack object created by deserialization.
        """

        entries_cnt = struct.unpack(">H", b[:2])[0]
        b = b[2:]

        entries = []
        for _ in range(entries_cnt):
            idx = struct.unpack(">B", b[:1])[0]
            de_cls = IndexMap.get_de_cls(idx)
            de = de_cls.deserialize(b)
            entries.append(de)
            b = b[len(de.serialize()) :]

        return cls(*entries)

    def serialize(self) -> bytes:
        """
        serialize serializes the DataStack object to bytes.

        Returns:
            bytes: The serializes result.
        """
        b = struct.pack(">H", len(self.entries))

        for de in self.entries:
            b += de.serialize()

        return b
