"""
contract contains shared resources for smart contracts
"""
from __future__ import annotations
import abc
import enum
import struct
from typing import Tuple, List, TYPE_CHECKING, NamedTuple, Any

import base58
from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_vsys import chain as ch

from py_vsys import data_entry as de
from py_vsys import model as md
from py_vsys.utils.crypto import hashes as hs


class Bytes:
    """
    Bytes is the helper data container for bytes used in contract meta data
    with handy methods.
    """

    def __init__(self, data: bytes = b"") -> None:
        """
        Args:
            data (bytes, optional): The data to contain. Defaults to b"".
        """
        self.data = data

    @classmethod
    def deserialize(cls, b: bytes) -> Bytes:
        """
        deserialize deserializes the given bytes and creates a Bytes object.

        Args:
            b (bytes): The bytes to deserialize.

        Returns:
            Bytes: The Bytes object created by deserialization.
        """
        l = struct.unpack(">H", b[:2])[0]
        return cls(b[2 : 2 + l])

    @property
    def len_bytes(self) -> bytes:
        """
        len_bytes returns the length in bytes of the containing data.

        Returns:
            bytes: The length in bytes.
        """
        return struct.pack(">H", len(self.data))

    def serialize(self) -> bytes:
        """
        serialize serializes Bytes object to bytes.

        Returns:
            bytes: The serialization result.
        """
        return self.len_bytes + self.data


class BytesList:
    """
    BytesList is a collection of Bytes
    """

    def __init__(self, *items: Tuple[Bytes]) -> None:
        """
        Args:
            *items (Tuple[Bytes]): Bytes objects to contain
        """
        self.items: List[Bytes] = list(items)

    @classmethod
    def deserialize(cls, b: bytes, with_bytes_len: bool = True) -> BytesList:
        """
        deserialize deserializes the given bytes and creates a BytesList object.

        Args:
            b (bytes): The bytes to deserialize.
            with_bytes_len (bool, optional): If the first 2 bytes of the given data
                should be treated as the meta data that indicates the length for the data.
                Defaults to True.

        Returns:
            BytesList: The BytesList object created by deserialization.
        """
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
        """
        serialize serializes BytesList object to bytes.

        Args:
            with_bytes_len (bool, optional): If the 2-bytes meta data that indicates
                the length of the data should be prepended.
                Defaults to True.

        Returns:
            bytes: The serialization result.
        """
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
        """
        Args:
            lang_code (str): The language code of the contract. E.g. "vdds".
            lang_ver (int): The language version of the contract. E.g. 1
            triggers (BytesList): The triggers of the contract.
            descriptors (BytesList): The descriptors of the contract.
            state_vars (BytesList): The state variables of the contract.
            state_map (BytesList): The state map of the contract.
            textual (BytesList): The textual of the contract.
        """
        self.lang_code = lang_code
        self.lang_ver = lang_ver
        self.triggers = triggers
        self.descriptors = descriptors
        self.state_vars = state_vars
        self.state_map = state_map
        self.textual = textual

    @classmethod
    def from_b58_str(cls, b58_str: str) -> CtrtMeta:
        """
        from_b58_str creates a CtrtMeta object from the given base58 string.

        Args:
            b58_str (str): The base58 string to parse.

        Returns:
            CtrtMeta: The result CtrtMeta object.
        """
        b = base58.b58decode(b58_str)
        return cls.deserialize(b)

    @classmethod
    def deserialize(cls, b: bytes) -> CtrtMeta:
        """
        deserialize deserializes the given bytes to a CtrtMeta object.

        Args:
            b (bytes): The bytes to deserialize.

        Returns:
            CtrtMeta: The result CtrtMeta object.
        """

        def parse_len(b: bytes) -> int:
            """
            parse_len unpacks the given 2 bytes as an unsigned short integer.

            Args:
                b (bytes): The bytes to unpack.

            Returns:
                int: The unpacked value.
            """
            return struct.unpack(">H", b)[0]

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
        serialize serializes CtrtMeta to a bytes.

        Returns:
            bytes: The serialization result.
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
    Ctrt is the abstract base class for smart contracts.
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
        """
        FuncIdx is the enum class for function indexes of a contract.
        """

        def serialize(self) -> bytes:
            """
            serialize serializes the FuncIdx object to bytes.

            Returns:
                bytes: The serialization result.
            """
            return struct.pack(">H", self.value)

    class StateVar(enum.Enum):
        """
        StateVar is the enum class for state variables of a contract.
        """

        def serialize(self) -> bytes:
            """
            serialize serializes the StateVar object to bytes.

            Returns:
                bytes: The serialization result.
            """
            return struct.pack(">B", self.value)

    class StateMapIdx(enum.Enum):
        """
        StateMapIdx is the enum class for state map indexes.
        """

    class StateMap(NamedTuple):
        """
        StateMap is the class for state map of a contract.
        """

        idx: Ctrt.StateMapIdx
        data_entry: de.DataEntry

        def serialize(self) -> bytes:
            """
            serialize serializes the StateMap object to bytes.

            Returns:
                bytes: The serialization result.
            """
            b = struct.pack(">B", self.idx.value) + self.data_entry.serialize()
            return b

    class DBKey(md.Bytes):
        """
        DBKey is the class for DB key of a contract used to query data.
        """

    def __init__(self, ctrt_id: str, chain: ch.Chain) -> None:
        """
        Args:
            ctrt_id (str): The id of the contract.
            chain (ch.Chain): The object of the chain where the contract is on.
        """
        self._ctrt_id = md.CtrtID(ctrt_id)
        self._chain = chain

    @property
    def ctrt_id(self) -> md.CtrtID:
        """
        ctrt_id returns the contract id in base58 string format.

        Returns:
            md.CtrtID: The contract id.
        """
        return self._ctrt_id

    @property
    def chain(self) -> ch.Chain:
        """
        chain returns the chain object of the contract.

        Returns:
            ch.Chain: The chain object of the contract.
        """
        return self._chain

    async def _query_db_key(self, db_key: Ctrt.DBKey) -> Any:
        """
        _query_db_key queries the data by the given db_key.

        Args:
            db_key (Ctrt.DBKey): The db key.

        Returns:
            Any: The result.
        """
        data = await self.chain.api.ctrt.get_ctrt_data(
            ctrt_id=self.ctrt_id.data,
            db_key=db_key.b58_str,
        )
        logger.debug(data)
        return data["value"]

    @staticmethod
    def get_tok_id(ctrt_id: md.CtrtID, tok_idx: md.TokenIdx) -> md.TokenID:
        """
        get_tok_id computes the token ID based on the given contract ID & token index.

        Args:
            ctrt_id (md.CtrtID): The contract ID.
            tok_idx (md.TokenIdx): The token index.

        Returns:
            md.TokenID: The token ID.
        """
        b = ctrt_id.bytes
        raw_ctrt_id = b[1 : (len(b) - CtrtMeta.CHECKSUM_LEN)]
        ctrt_id_no_checksum = (
            struct.pack("<b", CtrtMeta.TOKEN_ADDR_VER)
            + raw_ctrt_id
            + struct.pack(">I", tok_idx.data)
        )
        h = hs.keccak256_hash(hs.blake2b_hash(ctrt_id_no_checksum))

        tok_id_bytes = base58.b58encode(
            ctrt_id_no_checksum + h[: CtrtMeta.CHECKSUM_LEN]
        )

        tok_id = tok_id_bytes.decode("latin-1")
        return md.TokenID(tok_id)


class BaseTokCtrt(Ctrt):
    """
    BaseTokCtrt is the base class for token contracts(NFT included)
    """

    @property
    @abc.abstractmethod
    async def unit(self) -> int:
        """
        unit returns the unit of the token contract.

        Returns:
            int: The unit.
        """
