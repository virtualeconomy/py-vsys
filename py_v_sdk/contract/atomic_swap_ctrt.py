"""
atomic_swap_ctrt contains Atomic Swap contract.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any, Union
from py_v_sdk.data_entry import DataStack

from loguru import logger
import asyncio

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import account as acnt

from py_v_sdk import data_entry as de
from py_v_sdk import tx_req as tx
from py_v_sdk import model as md
from py_v_sdk import chain as ch
from . import CtrtMeta, Ctrt

from py_v_sdk.utils.crypto.hashes import sha256_hash
import base58


class AtomicSwapCtrt(Ctrt):
    """
    AtomicSwapCtrt is the class for VSYS Atomic Swap contract.
    """

    CTRT_META = CtrtMeta.from_b58_str(
        "4CrYZXauEHTHvUcNbU2qxvYSgdxPkSBum4PAUfytuZu7Nn56L59op72uKJUBMnF8dk8dLb5k63M9236s8S2yH4FTeWFP4zjfpkx9HGwjAuh6n6WJyxWE1S5HHH2cQLy4xk5B4iMpQKyHQwrQDn3zWwQQPsrfnwaHX1F3V2zKHKx15QYATS784BGfz9NeY72Ntdz2Cgsf6MLQE1YKdgdRfpryCwadqs5xchALCPYLNg6ECSxzPDa4XdS8ywTWzRpiajTGZA1z9YoQZiUMYBwM8S2G4ttZJkgrWTqpXuxberLv3CWZm7kp8bwvg577p8kJ7zAugTgaBU9vzSRFzi3fWtGEP1TPuMCjLSQfskepjoLXbPHyVMmvLZGbjx2AwCyGikdXBdLJWhheL6rnveiXJQfV6zfgF9zeMTpg9GE5SRstGHFetCZwfe3qCPV6vUWrobmWusQ9rDkj5uUXVpjwmBseynCnKNS1CZKDnBDy6mWBDPHNCtuDdYCamqaSEh1nx9ykk4vVJggzPJR8awFMHh5iKPRL9LGhuqbqs4rDPVsg7BCrdaszTGEBEHjfqF51K8PF9kUnPQJvGkf58MrLj2SAArizmZYcnpGMwdfYqGxrjz7xaJGZVAqvFbWFDk3x18ozp58PwFM1fdAn1dn15fKCsiQoqZBtVTxSd4GRJ2tFvBzgUJjig6hqhHqCqobCbpes8LoTdtDCHE5Co3YBnrYN19vbESu2W6LMpwrPPgd1YUeHx8AxR9evasFYrCjmnvBkEyefu5n66yTPYNXfjAk646dHmWYJiUPp1oWDXMjfDJ4xif4BXhRwBtfwgHoDhU2dMV6E7cPVppXxeVL2UsFCbqsafpNcDmhsrGEDAWmxJ3V8KymyuNugM1CHTEiwcTb7GXd4dD3UznDVoJEVrmBveETvCuGVNfGZ4zGZnURyoJHzMkDKPWFQhqgVYLoRuLg4MtquRAaSEKixtXiSJZFKZvQTzMbJC2ie3bnyQoX3x2C9pPpzp3uFKc1eGpgafgi8KoyiqiCMJvfzi8v8DiyTZ9QPENAtwToUpf6vsn1C4HhDzGb9otfigtVuh9JuzsZkJbd4r2rU8sUcKWZcaLF1uX4EdZiEfiW3aV5cm1L7oEJX2w4rQbNiFZWGUpS31WS6mYtWkSTnQupp7rggs8sQxcdWK8WamLgonF4mhXkY12Y2U9AXDJifMKr7mzxiFxZumPWxGn8A1PtTp34wcuhykNMesekwDgWGRCWca9w3YDkeinoD2QmV5ivF2GfHTKhCVH5pkGmBZczeVMA2ZTWb5DTM5qQA9vRy43aJipwmYH73ssbdF7N96678x4hsdcFXXJooRbDtuEY9UkhFPtFMjzD7D5uvXzN4qTPFSyoumwH3ag6cmZMxxQdHNJAm7vitgDpRy3HM174KpjE7uUQXtVvMKEYeAWus24vwW6M4i7APsVg6FeJTgGJJHAHFJFJ4YrZ1fmzgGFnugfp9g4hMuo9G76dzzkZetLhweJCggXBRVpNeRzQ9xmtuDN3wmiyQ1bLSx2ZtNcmWqzbSDsUnCezXtbF4CURyp2djUKo2DRza78CHpmUgHHVai8JrAxPwS6gB8mBg"
    )

    class FuncIdx(Ctrt.FuncIdx):
        """
        FuncIdx is the enum class for function indexes of a contract.
        """

        LOCK = 0
        SOLVE_PUZZLE = 1
        EXPIRE_WITHDRAW = 2

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

        TOKEN_BALANCE = 0
        SWAP_OWNER = 1
        SWAP_RECIPIENT = 2
        SWAP_PUZZLE = 3
        SWAP_AMOUNT = 4
        SWAP_EXPIRED_TIME = 5
        SWAP_STATUS = 6

    class DBKey(Ctrt.DBKey):
        """
        DBKey is the class for DB key of a contract used to query data.
        """

        @classmethod
        def for_maker(cls) -> AtomicSwapCtrt.DBKey:
            """
            for_maker returns the AtomicSwapCtrt.DBKey object for querying the maker.

            Returns:
                AtomicSwapCtrt.DBKey: The AtomicSwapCtrt.DBKey object.
            """
            b = AtomicSwapCtrt.StateVar.MAKER.serialize()
            return cls(b)

        @classmethod
        def for_token_id(cls) -> AtomicSwapCtrt.DBKey:
            """
            for_token_id returns the AtomicSwapCtrt.DBKey object for querying the token_id.

            Returns:
                AtomicSwapCtrt.DBKey: The AtomicSwapCtrt.DBKey object.
            """
            b = AtomicSwapCtrt.StateVar.TOKEN_ID.serialize()
            return cls(b)

        @classmethod
        def for_token_balance(cls, addr: str) -> AtomicSwapCtrt.DBKey:
            """
            for_token_balance returns the AtomicSwapCtrt.DBKey object for querying the token balance.

            Returns:
                AtomicSwapCtrt.DBKey: The AtomicSwapCtrt.DBKey object.
            """
            b = AtomicSwapCtrt.StateMap(
                idx=AtomicSwapCtrt.StateMapIdx.TOKEN_BALANCE,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

        @classmethod
        def for_swap_owner(cls, tx_id: str) -> AtomicSwapCtrt.DBKey:
            """
            for_swap_owner returns the AtomicSwapCtrt.DBKey object for querying the swap owner.

            Returns:
                AtomicSwapCtrt.DBKey: The AtomicSwapCtrt.DBKey object.
            """
            b = AtomicSwapCtrt.StateMap(
                idx=AtomicSwapCtrt.StateMapIdx.SWAP_OWNER,
                data_entry=de.Bytes.for_base58_str(tx_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_swap_recipient(cls, tx_id: str) -> AtomicSwapCtrt.DBKey:
            """
            for_swap_recipient returns the AtomicSwapCtrt.DBKey object for querying the swap receipient.

            Returns:
                AtomicSwapCtrt.DBKey: The AtomicSwapCtrt.DBKey object.
            """
            b = AtomicSwapCtrt.StateMap(
                idx=AtomicSwapCtrt.StateMapIdx.SWAP_RECIPIENT,
                data_entry=de.Bytes.for_base58_str(tx_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_puzzle(cls, tx_id: str) -> AtomicSwapCtrt.DBKey:
            """
            for_puzzle gets the AtomicSwapCtrt.DBKey object for querying the hashed puzzle.

            Returns:
                AtomicSwapCtrt.DBKey: The AtomicSwapCtrt.DBKey object.
            """
            b = AtomicSwapCtrt.StateMap(
                idx=AtomicSwapCtrt.StateMapIdx.SWAP_PUZZLE,
                data_entry=de.Bytes(md.Bytes(base58.b58decode(tx_id))),
            ).serialize()
            return cls(b)

        @classmethod
        def for_swap_amount(cls, tx_id: str) -> AtomicSwapCtrt.DBKey:
            """
            for_swap_amount returns the AtomicSwapCtrt.DBKey object for querying the swap amount.

            Returns:
                AtomicSwapCtrt.DBKey: The AtomicSwapCtrt.DBKey object.
            """
            b = AtomicSwapCtrt.StateMap(
                idx=AtomicSwapCtrt.StateMapIdx.SWAP_AMOUNT,
                data_entry=de.Bytes.for_base58_str(tx_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_swap_expired_time(cls, tx_id: str) -> AtomicSwapCtrt.DBKey:
            """
            for_swap_expired_time returns the AtomicSwapCtrt.DBKey object for querying the swap expired time.

            Returns:
                AtomicSwapCtrt.DBKey: The AtomicSwapCtrt.DBKey object.
            """
            b = AtomicSwapCtrt.StateMap(
                idx=AtomicSwapCtrt.StateMapIdx.SWAP_EXPIRED_TIME,
                data_entry=de.Bytes.for_base58_str(tx_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_swap_status(cls, tx_id: str) -> AtomicSwapCtrt.DBKey:
            """
            for_swap_status returns the AtomicSwapCtrt.DBKey object for querying the swap status.

            Returns:
                AtomicSwapCtrt.DBKey: The AtomicSwapCtrt.DBKey object.
            """
            b = AtomicSwapCtrt.StateMap(
                idx=AtomicSwapCtrt.StateMapIdx.SWAP_STATUS,
                data_entry=de.Bytes.for_base58_str(tx_id),
            ).serialize()
            return cls(b)

    @classmethod
    async def register(
        cls,
        by: acnt.Account,
        tok_id: str,
        ctrt_description: str = "",
        fee: int = md.RegCtrtFee.DEFAULT,
    ) -> AtomicSwapCtrt:
        """
        register registers an Atomic Swap Contract

        Args:
            by (acnt.Account): The action taker.
            tok_id (str): The id of the token to atomic swap.
            ctrt_description (str, optional): The description of the contract. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.RegCtrtFee.DEFAULT.

        Returns:
            AtomicSwapCtrt: The AtomicSwapCtrt object of the registered Atomic Swap contract.
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

    async def get_swap_balance(self, addr: str) -> md.Token:
        """
        get_swap_balance queries & returns the balance of the token deposited into the contract.

        Args:
            addr (str): The account address that deposits the token.

        Returns:
            md.Token: The balance of the token.
        """
        bal = await self._query_db_key(self.DBKey.for_token_balance(addr))

        resp = await self.chain.api.ctrt.get_tok_info(await self.token_id)
        unit = resp["unity"]
        return md.Token.for_amount(bal, unit)

    async def get_swap_owner(self, tx_id: str) -> md.Addr:
        """
        get_swap_owner queries & returns the address of swap owner.

        Args:
            tx_id (str): The lock transaction id.

        Returns:
            md.Addr: The address of the swap owner.
        """
        owner_addr = await self._query_db_key(self.DBKey.for_swap_owner(tx_id))

        return md.Addr(owner_addr)

    async def get_swap_recipient(self, tx_id: str) -> md.Addr:
        """
        get_swap_recipient queries & returns the address of swap recipient.

        Args:
            tx_id (str): The lock transaction id.

        Returns:
            md.Addr: The address of the recipient.
        """
        recipient_addr = await self._query_db_key(self.DBKey.for_swap_recipient(tx_id))

        return md.Addr(recipient_addr)

    async def get_swap_puzzle(self, tx_id: str) -> str:
        """
        get_swap_puzzle queries & returns the hashed secret.

        Args:
            tx_id (str): The lock transaction id.

        Returns:
            str: The puzzle.
        """
        puzzle = await self._query_db_key(self.DBKey.for_puzzle(tx_id))

        return puzzle

    async def get_swap_amount(self, tx_id: str) -> md.Token:
        """
        get_swap_amount queries & returns the balance that the token locked.

        Args:
            tx_id (str): The lock transaction id.

        Returns:
            int: The balance of the token locked.
        """
        amount = await self._query_db_key(self.DBKey.for_swap_amount(tx_id))

        resp = await self.chain.api.ctrt.get_tok_info(await self.token_id)
        unit = resp["unity"]
        return md.Token.for_amount(amount, unit)

    async def get_swap_expired_time(self, tx_id: str) -> md.VSYSTimestamp:
        """
        get_swap_expired_time queries & returns the expired timestamp.

        Args:
            tx_id (str): The lock transaction id.

        Returns:
            md.VSYSTimestamp: The expired timestamp.
        """
        expired_time = await self._query_db_key(self.DBKey.for_swap_expired_time(tx_id))

        return md.VSYSTimestamp(int(expired_time))

    async def get_swap_status(self, tx_id: str) -> str:
        """
        get_swap_status queries & returns the status of the swap contract.

        Args:
            tx_id (str): The lock transaction id.

        Returns:
            bool: The status of the swap contract.
        """
        status = await self._query_db_key(self.DBKey.for_swap_status(tx_id))

        return status

    async def maker_lock(
        self,
        by: acnt.Account,
        amount: Union[int, float],
        recipient: str,
        secret: str,
        expire_time: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        maker_lock locks the token by the maker.
        Args:
            by (acnt.Account): The action taker.
            amount (Union[int, float]): The amount of the token to be locked.
            recipient (str): The taker's address.
            secret (str): The secret.
            expire_time (int): The expired timestamp to lock.
            attachment (str, optional): [description]. Defaults to "".
            fee (int, optional): [description]. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """
        SCALE = 1_000_000_000
        puzzle_bytes = sha256_hash(secret.encode("latin-1"))

        tok_id = await self.token_id
        resp = await by.chain.api.ctrt.get_tok_info(tok_id)
        unit = resp["unity"]

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.LOCK,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount, unit),
                    de.Addr(md.Addr(recipient)),
                    de.Bytes(md.Bytes(puzzle_bytes)),
                    de.Timestamp(md.VSYSTimestamp(int(expire_time * SCALE))),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def taker_lock(
        self,
        by: acnt.Account,
        amount: Union[int, float],
        maker_swap_ctrt_id: str,
        recipient: str,
        maker_lock_tx_id: str,
        expire_time: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        taker_lock locks the token by the maker.

        Args:
            by (acnt.Account): The action maker.
            amount (Union[int, float]): The amount of the token to be locked.
            maker_swap_ctrt_id: The contract id of the maker's.
            recipient (str): The maker's address.
            maker_lock_tx_id (str): The tx id of the maker's.
            expire_time (int): The expire timestamp to lock.
            attachment (str, optional): [description]. Defaults to "".
            fee (int, optional): [description]. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """
        SCALE = 1_000_000_000

        puzzle_db_key = self.DBKey.for_puzzle(maker_lock_tx_id)
        print(puzzle_db_key.b58_str)
        data = await self.chain.api.ctrt.get_ctrt_data(
            maker_swap_ctrt_id, puzzle_db_key.b58_str
        )
        logger.debug(data)
        hashed_secret_b58str = data["value"]
        puzzle_bytes = base58.b58decode(hashed_secret_b58str.encode("latin-1"))

        tok_id = await self.token_id
        resp = await by.chain.api.ctrt.get_tok_info(tok_id)
        unit = resp["unity"]

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.LOCK,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount, unit),
                    de.Addr(md.Addr(recipient)),
                    de.Bytes(md.Bytes(puzzle_bytes)),
                    de.Timestamp(md.VSYSTimestamp(expire_time * SCALE)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def maker_solve(
        self,
        by: acnt.Account,
        taker_ctrt_id: str,
        tx_id: str,
        key: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        maker_solve encapsulates the secret.

        Args:
            by (acnt.Account): The action maker.
            taker_ctrt_id (str): The swap ctrt id of the taker's.
            tx_id (str): The lock transaction id of taker's .
            key (str): The secret.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=md.CtrtID(taker_ctrt_id),
                func_id=self.FuncIdx.SOLVE_PUZZLE,
                data_stack=de.DataStack(
                    de.Bytes(md.Bytes(base58.b58decode(tx_id))),
                    de.Bytes(md.Bytes(key.encode("latin-1"))),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def taker_solve(
        self,
        by: acnt.Account,
        maker_ctrt_id: str,
        maker_lock_tx_id: str,
        maker_solve_tx_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        Taker_solve gets the puzzle.

        Args:
            by (acnt.Account): The action maker.
            maker_ctrt_id (str): The contract id of the maker's.
            maker_lock_tx_id (str): The lock tx id of the maker's.
            maker_solve_tx_id (str): The solve tx id of the maker's.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """
        # get the revealed_secret
        dict_data = await by.chain.api.tx.get_info(maker_solve_tx_id)
        func_data = dict_data["functionData"]
        ds = DataStack.deserialize(base58.b58decode(func_data))
        revealed_secret = ds.entries[1].data.data.decode("latin-1")

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=md.CtrtID(maker_ctrt_id),
                func_id=self.FuncIdx.SOLVE_PUZZLE,
                data_stack=de.DataStack(
                    de.Bytes(md.Bytes(base58.b58decode(maker_lock_tx_id))),
                    de.Bytes(md.Bytes(revealed_secret.encode("latin-1"))),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def exp_withdraw(
        self,
        by: acnt.Account,
        tx_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        exp_withdraw withdraws the tokens when the lock is expired.

        Args:
            by (acnt.Account): the action taker.
            tx_id (str): The transaction lock id.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.EXPIRE_WITHDRAW,
                data_stack=de.DataStack(de.Bytes(md.Bytes(base58.b58decode(tx_id)))),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data
