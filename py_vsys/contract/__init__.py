"""
contract contains shared resources for smart contracts
"""
from __future__ import annotations
import abc
import enum
import struct
from typing import TYPE_CHECKING, NamedTuple, Any

from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_vsys import chain as ch

from py_vsys import data_entry as de
from py_vsys import model as md
from py_vsys.utils.crypto import hashes as hs


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
        return ctrt_id.get_tok_id(tok_idx.data)


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
