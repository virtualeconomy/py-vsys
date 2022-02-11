"""
lock_ctrt contains Lock contract.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any

from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import account as acnt

from py_v_sdk import data_entry as de
from py_v_sdk import tx_req as tx
from py_v_sdk import model as md
from . import CtrtMeta, Ctrt


class LockCtrt(Ctrt):
    """
    LockCtrt is the class for VSYS Lock contract.
    """

    CTRT_META = CtrtMeta.from_b58_str(
        "4Qgfi31k6qfLxTguJg8AeYzmmgaCTJCEPQyAdoRUUSrFDc91PhkdU6C8QQSsNCFc2xEud2XnuQ4YNJ51HgdNtBdnxZcU5Rnqdzyop41Ck81v4nRKkHpTdTrfD8vTur2w4mTFeTFKVzGvGjpHXUVvT47vZiKLBHSB7FHHpGf69bu8DQGXWu6xnZZkn9v2Rfc9mByhwVLSNghNdRhrQwRWPFJ9Qt7Yb8N8WdmcUCAC6PrC3Ha3Z9w7dyf6CsKcCMS6JmB2gvNQitm9jqAfjRxDdqPBUR6TtyjSdmHP9BZRGgiVCaQH7X8fbJZVWSib4RXvFoSrqY4SfVftDY3PU4hXASaRWbaheB8m4VgM4mA8nKDbZvRWZtZ4cHdWeNFyVPs6HxHQZHrQ3GZGNPjmBSyAkGRFS7i5dK8aYWQDEYu1Xijk63UFAWuf6tRdR44ZgRjWGUZJtdQBDFB38XaU8LSFEj2eaC1yNqZ6nnGeRXDzS1q3YKsGyJTqaDDMHvPHiHonGn76JQHAZN7eGU7biaSLxoikW4MaTPSfmcTmDyPGJyJNHjc8MrpV8aQSaGGyDkf1a9MpoJcyEjsPFQbxYzSJVqFEFg2oUL7Z8VUtJK2kYcWDz7w8UiiQqe3uuQnKDGb1nJ5Ad3W8ZPfVP6YHbJrnBKZXMMypNoveokVvxZMCkSNYDsoBxJzrwFvm5DcDJbePQU6VbeZ5SzQw9XTAw4DZpxkQm9RwRE9PXPqogpp9P6LhaiUa6ZD1cWUAHypjWLJ2Rds96oap3biBp5aESunuh99HByoXg5Aa7EQ3FrEvmeq9TLVFYpJraZyW"
    )

    class FuncIdx(Ctrt.FuncIdx):
        """
        FuncIdx is the enum class for function indexes of a contract.
        """

        LOCK = 0

    class StateVar(Ctrt.StateVar):
        """
        StateVar is the enum class for state variables of a contract.
        """

        MAKER = 0
        TOKEN_ID = 1

    class StateMapIdx(Ctrt.StateMapIdx):
        """
        StateMapIdx is the enum class for state map indexes.
        """

        CONTRACT_BALANCE = 0
        CONTRACT_LOCK_TIME = 1

    class DBKey(Ctrt.DBKey):
        """
        DBKey is the class for DB key of a contract used to query data.
        """

        @classmethod
        def for_maker(cls) -> LockCtrt.DBKey:
            """
            for_maker returns the LockCtrt.DBKey object for querying the maker.

            Returns:
                LockCtrt.DBKey: The LockCtrt.DBKey object.
            """
            b = LockCtrt.StateVar.MAKER.serialize()
            return cls(b)

        @classmethod
        def for_token_id(cls) -> LockCtrt.DBKey:
            """
            for_token_id returns the LockCtrt.DBKey object for querying the token_id.

            Returns:
                LockCtrt.DBKey: The LockCtrt.DBKey object.
            """
            b = LockCtrt.StateVar.TOKEN_ID.serialize()
            return cls(b)

        @classmethod
        def for_contract_balance(cls, addr: str) -> LockCtrt.DBKey:
            """
            for_contract_balance returns the LockCtrt.DBKey object for querying the contract balance.

            Args:
                addr (str): The account address.

            Returns:
                LockCtrt.DBKey: The LockCtrt.DBKey object.
            """
            b = LockCtrt.StateMap(
                idx=LockCtrt.StateMapIdx.CONTRACT_BALANCE,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

        @classmethod
        def for_contract_lock_time(cls, addr: str) -> LockCtrt.DBKey:
            """
            for_contract_lock_time returns the LockCtrt.DBKey object for querying the contract lock time.

            Args:
                addr (str): The account address.

            Returns:
                LockCtrt.DBKey: The LockCtrt.DBKey object.
            """
            b = LockCtrt.StateMap(
                idx=LockCtrt.StateMapIdx.CONTRACT_LOCK_TIME,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

    @classmethod
    async def register(
        cls,
        by: acnt.Account,
        tok_id: str,
        ctrt_description: str = "",
        fee: int = md.RegCtrtFee.DEFAULT,
    ) -> LockCtrt:
        """
        register registers a Lock Contract

        Args:
            by (acnt.Account): The action taker.
            tok_id (str): The id of the token to lock.
            ctrt_description (str, optional): The description of the contract. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.RegCtrtFee.DEFAULT.

        Returns:
            LockCtrt: The LockCtrt object of the registered Lock contract.
        """
        data = await by._register_contract(
            tx.RegCtrtTxReq(
                data_stack=de.DataStack(
                    de.TokenID(md.TokenID(tok_id)),
                ),
                ctrt_meta=cls.CTRT_META,
                timestamp=md.VSYSTimestamp.now(),
                description=md.Str(ctrt_description),
                fee=md.RegCtrtFee(fee),
            )
        )
        print(data)
        logger.debug(data)

        return cls(
            data["contractId"],
            chain=by.chain,
        )

    @property
    async def maker(self) -> str:
        """
        maker queries & returns the maker of the contract.

        Returns:
            str: The address of the maker of the contract.
        """
        return await self._query_db_key(self.DBKey.for_maker())

    @property
    async def token_id(self) -> str:
        """
        token_id queries & returns the token_id of the contract.

        Returns:
            str: The token_id of the contract.
        """
        return await self._query_db_key(self.DBKey.for_token_id())

    async def get_ctrt_bal(self, addr: str) -> int:
        """
        get_ctrt_bal queries & returns the balance of the token within this contract
        belonging to the user address.

        Args:
            addr (str): The account address.

        Returns:
            int: The balance of the token.
        """
        return await self._query_db_key(self.DBKey.for_contract_balance(addr))

    async def get_ctrt_lock_time(self, addr: str) -> int:
        """
        get_ctrt_lock_time queries & returns the lock time of the token locked in this contract
        belonging to the user address.

        Args:
            addr (str): The account address.

        Returns:
            int: The lock time of the token in Unix timestamp.
        """
        raw_ts = await self._query_db_key(self.DBKey.for_contract_lock_time(addr))
        unix_ts = md.VSYSTimestamp(raw_ts).unix_ts
        return int(unix_ts)

    async def lock(
        self,
        by: acnt.Account,
        expire_at: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        lock locks the user's deposited tokens in the contract until the given timestamp.

        Args:
            by (acnt.Account): The action taker.
            expire_at (int): Unix timestamp. When the lock will expire.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.LOCK,
                data_stack=de.DataStack(
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(expire_at)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data
