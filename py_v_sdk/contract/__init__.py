from __future__ import annotations
import abc
import enum
import struct
from typing import Tuple, List, TYPE_CHECKING, NamedTuple

import base58

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import chain as ch

from py_v_sdk import data_entry as de


class Bytes:
    def __init__(self, data: bytes = b"") -> None:
        self.data = data

    @classmethod
    def deserialize(cls, b: bytes) -> Bytes:
        l = struct.unpack(">H", b[:2])[0]
        return cls(b[2 : 2 + l])

    @property
    def bytes(self) -> bytes:
        return self.data

    @property
    def b58_str(self) -> str:
        return base58.b58encode(self.data).decode("latin-1")

    @property
    def len_bytes(self) -> bytes:
        """
        len_bytes returns the length of the bytes representation of the holding data in bytes

        Returns:
            bytes: The length in bytes
        """
        return struct.pack(">H", len(self.bytes))

    def serialize(self) -> bytes:
        return self.len_bytes + self.bytes


class BytesList:
    def __init__(self, *items: Tuple[Bytes]) -> None:
        self.items: List[Bytes] = list(items)

    @classmethod
    def deserialize(cls, b: bytes, with_bytes_len: bool = True) -> BytesList:
        if with_bytes_len:
            l = struct.unpack(">H", b[:2])[0]
            b = b[2 : 2 + l]

        items_cnt = struct.unpack(">H", b[:2])[0]
        b = b[2:]
        items = []
        for _ in range(items_cnt):
            l = struct.unpack(">H", b[:2])[0]
            item = Bytes.deserialize(b)
            items.append(item)
            b = b[2 + l :]

        return cls(*items)

    def serialize(self, with_bytes_len: bool = True) -> bytes:
        b = struct.pack(">H", len(self.items))

        for i in self.items:
            b += i.serialize()

        if with_bytes_len:
            b = struct.pack(">H", len(b)) + b

        return b


class CtrtMeta:

    LANG_CODE_BYTE_LEN = 4
    LANG_VER_BYTE_LEN = 4
    TOKEN_ADDR_VER = -124
    CHECKSUM_LEN = 4

    def __init__(
        self,
        lang_code: str,
        lang_ver: int,
        triggers: BytesList,
        descriptors: BytesList,
        state_vars: BytesList,
        state_map: BytesList,
        textual: BytesList,
    ) -> None:
        self.lang_code = lang_code
        self.lang_ver = lang_ver
        self.triggers = triggers
        self.descriptors = descriptors
        self.state_vars = state_vars
        self.state_map = state_map
        self.textual = textual

    @classmethod
    def from_b58_str(cls, b58_str: str) -> CtrtMeta:
        def parse_len(b: bytes) -> int:
            return struct.unpack(">H", b)[0]

        b = base58.b58decode(b58_str)

        lang_code = b[:4].decode("latin-1")
        b = b[4:]

        lang_ver = struct.unpack(">I", b[:4])[0]
        b = b[4:]

        l = parse_len(b[:2])
        triggers = BytesList.deserialize(b)
        b = b[2 + l :]

        l = parse_len(b[:2])
        descriptors = BytesList.deserialize(b)
        b = b[2 + l :]

        l = parse_len(b[:2])
        state_vars = BytesList.deserialize(b)
        b = b[2 + l :]

        if lang_ver == 1:
            state_map = BytesList()
        else:
            l = parse_len(b[:2])
            state_map = BytesList.deserialize(b)
            b = b[2 + l :]

        textual = BytesList.deserialize(b, with_bytes_len=False)

        return cls(
            lang_code, lang_ver, triggers, descriptors, state_vars, state_map, textual
        )

    def serialize(self) -> bytes:
        """
        serialize serializes meta content of the contract to a byte string

        Returns:
            bytes: The serialized bytes string
        """
        stmap_bytes = b"" if self.lang_ver == 1 else self.state_map.serialize()
        b = (
            self.lang_code.encode("latin-1")
            + struct.pack(">I", self.lang_ver)
            + self.triggers.serialize()
            + self.descriptors.serialize()
            + self.state_vars.serialize()
            + stmap_bytes
            + self.textual.serialize(with_bytes_len=False)
        )
        return b


class Ctrt(abc.ABC):
    """
    Ctrt is the abstract base class for smart contracts

    Each contract has a base58 encoded string that contains meta data of the contract.

    Below is an example response from the node api `contract/content/{contractId}
    {
        "transactionId": "72oJ6qzBJw1ATGV6KTruFcPLEBeJ6yD4VwDhuEUU3Zu6",
        "languageCode": "vdds",
        "languageVersion": 1,
        "triggers": [
            "111111CktRzdj615GhYiN5qtRjzxwE8jypDwGbQV9iXn8NK3o"
        ],
        "descriptors": [
            "1111112EP7Gb96dj5VLAcfpEDiaTeapNEfczB",
            "1bbn7XmN81WxPGPpdCtU38xMGvgaUbnrASoSQf",
            "12CCZE4Xi2itkMk8zE87pKF1mN8U311U2Bq99jV",
            "1QWywjfJS2CDokeThm2PVEKPzag9nouQ72jYj",
            "1N9hmWGg5UN8zHMrtrxMWFND6pUMLhAGg",
            "131h1vYVUznedmBCAvcPqzW6Ewx5xvXF4fB",
            "13R2cuenmhy573wnHtSch5h2jSJQ3hS6h1B",
            "13pNDtm64QxxY3tNu8tVZiwUAPB8TP9cVs7",
            "1VXrvftSE5dDWxAQwUHSpM3jdx2FR",
            "1Z6ifdCDh5xNbucPnydpgg2nbfS3R",
            "1Cyp7C43k4foxpiwcrr33L3mCEKxLsoe",
            "13zAHzf98UyzPAVrFiE8sQLcUX6EcSK"
        ],
        "stateVariables": [
            "13",
            "5T"
        ],
        "textual": {
            "triggers": "124VnyFU9tQUn4Z19KBbV8aAQF4aCgWrQWrLL1yK5RpWY2sU74P8GU6wJ6dwyuFHP3Xt5Kmpm",
            "descriptors": "1RypGiL5eNbDESxn2SVM8HrLF6udvXV6YmwvFsp4fLJfRcr7nQuVFMvXn6KmWJeq8c53tdrutZcsQA2zyHb8Wj1tQUjGmitP6kLzcnpQXEq7AUZpMT6j7LCrhJvs3oLCCr7SSpz3h4iJJJg9WuL7Acbsw1x2AK4tRSZWXyrnLgqWhgqbTdfmxFGHjD58XrScBibJ9AUwEWCAeAna3NFofSZaSDxFJAK2adrrHhJdktQCQobMJMmC164HtJKF569naoMREkncYedQwXWk4uyPzGTUKsfXFwLaR77wv8gtNEjqwvGtpdFJELyJ3RC2F7exhqiiVxTaoGrAanuv1bianVbKqPAygPaGrhA1H3JmQWksNhg6q7dtPvBuqWDqDs4DkhV35JhNFeiER18o49pxX8zR1n1jvis6QrU2cD1Cn3yXwSZaW8TxWMKZ7ULRo1UcJykQvQCLq3EBVfzf6iULhuRagTnJ3Sq4tFSxgnNPhATLDreQpEe1BA3SfRWKRskLFjXV5aMeYxgFLfqYEFJ37BaRVyFZDSUgrKLMnNzrZZG2P81t7MhT6GpDApLZkNtjdGRMQGFsRN2azGruQReFnXeB3mScaxgfhGxcu9B",
            "stateVariables": "1FKqt4aNuTwK15xVSfjkwT"
        },
        "height": 301588
    }
    """

    class FuncIdx(enum.Enum):
        def serialize(self) -> bytes:
            return struct.pack(">H", self.value)

    class StateVar(enum.Enum):
        def serialize(self) -> bytes:
            return struct.pack(">B", self.value)

    class StateMap(NamedTuple):

        idx: int
        data_entry: de.DataEntry

        def serialize(self) -> bytes:
            b = struct.pack(">B", self.idx) + self.data_entry.serialize()
            return b

    class DBKey:
        def __init__(self, data: bytes = b"") -> None:
            self.data = data

        @classmethod
        def from_b58_str(cls, s: str) -> Ctrt.DBKey:
            return cls(base58.b58decode(s))

        @property
        def b58_str(self) -> str:
            return base58.b58encode(self.data).decode("latin-1")

    def __init__(self, ctrt_id: str, chain: ch.Chain) -> None:
        self._ctrt_id = ctrt_id
        self._chain = chain

    @property
    def ctrt_id(self) -> str:
        return self._ctrt_id

    @property
    def chain(self) -> ch.Chain:
        return self._chain
