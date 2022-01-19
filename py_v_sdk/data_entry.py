from __future__ import annotations
import abc
import struct
from typing import Tuple, List


from py_v_sdk import model as md


class DataEntry(abc.ABC):
    """
    DataEntry is the container for data(e.g. function_data for executing contract function)
    passed to & received from smart contracts
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
        It converts only the data to bytes.

        Returns:
            bytes: The bytes representation of the DataEntry
        """

    @abc.abstractmethod
    def serialize(self) -> bytes:
        """
        serialize serializes the holding data to bytes

        Returns:
            bytes: The serialization result
        """


class B58Str(DataEntry):

    MODEL = md.B58Str

    def __init__(self, data: md.B58Str = md.B58Str()) -> None:
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

    MODEL = md.PubKey

    IDX = 1
    SIZE = 32

    def __init__(self, data: md.PubKey) -> None:
        self.data = data


class Addr(B58Str):

    MODEL = md.Addr

    IDX = 2
    SIZE = 26

    def __init__(self, data: md.Addr) -> None:
        self.data = data


class Int(DataEntry):
    def __init__(self, data: md.Int = md.Int()) -> None:
        self.data = data


class Long(Int):

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

    IDX = 3


class INT32(Int):

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
    @classmethod
    def deserialize(cls, b: bytes) -> String:
        l = struct.unpack(">H", b[1:3])[0]
        return cls.from_bytes(b[3 : 3 + l])

    @property
    def len_bytes(self) -> bytes:
        """
        len_bytes returns the length of the bytes representation of the holding data in bytes

        Returns:
            bytes: The length in bytes
        """
        return struct.pack(">H", len(self.bytes))

    def serialize(self) -> bytes:
        return self.idx_bytes + self.len_bytes + self.bytes


class String(Text):

    IDX = 5

    def __init__(self, data: md.Str = md.Str()):
        self.data = data

    @classmethod
    def from_bytes(cls, b: bytes) -> String:
        return cls(md.Str.from_bytes(b))

    @property
    def bytes(self) -> bytes:
        return self.data.bytes


class CtrtAcnt(B58Str):

    MODEL = md.CtrtID

    IDX = 6
    SIZE = 26

    def __init__(self, data: md.CtrtID) -> None:
        self.data = data


class Acnt(B58Str):

    MODEL = md.Addr

    IDX = 7
    SIZE = 26

    def __init__(self, data: md.Addr) -> None:
        self.data = data


class TokenID(B58Str):

    MODEL = md.TokenID

    IDX = 8
    SIZE = 30

    def __init__(self, data: md.TokenID) -> None:
        self.data = data


class Timestamp(Long):

    IDX = 9

    def __init__(self, data: md.VSYSTimestamp) -> None:
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

    IDX = 10
    SIZE = 1

    def __init__(self, data: md.Bool = md.Bool()) -> None:
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

    IDX = 11

    def __init__(self, data: md.Bytes = md.Bytes()) -> None:
        self.data = data

    @classmethod
    def from_bytes(cls, b: bytes) -> Bytes:
        return cls(md.Bytes(b))

    @property
    def bytes(self) -> bytes:
        return self.data.data


class Balance(Long):

    IDX = 12


class IndexMap:
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
    def get_de_cls(cls, idx: int) -> DataEntry:
        """
        get_de_cls gets DataEntry Class as per the given index

        Args:
            idx (int): The index to a DataEntry

        Returns:
            DataEntry: The DataEntry class
        """
        return cls.MAP[idx]


class DataStack:
    """
    DataStack is the collection of DataEntry(s)
    """

    def __init__(self, *data_entries: Tuple[DataEntry]) -> None:
        self.entries: List[DataEntry] = list(data_entries)

    @classmethod
    def deserialize(cls, b: bytes) -> DataStack:
        l = struct.unpack(">H", b[:2])[0]
        b = b[2 : 2 + l]

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
        b = struct.pack(">H", len(self.entries))

        for de in self.entries:
            b += de.serialize()

        return b
