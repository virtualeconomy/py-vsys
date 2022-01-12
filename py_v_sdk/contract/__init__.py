import abc
import enum
from typing import Tuple

import base58

from py_v_sdk import model as md
from py_v_sdk import chain as ch
from py_v_sdk.utils import bytes as bu


class CtrtMeta:

    LANG_CODE_BYTE_LEN = 4
    LANG_VER_BYTE_LEN = 4
    TOKEN_ADDR_VER = -124
    CHECKSUM_LEN = 4

    def __init__(
        self,
        lang_code: md.String,
        lang_ver: md.UnInt,
        triggers: md.BytesList,
        descriptors: md.BytesList,
        state_vars: md.BytesList,
        state_map: md.BytesList,
        textual: md.BytesList,
    ) -> None:
        self.lang_code = lang_code
        self.lang_ver = lang_ver
        self.triggers = triggers
        self.descriptors = descriptors
        self.state_vars = state_vars
        self.state_map = state_map
        self.textual = textual

    @classmethod
    def from_b58_str(cls, b58_str: str) -> "CtrtMeta":
        ctrt_data = base58.b58decode(b58_str)

        lang_code, lang_code_end = cls._parse_lang_code(ctrt_data, 0)
        lang_ver, lang_ver_end = cls._parse_lang_ver(ctrt_data, lang_code_end)
        triggers, trig_end = cls._parse_triggers(ctrt_data, lang_ver_end)
        descriptors, desc_end = cls._parse_descriptors(ctrt_data, trig_end)
        state_vars, stvar_end = cls._parse_state_vars(ctrt_data, desc_end)
        state_map, stmap_end = cls._parse_state_map(ctrt_data, stvar_end, lang_ver)
        textual = cls._parse_textual(ctrt_data, stmap_end)

        return cls(
            lang_code, lang_ver, triggers, descriptors, state_vars, state_map, textual
        )

    @classmethod
    def _parse_lang_code(cls, ctrt_data: bytes, pos: int) -> Tuple[md.String, int]:
        """
        _parse_lang_code parses the language code from the contract data

        Args:
            ctrt_data (bytes): The contract data in bytes
            pos (int): The start position in the contract data

        Returns:
            Tuple[md.String, int]: (language code, the end position)
        """
        l = cls.LANG_CODE_BYTE_LEN
        lang_code = md.String.deserialize(ctrt_data[pos : pos + l])
        return lang_code, pos + l

    @classmethod
    def _parse_lang_ver(cls, ctrt_data: bytes, pos: int) -> Tuple[md.UnInt, int]:
        """
        _parse_lang_ver parses the language version from the contract data

        Args:
            ctrt_data (bytes): The contract data in bytes
            pos (int): The start position in the contract data

        Returns:
            Tuple[md.UnInt, int]: (language version, the end position)
        """
        l = cls.LANG_VER_BYTE_LEN
        lang_ver = md.UnInt.deserialize(ctrt_data[pos : pos + l])
        return lang_ver, pos + l

    @classmethod
    def _parse_triggers(cls, ctrt_data: bytes, pos: int) -> Tuple[md.BytesList, int]:
        """
        _parse_triggers parses the triggers from the contract data

        Args:
            ctrt_data (bytes): The contract data in bytes
            pos (int): The start position in the contract data

        Returns:
            Tuple[md.BytesList, int]: (triggers, the end position)
        """
        l = bu.bytes_to_int(ctrt_data[pos : pos + 2])
        triggers = md.BytesList.deserialize(ctrt_data[pos + 2 : pos + 2 + l])
        return triggers, pos + 2 + l

    @classmethod
    def _parse_descriptors(cls, ctrt_data: bytes, pos: int) -> Tuple[md.BytesList, int]:
        """
        _parse_descriptors parses the descriptors from the contract data

        Args:
            ctrt_data (bytes): The contract data in bytes
            pos (int): The start position in the contract data

        Returns:
            Tuple[md.BytesList, int]: (descriptors, the end position)
        """
        l = bu.bytes_to_int(ctrt_data[pos : pos + 2])
        descriptors = md.BytesList.deserialize(ctrt_data[pos + 2 : pos + 2 + l])
        return descriptors, pos + 2 + l

    @classmethod
    def _parse_state_vars(cls, ctrt_data: bytes, pos: int) -> Tuple[md.BytesList, int]:
        """
        _parse_state_vars parses the state variables from the contract data

        Args:
            ctrt_data (bytes): The contract data in bytes
            pos (int): The start position in the contract data

        Returns:
            Tuple[md.BytesList, int]: (state variables, the end position)
        """
        l = bu.bytes_to_int(ctrt_data[pos : pos + 2])
        state_vars = md.BytesList.deserialize(ctrt_data[pos + 2 : pos + 2 + l])
        return state_vars, pos + 2 + l

    @classmethod
    def _parse_state_map(
        cls, ctrt_data: bytes, pos: int, lang_ver: md.UnInt
    ) -> Tuple[md.BytesList, int]:
        """
        _parse_state_map parses the state map from the contract data

        Args:
            ctrt_data (bytes): The contract data in bytes
            pos (int): The start position in the contract data
            lang_ver (md.UnInt): The language version

        Returns:
            Tuple[md.BytesList, int]: (state maps, the end position)
        """
        if lang_ver.data == 1:
            return md.BytesList(), pos

        l = bu.bytes_to_int(ctrt_data[pos : pos + 2])
        state_map = md.BytesList.deserialize(ctrt_data[pos + 2 : pos + 2 + l])
        return state_map, pos + 2 + l

    @classmethod
    def _parse_textual(cls, ctrt_data: bytes, pos: int) -> md.BytesList:
        """
        _parse_textual parses the textual from the contract data

        Args:
            ctrt_data (bytes): The contract data in bytes
            pos (int): The start position in the contract data

        Returns:
            md.BytesList: The parsed Textual object
        """
        return md.BytesList.deserialize(ctrt_data[pos:])

    def serialize(self) -> md.Bytes:
        """
        serialize serializes meta content of the contract to a byte string

        Returns:
            bytes: The serialized bytes string
        """
        stmap_bytes = (
            b""
            if self.lang_ver.data == 1
            else self.state_map.serialize(True, True).bytes
        )
        b = (
            self.lang_code.serialize().bytes
            + self.lang_ver.serialize().bytes
            + self.triggers.serialize(True, True).bytes
            + self.descriptors.serialize(True, True).bytes
            + self.state_vars.serialize(True, True).bytes
            + stmap_bytes
            + self.textual.serialize(with_items_len=True).bytes
        )
        return md.Bytes(b)


class Contract(abc.ABC):
    """
    Contract is the abstract base class for smart contracts

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
        pass

    def __init__(self, ctrt_id: md.B58Str, chain: ch.Chain) -> None:
        self._ctrt_id = ctrt_id
        self._chain = chain

    @property
    def ctrt_id(self) -> md.B58Str:
        return self._ctrt_id
    
    @property
    def chain(self) -> ch.Chain:
        return self._chain
    