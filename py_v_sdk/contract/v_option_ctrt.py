"""
v_option_ctrt contains V Option contract.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Union

from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import account as acnt
    from py_v_sdk import chain as ch

from py_v_sdk import data_entry as de
from py_v_sdk import tx_req as tx
from py_v_sdk import model as md
from . import CtrtMeta, Ctrt

import py_v_sdk as pv


class VOptionCtrt(Ctrt):
    """
    VOptionCtrt is the class for VSYS V Option contract.
    """

    CTRT_META = CtrtMeta.from_b58_str(
        "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"
    )

    class FuncIdx(Ctrt.FuncIdx):
        """
        FuncIdx is the enum class for function indexes of a contract.
        """

        SUPERSEDE = 0
        ACTIVATE = 1
        MINT = 2
        UNLOCK = 3
        EXECUTE = 4
        COLLECT = 5

    class StateVar(Ctrt.StateVar):
        """
        StateVar is the enum class for state variables of a contract.
        """

        MAKER = 0
        BASE_TOKEN_ID = 1
        TARGET_TOKEN_ID = 2
        OPTION_TOKEN_ID = 3
        PROOF_TOKEN_ID = 4
        EXECUTE_TIME = 5
        EXECUTE_DEADLINE = 6
        OPTION_STATUS = 7
        MAX_ISSUE_NUM = 8
        RESERVED_OPTION = 9
        RESERVED_PROOF = 10
        PRICE = 11
        PRICE_UNIT = 12
        TOKEN_LOCKED = 13
        TOKEN_COLLECTED = 14

    class StateMapIdx(Ctrt.StateMapIdx):
        """
        StateMapIdx is the enum class for state map indexes.
        """

        BASE_TOKEN_BALANCE = 0
        TARGET_TOKEN_BALANCE = 1
        OPTION_TOKEN_BALANCE = 2
        PROOF_TOKEN_BALANCE = 3

    class DBKey(Ctrt.DBKey):
        """
        DBKey is the class for DB key of a contract used to query data.
        """

        # state var.
        @classmethod
        def for_maker(cls) -> VOptionCtrt.DBKey:
            """
            for_maker returns the VOptionCtrt.DBKey object for querying the maker.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateVar.MAKER.serialize()
            return cls(b)

        @classmethod
        def for_base_token_id(cls) -> VOptionCtrt.DBKey:
            """
            for_base_token_id returns the VOptionCtrt.DBKey object for querying the base token id.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateVar.BASE_TOKEN_ID.serialize()
            return cls(b)

        @classmethod
        def for_target_token_id(cls) -> VOptionCtrt.DBKey:
            """
            for_target_token_id returns the VOptionCtrt.DBKey object for querying the target token id.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateVar.TARGET_TOKEN_ID.serialize()
            return cls(b)

        @classmethod
        def for_option_token_id(cls) -> VOptionCtrt.DBKey:
            """
            for_option_token_id returns the VOptionCtrt.DBKey object for querying the option token id.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateVar.OPTION_TOKEN_ID.serialize()
            return cls(b)

        @classmethod
        def for_proof_token_id(cls) -> VOptionCtrt.DBKey:
            """
            for_proof_token_id returns the VOptionCtrt.DBKey object for querying the proof token id.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateVar.PROOF_TOKEN_ID.serialize()
            return cls(b)

        @classmethod
        def for_execute_time(cls) -> VOptionCtrt.DBKey:
            """
            for_execute_time returns the VOptionCtrt.DBKey object for querying the execute time.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateVar.EXECUTE_TIME.serialize()
            return cls(b)

        @classmethod
        def for_execute_deadline(cls) -> VOptionCtrt.DBKey:
            """
            for_execute_deadline returns the VOptionCtrt.DBKey object for querying the execute deadline.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateVar.EXECUTE_DEADLINE.serialize()
            return cls(b)

        @classmethod
        def for_option_status(cls) -> VOptionCtrt.DBKey:
            """
            for_option_status returns the VOptionCtrt.DBKey object for querying the option contract's status.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateVar.OPTION_STATUS.serialize()
            return cls(b)

        @classmethod
        def for_max_issue_num(cls) -> VOptionCtrt.DBKey:
            """
            for_max_issue_num returns the VOptionCtrt.DBKey object for querying the maximum issue of the option tokens.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateVar.MAX_ISSUE_NUM.serialize()
            return cls(b)

        @classmethod
        def for_reserved_option(cls) -> VOptionCtrt.DBKey:
            """
            for_reserved_option returns the VOptionCtrt.DBKey object for querying the reserved amount of option tokens in the pool.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateVar.RESERVED_OPTION.serialize()
            return cls(b)

        @classmethod
        def for_reserved_proof(cls) -> VOptionCtrt.DBKey:
            """
            for_reserved_proof returns the VOptionCtrt.DBKey object for querying the reserved amount of proof tokens in the pool.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateVar.RESERVED_PROOF.serialize()
            return cls(b)

        @classmethod
        def for_price(cls) -> VOptionCtrt.DBKey:
            """
            for_price returns the VOptionCtrt.DBKey object for querying the price of the contract creator.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateVar.PRICE.serialize()
            return cls(b)

        @classmethod
        def for_price_unit(cls) -> VOptionCtrt.DBKey:
            """
            for_price_unit returns the VOptionCtrt.DBKey object for querying the price unit of the contract creator.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateVar.PRICE_UNIT.serialize()
            return cls(b)

        @classmethod
        def for_token_locked(cls) -> VOptionCtrt.DBKey:  # not sure about the type
            """
            for_token_locked returns the VOptionCtrt.DBKey object for querying the address of the contract creator.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateVar.TOKEN_LOCKED.serialize()
            return cls(b)

        @classmethod
        def for_token_collected(cls) -> VOptionCtrt.DBKey:
            """
            for_token_collected returns the VOptionCtrt.DBKey object for querying the amount of base tokens in the pool.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateVar.TOKEN_COLLECTED.serialize()
            return cls(b)

        # state map.
        @classmethod
        def for_base_token_balance(cls, addr: str) -> VOptionCtrt.DBKey:
            """
            for_base_token_balance returns the VOptionCtrt.DBKey object for querying the base token balance of the user.

            Args:
                addr (str): The address of the account that owns the base token.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateMap(
                idx=VOptionCtrt.StateMapIdx.BASE_TOKEN_BALANCE,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

        @classmethod
        def for_target_token_balance(cls, addr: str) -> VOptionCtrt.DBKey:
            """
            for_target_token_balance returns the VOptionCtrt.DBKey object for querying the target token balance of the user.

            Args:
                addr (str): The address of the account that owns the target token.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateMap(
                idx=VOptionCtrt.StateMapIdx.TARGET_TOKEN_BALANCE,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

        @classmethod
        def for_option_token_balance(cls, addr: str) -> VOptionCtrt.DBKey:
            """
            for_option_token_balance returns the VOptionCtrt.DBKey object for querying the option token balance of the user.

            Args:
                addr (str): The address of the account that owns the option token.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateMap(
                idx=VOptionCtrt.StateMapIdx.OPTION_TOKEN_BALANCE,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

        @classmethod
        def for_proof_token_balance(cls, addr: str) -> VOptionCtrt.DBKey:
            """
            for_proof_token_balance returns the VOptionCtrt.DBKey object for querying the proof token balance of the user.

            Args:
                addr (str): The address of the account that owns the proof token.

            Returns:
                VOptionCtrt.DBKey: The VOptionCtrt.DBKey object.
            """
            b = VOptionCtrt.StateMap(
                idx=VOptionCtrt.StateMapIdx.PROOF_TOKEN_BALANCE,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

    @property
    async def maker(self) -> str:
        """
        maker queries & returns the maker of the contract.

        Returns:
            str: The address of the maker of the contract.
        """
        return await self._query_db_key(self.DBKey.for_maker())

    @property
    async def base_token_id(self) -> md.TokenID:
        """
        base_token_id queries & returns the base token id.

        Returns:
            str: The base token id.
        """
        return await self._query_db_key(self.DBKey.for_base_token_id())

    @property
    async def target_token_id(self) -> str:
        """
        target_token_id queries & returns the target token id.

        Returns:
            str: The target token id.
        """
        return await self._query_db_key(self.DBKey.for_target_token_id())

    @property
    async def option_token_id(self) -> md.TokenID:
        """
        option_token_id queries & returns the option token id.

        Returns:
            str: The option token id.
        """
        return await self._query_db_key(self.DBKey.for_option_token_id())

    @property
    async def proof_token_id(self) -> str:
        """
        proof_token_id queries & returns the proof token id.

        Returns:
            str: The proof token id.
        """
        return await self._query_db_key(self.DBKey.for_proof_token_id())

    @property
    async def execute_time(self) -> str:
        """
        execute_time queries & returns the execute time.

        Returns:
            str: The execute time.
        """
        return await self._query_db_key(self.DBKey.for_execute_time())

    @property
    async def execute_deadline(self) -> str:
        """
        execute_time queries & returns the execute time.

        Returns:
            str: The execute time.
        """
        return await self._query_db_key(self.DBKey.for_execute_deadline())

    @property
    async def option_status(self) -> str:
        """
        execute_time queries & returns the option contract's status.

        Returns:
            str: The option contract's status.
        """
        return await self._query_db_key(self.DBKey.for_option_status())

    @property
    async def max_issue_num(self) -> md.Token:
        """
        max_issue_num queries & returns the maximum issue of the option tokens.

        Returns:
            str: The maximum issue of the option tokens.
        """
        a = await self._query_db_key(self.DBKey.for_max_issue_num())
        return md.Token.for_amount(a, await self.base_tok_unit)

    @property
    async def reserved_option(self) -> str:
        """
        reserved_option queries & returns the reserved option tokens remaining in the pool.

        Returns:
            str: The reserved option tokens remaining in the pool.
        """
        return await self._query_db_key(self.DBKey.for_reserved_option())

    @property
    async def reserved_proof(self) -> str:
        """
        reserved_proof queries & returns the reserved proof tokens remaining in the pool.

        Returns:
            str: The reserved proof tokens remaining in the pool.
        """
        return await self._query_db_key(self.DBKey.for_reserved_proof())

    @property
    async def price(self) -> str:
        """
        price queries & returns the price of the contract creator.

        Returns:
            str: The price of the contract creator.
        """
        a = await self._query_db_key(self.DBKey.for_price())
        b = md.Token(a)
        return b.data

    @property
    async def price_unit(self) -> md.Token:
        """
        price_unit queries & returns the price unit of the contract creator.

        Returns:
            str: The price unit of the contract creator.
        """
        a = await self._query_db_key(self.DBKey.for_price_unit())
        return md.Token(a)

    @property
    async def token_locked(self) -> md.Token:
        """
        token_locked queries & returns the locked token amount.

        Returns:
            md.Addr: The lock token amount.
        """
        a = await self._query_db_key(self.DBKey.for_token_locked())
        return md.Token(a, await self.target_tok_unit)

    @property
    async def token_collected(self) -> md.Token:
        """
        token_collected queries & returns the amount of the base tokens in the pool.

        Returns:
            md.Addr: The amount of the base tokens in the pool.
        """
        a = await self._query_db_key(self.DBKey.for_token_collected())
        return md.Token(a)

    @property
    async def base_tok_unit(self) -> int:
        """
        base_tok_unit queries & return the unit of base token.

        Returns:
            int: The unit of base token.
        """
        tok_a_id = await self.base_token_id
        data = await self.chain.api.ctrt.get_tok_info(tok_a_id)
        return data["unity"]

    @property
    async def target_tok_unit(self) -> int:
        """
        target_tok_unit queries & return the unit of target token.

        Returns:
            int: The unit of target token.
        """
        tok_b_id = await self.target_token_id
        data = await self.chain.api.ctrt.get_tok_info(tok_b_id)
        return data["unity"]

    @property
    async def option_tok_unit(self) -> int:
        """
        option_tok_unit queries & return the unit of option token.

        Returns:
            int: The unit of option token.
        """
        tok_c_id = await self.option_token_id
        data = await self.chain.api.ctrt.get_tok_info(tok_c_id)
        return data["unity"]

    @property
    async def proof_tok_unit(self) -> int:
        """
        proof_tok_unit queries & return the unit of proof token.

        Returns:
            int: The unit of proof token.
        """
        tok_d_id = await self.proof_token_id
        data = await self.chain.api.ctrt.get_tok_info(tok_d_id)
        return data["unity"]

    async def get_base_tok_bal(self, addr: str) -> md.Token:
        """
        get_base_tok_bal queries & returns the balance of the available base tokens.

        Args:
            addr (str): The account address that deposits the token.

        Returns:
            md.Token: The balance of the base token.
        """
        bal = await self._query_db_key(self.DBKey.for_base_token_balance(addr))

        return md.Token.for_amount(bal, await self.base_tok_unit)

    async def get_target_tok_bal(self, addr: str) -> md.Token:
        """
        get_target_tok_bal queries & returns the balance of the available target tokens.

        Args:
            addr (str): The account address that deposits the token.

        Returns:
            md.Token: The balance of the target token.
        """
        bal = await self._query_db_key(self.DBKey.for_target_token_balance(addr))
        return md.Token.for_amount(bal, await self.target_tok_unit)

    async def get_option_tok_bal(self, addr: str) -> md.Token:
        """
        get_option_tok_bal queries & returns the balance of the available option tokens.

        Args:
            addr (str): The account address that deposits the token.

        Returns:
            md.Token: The balance of the option token.
        """
        bal = await self._query_db_key(self.DBKey.for_option_token_balance(addr))

        return md.Token.for_amount(bal, await self.base_tok_unit)

    async def get_proof_tok_bal(self, addr: str) -> md.Token:
        """
        get_proof_tok_bal queries & returns the balance of the available proof tokens.

        Args:
            addr (str): The account address that deposits the token.

        Returns:
            md.Token: The balance of the proof token.
        """
        bal = await self._query_db_key(self.DBKey.for_proof_token_balance(addr))
        return md.Token.for_amount(bal, await self.proof_tok_unit)

    @classmethod
    async def register(
        cls,
        by: acnt.Account,
        base_tok_id: str,
        target_tok_id: str,
        option_tok_id: str,
        proof_tok_id: str,
        execute_time: int,
        execute_deadline: int,
        ctrt_description: str = "",
        fee: int = md.RegCtrtFee.DEFAULT,
    ) -> VOptionCtrt:
        """
        register registers a v option contract.

        Args:
            by (acnt.Account): The action maker.
            base_tok_id (str): The base token id.
            target_token_id (str): The target token id.
            option_tok_id (str): The option token id.
            proof_token_id (str): The proof token id.
            max_order_per_user (Union[int, float]): The max order number that per user can create.
            unit_price_base (Union[int, float]): The unit price of the base token.
            unit_price_target (Union[int, float]): The unit price of the target token.

        Returns:
            VOptionCtrt: The VOptionCtrt object of the registered V Option contract.
        """
        # a = await by.chain.api.ctrt.get_tok_info(base_tok_id)
        # base_unit = a["unity"]
        # b = await by.chain.api.ctrt.get_tok_info(target_tok_id)
        # target_unit = b["unity"]
        # c = await by.chain.api.ctrt.get_tok_info(option_tok_id)
        # base_unit = a["unity"]
        # b = await by.chain.api.ctrt.get_tok_info(proof_tok_id)
        # target_unit = b["unity"]

        data = await by._register_contract(
            tx.RegCtrtTxReq(
                data_stack=de.DataStack(
                    de.TokenID(md.TokenID(base_tok_id)),
                    de.TokenID(md.TokenID(target_tok_id)),
                    de.TokenID(md.TokenID(option_tok_id)),
                    de.TokenID(md.TokenID(proof_tok_id)),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(execute_time)),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(execute_deadline)),
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

    async def supersede(
        self,
        by: acnt.Account,
        new_owner: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, any]:
        """
        supersede transfers the ownership of the contract to another account

        Args:
            by (acnt.Account): The action taker
            new_owner (int): The new owner of the contract
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str,any]: The response returned by the Node API
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SUPERSEDE,
                data_stack=de.DataStack(de.Addr(md.Addr(new_owner))),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def activate(
        self,
        by: acnt.Account,
        max_issue_num: Union[int, float],
        price: Union[int, float],
        price_unit: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, any]:
        """
        activate activates the V Option contract to store option token and proof token into the pool.

        Args:
            by (acnt.Account): The action taker
            max_issue_num Union[int, float]: The number of the maximum issue of the option tokens.
            price (Union[int, float]): The price of the creator of the V Option contract
            price_unit Union[int, float]: The price unit of the creator of the V Option contract
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str,any]: The response returned by the Node API
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.ACTIVATE,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(max_issue_num, await self.option_tok_unit),
                    de.Amount.for_tok_amount(price, await self.option_tok_unit),
                    de.Amount.for_tok_amount(price_unit, await self.option_tok_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def mint(
        self,
        by: acnt.Account,
        amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, any]:
        """
        mint mints target tokens into the pool to get option tokens and proof tokens.

        Args:
            by (acnt.Account): The action taker
            amount Union[int, float]: The mint amount.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str,any]: The response returned by the Node API
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.MINT,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount, await self.target_tok_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def unlock(
        self,
        by: acnt.Account,
        amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, any]:
        """
        unlock gets the remaining option tokens and proof tokens from the pool before the execute time.

        Args:
            by (acnt.Account): The action taker
            amount Union[int, float]: The amount.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str,any]: The response returned by the Node API
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.UNLOCK,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount, await self.target_tok_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def execute(
        self,
        by: acnt.Account,
        amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, any]:
        """
        execute executes the V Option contract to get target token after execute time.

        Args:
            by (acnt.Account): The action taker
            amount Union[int, float]: The amount.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str,any]: The response returned by the Node API
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.EXECUTE,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount, await self.target_tok_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def collect(
        self,
        by: acnt.Account,
        amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, any]:
        """
        collect collects the base tokens or/and target tokens from the pool depending on the amount of proof tokens after execute deadline.

        Args:
            by (acnt.Account): The action taker
            amount Union[int, float]: The amount.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str,any]: The response returned by the Node API
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.COLLECT,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount, await self.option_tok_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data
