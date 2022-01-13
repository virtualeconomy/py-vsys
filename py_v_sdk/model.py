import abc
import struct
import copy
import time
from typing import List, Type, NamedTuple

import base58

from py_v_sdk.utils import bytes as bu


class DataEntry(abc.ABC):
    """
    DataEntry is the abstract base class for customized data containers
    """

    IDX = 0

    @classmethod
    @abc.abstractmethod
    def from_bytes(cls, b: bytes) -> "DataEntry":
        """
        from_bytes parses the given bytes and constructs a DataEntry instance
        It is assumed that the given bytes contains only data(i.e. no other meta info like length)

        Args:
            b (bytes): The bytes to parse

        Raises:
            NotImplementedError: Left to be implemented by subclasses

        Returns:
            DataEntry: The DataEntry instance
        """
        raise NotImplementedError

    @classmethod
    def deserialize(cls, b: bytes, size_bytes_len: int = 0) -> "DataEntry":
        """
        deserialize parses the given bytes and constructs a DataEntry instance
        It is assumed that the given bytes might have a few prefix bytes containing its length

        Args:
            b (bytes): The bytes to parse
            size_bytes_len (int): The length of the prefix size bytes

        Returns:
            DataEntry: The DataEntry instance
        """
        s = size_bytes_len
        if s == 0:
            return cls.from_bytes(b)

        l = bu.bytes_to_int(b[:s])
        return cls.from_bytes(b[s : s + l])

    @classmethod
    def default(cls) -> "DataEntry":
        """
        default returns a default instance of DataEntry

        Returns:
            DataEntry: The default instance of DataEntry
        """
        return cls()

    @property
    @abc.abstractmethod
    def bytes(self) -> bytes:
        """
        bytes returns the bytes representation of the DataEntry
        It converts only the data to bytes.

        Raises:
            NotImplementedError: Left to be implemented by subclasses

        Returns:
            bytes: The bytes representation of the DataEntry
        """
        raise NotImplementedError

    def serialize(self, with_size: bool = False, with_idx: bool = False) -> "Bytes":
        """
        serialize serializes the holding data to bytes
        if with_size == True, prefix bytes for the length will be prepended
        if with_idx == True, prefix bytes for the index will be prepended

        Args:
            with_size (bool, optional): Whether or not to prepend size bytes. Defaults to False
            with_idx (bool, optional): Whether or not to prepend idx bytes. Defaults to False

        Returns:
            Bytes: The serialization result
        """
        b = self.bytes

        if with_size:
            b = struct.pack(">H", len(b)) + b

        if with_idx:
            b = UnChar(self.IDX).bytes + b

        return Bytes(b)


class DataEntries:
    """
    DataEntries is the collection class for DataEntry
    """

    def __init__(self, items: Optional[List[DataEntry]] = None) -> None:
        if items is None:
            self.items = []
        else:
        self.items = copy.deepcopy(items)

    @classmethod
    def default(cls) -> "DataEntries":
        """
        default returns a default instance of DataEntries

        Returns:
            DataEntries: The default instance of DataEntries
        """
        return cls()

    @classmethod
    def deserialize_as(
        cls, de_cls: Type[DataEntry], b: bytes, size_bytes_len: int = 2
    ) -> "DataEntries":
        """
        deserialize_as parses the given bytes and constructs a DataEntries instance with the given
        de_cls as the type of each item

        E.g.
        size_bytes_len == 2
        b"\x00\x02\x00\x01\x05\x00\x01\x06"
            => items_len => b"\x00\x02" => 2
            => items => [
                de_cls.deserialize(b"\x00\x01\x05", 2),
                de_cls.deserialize(b"\x00\x01\x06", 2),
            ]

        Args:
            de_cls (Type[DataEntry]): The type of each item
            b (bytes): The bytes to parse
            size_bytes_len (int): The length of size bytes

        Returns:
            DataEntries: The DataEntries instance
        """

        s = size_bytes_len
        items_len = bu.bytes_to_int(b[:s])
        b = b[s:]

        items = []
        for _ in range(items_len):
            l = bu.bytes_to_int(b[:s])
            i = de_cls.deserialize(b, size_bytes_len)
            items.append(i)
            b = b[s + l :]

        return cls(items)

    def serialize(
        self, with_items_len: bool = False, with_bytes_len: bool = False,
        **item_serial_args
    ) -> "Bytes":
        """
        serialize serializes the holding DataEntry items to bytes

        Args:
            with_items_len (bool, optional): Whether or not to prepend size bytes for the amount of items. Defaults to False.
            with_bytes_len (bool, optional): Whether or not to prepend size bytes for the length of bytes. Defaults to False.

        Kwargs: 
            item_serial_args (Dict[str, Any]): Keyword arguments for the serialize method of items

        Returns:
            Bytes: The serialization result
        """

        b = b""
        if with_items_len:
            b = struct.pack(">H", len(self.items)) + b

        for i in self.items:
            b += i.serialize(**item_serial_args).bytes

        if with_bytes_len:
            b = struct.pack(">H", len(b)) + b

        return Bytes(b)


class Integer(DataEntry):
    """
    Integer is the data container for integer
    """

    def __init__(self, data: int = 0) -> None:
        self.data = data


class UnChar(Integer):
    """
    UnChar is the data container for unsigned char integer (1 byte)
    """
    @classmethod
    def from_bytes(cls, b: bytes) -> "UnChar":
        return cls(struct.unpack(">B", b)[0])

    @property
    def bytes(self) -> bytes:
        return struct.pack(">B", self.data)


class UnShort(Integer):
    """
    UnShort is the data container for unsigned short integer (2 bytes)
    """

    @classmethod
    def from_bytes(cls, b: bytes) -> "UnShort":
        return cls(struct.unpack(">H", b)[0])

    @property
    def bytes(self) -> bytes:
        return struct.pack(">H", self.data)


class TxFeeScale(UnShort):
    """
    TxFeeScale is the data container for transaction fee scale
    """

    DEFAULT_FEE_SCALE = 100

    @classmethod
    def default(cls) -> "TxFeeScale":
        return cls(cls.DEFAULT_FEE_SCALE)


class UnInt(Integer):
    """
    UnInt is the data container for unsinged integer (4 bytes)
    """

    IDX = 4

    @classmethod
    def from_bytes(cls, b: bytes) -> "UnInt":
        return cls(struct.unpack(">I", b)[0])

    @property
    def bytes(self) -> bytes:
        return struct.pack(">I", self.data)


class UnLongLong(Integer):
    """
    UnLongLong is the data container for unsinged long long integer (8 bytes)
    """

    @classmethod
    def from_bytes(cls, b: bytes) -> "UnLongLong":
        return cls(struct.unpack(">Q", b)[0])

    @property
    def bytes(self) -> bytes:
        return struct.pack(">Q", self.data)


class TxFee(UnLongLong):
    """
    TxFee is the data container for transaction fee
    """

    VSYS = 1_00_000_000
    DEFAULT_TX_FEE = int(0.1 * VSYS)

    @classmethod
    def default(cls) -> "TxFee":
        return cls(cls.DEFAULT_TX_FEE)


class Timestamp(UnLongLong):
    """
    Timestamp is the data container for Unix timestamp
    To avoid floating point, a second is stored as 1_000_000_000
    """

    IDX = 9

    @classmethod
    def now(cls) -> "Timestamp":
        """
        now returns the Timestamp with the current unix timestamp

        Returns:
            [type]: [description]
        """
        return cls(int(time.time() * 1_000_000_000))

    @classmethod
    def default(cls) -> "Timestamp":
        return cls.now()


class Amount(UnLongLong):
    """
    Amount is the data container for amount
    """    
    IDX = 3


class Balance(UnLongLong):
    """
    Balance is the data container for account balance
    """
    IDX = 12


class String(DataEntry):
    """
    String is the data container for string
    """

    IDX = 5

    def __init__(self, data: str = ""):
        self.data = data

    @classmethod
    def from_bytes(cls, b: bytes) -> "String":
        return cls(bu.bytes_to_str(b))

    @property
    def bytes(self) -> bytes:
        return bu.str_to_bytes(self.data)

    @property
    def b58_str(self) -> str:
        """
        b58_str returns a base58-encoded string representation of
        the contained str data

        Returns:
            str: The generated base58-encoded string representation
        """
        b = base58.b58encode(self.data)
        return bu.bytes_to_str(b)

    def serialize_with_str_size(self) -> "Bytes":
        """
        serialize_with_str_size serializes the holding str to bytes
        The length of the holding str will be serialized to bytes and pad to the front

        E.g.
        "a" => b"a" => b'\x00\x01a'

        Returns:
            bytes: The serialization result
        """
        b = struct.pack(">H", len(self.data)) + self.bytes
        return Bytes(b)


class B58Str(String):
    """
    B58Str is the data container for string encoded in base58
    """

    @classmethod
    def from_bytes(cls, b: bytes) -> "String":
        b = base58.b58encode(b)
        return cls(bu.bytes_to_str(b))
    
    @property
    def bytes(self) -> bytes:
        return base58.b58decode(self.data)


class PubKey(B58Str):
    """
    PubKey is the data container for Public Key in base58 string format
    """
    IDX = 1


class Addr(B58Str):
    """
    Addr is the data container for Address in base58 string format
    """    
    IDX = 2


class CtrtAcnt(B58Str):
    """
    CtrtAcnt is the data container for Contract Account
    """
    IDX = 6


class Acnt(B58Str):
    """
    Acnt is the data container for Account
    """
    IDX = 7


class TokenID(B58Str):
    """
    TokenID is the data container for Token ID
    """
    IDX = 8


class Bytes(DataEntry):
    """
    Bytes is the data container for bytes
    """

    IDX = 11

    def __init__(self, data: bytes = b"") -> None:
        self.data = data

    @classmethod
    def from_bytes(cls, b: bytes) -> "Bytes":
        return cls(b)

    @property
    def bytes(self) -> bytes:
        return self.data

    @property
    def b58_str(self) -> str:
        """
        b58_str returns a base58-encoded string representation of
        the contained bytes data

        Returns:
            str: The generated base58-encoded string representation
        """
        return bu.bytes_to_b58_str(self.data)


class BytesList(DataEntries):
    """
    BytesList is the collection class for Bytes
    """

    @classmethod
    def deserialize(cls, b: bytes, size_bytes_len: int = 2) -> "BytesList":
        """
        deserialize parses the given bytes and constructs a BytesList instance
        It is assumed that the given bytes might have a few prefix bytes containing its length

        Args:
            b (bytes): The bytes to parse
            size_bytes_len (int): The length of the prefix size bytes

        Returns:
            BytesList: The BytesList instance
        """
        return cls.deserialize_as(Bytes, b, size_bytes_len)

    @property
    def b58_str_list(self) -> List[str]:
        """
        b58_str_list returns a list of base58-encoded string representation of
        each contained bytes data

        Returns:
            List[str]: The list of base58-encoded string representation
        """
        return [i.b58_str for i in self.items]

    def serialize(self, with_items_len: bool = True, with_bytes_len: bool = True) -> "Bytes":
        return super().serialize(
            with_items_len,
            with_bytes_len,
            **{
                "with_size": True,
                "with_idx": False,
            },
        )


class Bool(DataEntry):
    """
    Bool is the data container for a boolean value
    """
    IDX = 10


class KeyPair(NamedTuple):
    pub: Bytes
    pri: Bytes
