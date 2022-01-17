from __future__ import annotations
import abc
import struct
import time
from typing import Tuple, List

import base58


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


class B58(DataEntry):
    def __init__(self, data: str) -> None:
        """
        Args:
            data (str): The string in base58 format
        """
        self.data = data

    @classmethod
    def from_bytes(cls, b: bytes) -> B58:
        return cls(base58.b58encode(b).decode("latin-1"))

    @classmethod
    def deserialize(cls, b: bytes) -> B58:
        return cls.from_bytes(b[1 : 1 + cls.SIZE])

    @property
    def bytes(self) -> bytes:
        return base58.b58encode(self.data)

    def serialize(self) -> bytes:
        return self.idx_bytes + self.bytes


class PubKey(B58):

    IDX = 1
    SIZE = 32


class Addr(B58):

    IDX = 2
    SIZE = 26


class Long(DataEntry):

    SIZE = 8

    def __init__(self, data: int) -> None:
        """
        Args:
            data (int): The integer data
        """
        self.data = data

    @classmethod
    def from_bytes(cls, b: bytes) -> Long:
        return cls(struct.unpack(">Q", b)[0])

    @classmethod
    def deserialize(cls, b: bytes) -> Long:
        return cls.from_bytes(b[1 : 1 + cls.SIZE])

    @property
    def bytes(self) -> bytes:
        return struct.pack(">Q", self.data)

    def serialize(self) -> bytes:
        return self.idx_bytes + self.bytes


class Amount(Long):

    IDX = 3


class INT32(DataEntry):

    IDX = 4
    SIZE = 4

    def __init__(self, data: int) -> None:
        """
        Args:
            data (int): The integer data
        """
        self.data = data

    @classmethod
    def from_bytes(cls, b: bytes) -> INT32:
        return cls(struct.unpack(">I", b)[0])

    @classmethod
    def deserialize(cls, b: bytes) -> INT32:
        return cls.from_bytes(b[1 : 1 + cls.SIZE])

    @property
    def bytes(self) -> bytes:
        return struct.pack(">I", self.data)

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

    def __init__(self, data: str = ""):
        self.data = data

    @classmethod
    def from_bytes(cls, b: bytes) -> String:
        return cls(b.decode("latin-1"))

    @property
    def bytes(self) -> bytes:
        return self.data.encode("latin-1")


class CtrtAcnt(B58):

    IDX = 6
    SIZE = 26


class Acnt(B58):

    IDX = 7
    SIZE = 26


class TokenID(B58):
    """
    TokenID is the data container for Token ID
    """

    IDX = 8
    SIZE = 30


class Timestamp(Long):

    IDX = 9

    @classmethod
    def now(cls) -> Timestamp:
        """
        now returns the Timestamp with the current unix timestamp

        Returns:
            Timestamp: The current Timestamp
        """
        return cls(int(time.time() * 1_000_000_000))


class Bool(DataEntry):

    IDX = 10
    SIZE = 1

    def __init__(self, data: bool) -> None:
        """
        Args:
            data (bool): The boolean data
        """
        self.data = data

    @classmethod
    def from_bytes(cls, b: bytes) -> Bool:
        return cls(struct.unpack(">?", b)[0])

    @classmethod
    def deserialize(cls, b: bytes) -> Bool:
        return cls.from_bytes(b[1 : 1 + cls.SIZE])

    @property
    def bytes(self) -> bytes:
        return struct.pack(">?", self.data)

    def serialize(self) -> bytes:
        return self.idx_bytes + self.bytes


class Bytes(Text):

    IDX = 11

    def __init__(self, data: bytes = b"") -> None:
        self.data = data

    @classmethod
    def from_bytes(cls, b: bytes) -> Bytes:
        return cls(b)

    @property
    def bytes(self) -> bytes:
        return self.data


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
