"""
v_stable_swap_ctrt contains V Stable Swap contract.
"""
from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Dict, Union, Optional

from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_vsys import account as acnt
    from py_vsys import chain as ch

from py_vsys import data_entry as de
from py_vsys import tx_req as tx
from py_vsys import model as md
from py_vsys.contract import tok_ctrt_factory as tcf
from . import Ctrt, BaseTokCtrt


class VStableSwapCtrt(Ctrt):
    """
    VStableSwapCtrt is the class for VSYS V Stable Swap contract.
    """

    CTRT_META = md.CtrtMeta.from_b58_str(
        "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"
    )

    class FuncIdx(Ctrt.FuncIdx):
        """
        FuncIdx is the enum class for function indexes of a contract.
        """

        SUPERSEDE = 0
        SET_ORDER = 1
        UPDATE_ORDER = 2
        ORDER_DEPOSIT = 3
        ORDER_WITHDRAW = 4
        CLOSE_ORDER = 5
        SWAP_BASE_TO_TARGET = 6
        SWAP_TARGET_TO_BASE = 7

    class StateVar(Ctrt.StateVar):
        """
        StateVar is the enum class for state variables of a contract.
        """

        MAKER = 0
        BASE_TOKEN_ID = 1
        TARGET_TOKEN_ID = 2
        MAX_ORDER_PER_USER = 3
        UNIT_PRICE_BASE = 4
        UNIT_PRICE_TARGET = 5

    class StateMapIdx(Ctrt.StateMapIdx):
        """
        StateMapIdx is the enum class for state map indexes.
        """

        BASE_TOKEN_BALANCE = 0
        TARGET_TOKEN_BALANCE = 1
        USER_ORDERS = 2
        ORDER_OWNER = 3
        FEE_BASE = 4
        FEE_TARGET = 5
        MIN_BASE = 6
        MAX_BASE = 7
        MIN_TARGET = 8
        MAX_TARGET = 9
        PRICE_BASE = 10
        PRICE_TARGET = 11
        BASE_TOKEN_LOCKED = 12
        TARGET_TOKEN_LOCKED = 13
        ORDER_STATUS = 14

    class DBKey(Ctrt.DBKey):
        """
        DBKey is the class for DB key of a contract used to query data.
        """

        # state var.
        @classmethod
        def for_maker(cls) -> VStableSwapCtrt.DBKey:
            """
            for_maker returns the VStableSwapCtrt.DBKey object for querying the maker.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateVar.MAKER.serialize()
            return cls(b)

        @classmethod
        def for_base_token_id(cls) -> VStableSwapCtrt.DBKey:
            """
            for_base_token_id returns the VStableSwapCtrt.DBKey object for querying the base token id.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateVar.BASE_TOKEN_ID.serialize()
            return cls(b)

        @classmethod
        def for_target_token_id(cls) -> VStableSwapCtrt.DBKey:
            """
            for_target_token_id returns the VStableSwapCtrt.DBKey object for querying the target token id.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateVar.TARGET_TOKEN_ID.serialize()
            return cls(b)

        @classmethod
        def for_max_order_per_user(cls) -> VStableSwapCtrt.DBKey:
            """
            for_max_order_per_user returns the VStableSwapCtrt.DBKey object for querying the max order number per user.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateVar.MAX_ORDER_PER_USER.serialize()
            return cls(b)

        @classmethod
        def for_base_price_unit(cls) -> VStableSwapCtrt.DBKey:
            """
            for_base_price_unit returns the VStableSwapCtrt.DBKey object for querying the unit of base token price.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateVar.UNIT_PRICE_BASE.serialize()
            return cls(b)

        @classmethod
        def for_target_price_unit(cls) -> VStableSwapCtrt.DBKey:
            """
            for_target_price_unit returns the VStableSwapCtrt.DBKey object for querying the unit of target token price.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateVar.UNIT_PRICE_TARGET.serialize()
            return cls(b)

        # state map.
        @classmethod
        def for_base_token_balance(cls, addr: str) -> VStableSwapCtrt.DBKey:
            """
            for_base_token_balance returns the VStableSwapCtrt.DBKey object for querying the base token balance.

            Args:
                addr (str): The address of the account that owns the base token.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateMap(
                idx=VStableSwapCtrt.StateMapIdx.BASE_TOKEN_BALANCE,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

        @classmethod
        def for_target_token_balance(cls, addr: str) -> VStableSwapCtrt.DBKey:
            """
            for_target_token_balance returns the VStableSwapCtrt.DBKey object for querying the target token balance.

            Args:
                addr (str): The address of the account that owns the target token.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateMap(
                idx=VStableSwapCtrt.StateMapIdx.TARGET_TOKEN_BALANCE,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

        @classmethod
        def for_user_orders(cls, addr: str) -> VStableSwapCtrt.DBKey:
            """
            for_user_orders returns the VStableSwapCtrt.DBKey object for querying the number of orders of the user's.

            Args:
                addr (str): The address of the account that create the orders.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateMap(
                idx=VStableSwapCtrt.StateMapIdx.USER_ORDERS,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_owner(cls, order_id: str) -> VStableSwapCtrt.DBKey:
            """
            for_order_owner returns the VStableSwapCtrt.DBKey object for querying the order owner.

            Args:
                order_id (str): The order id.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateMap(
                idx=VStableSwapCtrt.StateMapIdx.ORDER_OWNER,
                data_entry=de.Bytes.from_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_fee_base(cls, order_id: str) -> VStableSwapCtrt.DBKey:
            """
            for_fee_base returns the VStableSwapCtrt.DBKey object for querying the base fee.

            Args:
                order_id (str): The order id.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateMap(
                idx=VStableSwapCtrt.StateMapIdx.FEE_BASE,
                data_entry=de.Bytes.from_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_fee_target(cls, order_id: str) -> VStableSwapCtrt.DBKey:
            """
            for_fee_target returns the VStableSwapCtrt.DBKey object for querying the target fee.

            Args:
                order_id (str): The order id.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateMap(
                idx=VStableSwapCtrt.StateMapIdx.FEE_TARGET,
                data_entry=de.Bytes.from_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_min_base(cls, order_id: str) -> VStableSwapCtrt.DBKey:
            """
            for_min_base returns the VStableSwapCtrt.DBKey object for querying the minimum value of base.

            Args:
                order_id (str): The order id.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateMap(
                idx=VStableSwapCtrt.StateMapIdx.MIN_BASE,
                data_entry=de.Bytes.from_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_max_base(cls, order_id: str) -> VStableSwapCtrt.DBKey:
            """
            for_max_base returns the VStableSwapCtrt.DBKey object for querying the maximum value of base.

            Args:
                order_id (str): The order id.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateMap(
                idx=VStableSwapCtrt.StateMapIdx.MAX_BASE,
                data_entry=de.Bytes.from_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_min_target(cls, order_id: str) -> VStableSwapCtrt.DBKey:
            """
            for_min_target returns the VStableSwapCtrt.DBKey object for querying the minimum trade value of target.

            Args:
                order_id (str): The order id.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateMap(
                idx=VStableSwapCtrt.StateMapIdx.MIN_TARGET,
                data_entry=de.Bytes.from_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_max_target(cls, order_id: str) -> VStableSwapCtrt.DBKey:
            """
            for_max_target returns the VStableSwapCtrt.DBKey object for querying the maximum trade value of target.

            Args:
                order_id (str): The order id.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateMap(
                idx=VStableSwapCtrt.StateMapIdx.MAX_TARGET,
                data_entry=de.Bytes.from_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_price_base(cls, order_id: str) -> VStableSwapCtrt.DBKey:
            """
            for_price_base returns the VStableSwapCtrt.DBKey object for querying the price of base token.

            Args:
                order_id (str): The order id.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateMap(
                idx=VStableSwapCtrt.StateMapIdx.PRICE_BASE,
                data_entry=de.Bytes.from_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_price_target(cls, order_id: str) -> VStableSwapCtrt.DBKey:
            """
            for_price_target returns the VStableSwapCtrt.DBKey object for querying the price of target token.

            Args:
                order_id (str): The order id.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateMap(
                idx=VStableSwapCtrt.StateMapIdx.PRICE_TARGET,
                data_entry=de.Bytes.from_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_base_token_locked(cls, order_id: str) -> VStableSwapCtrt.DBKey:
            """
            for_base_token_locked returns the VStableSwapCtrt.DBKey object for querying the locked base token.

            Args:
                order_id (str): The order id.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateMap(
                idx=VStableSwapCtrt.StateMapIdx.BASE_TOKEN_LOCKED,
                data_entry=de.Bytes.from_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_target_token_locked(cls, order_id: str) -> VStableSwapCtrt.DBKey:
            """
            for_target_token_locked returns the VStableSwapCtrt.DBKey object for querying the locked target token.

            Args:
                order_id (str): The order id.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateMap(
                idx=VStableSwapCtrt.StateMapIdx.TARGET_TOKEN_LOCKED,
                data_entry=de.Bytes.from_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_status(cls, order_id: str) -> VStableSwapCtrt.DBKey:
            """
            for_order_status returns the VStableSwapCtrt.DBKey object for querying the order status.

            Args:
                order_id (str): The order id.

            Returns:
                VStableSwapCtrt.DBKey: The VStableSwapCtrt.DBKey object.
            """
            b = VStableSwapCtrt.StateMap(
                idx=VStableSwapCtrt.StateMapIdx.ORDER_STATUS,
                data_entry=de.Bytes.from_base58_str(order_id),
            ).serialize()
            return cls(b)

    def __init__(self, ctrt_id: str, chain: ch.Chain) -> None:
        """
        Args:
            ctrt_id (str): The id of the contract.
            chain (ch.Chain): The object of the chain where the contract is on.
        """
        self._ctrt_id = md.CtrtID(ctrt_id)
        self._chain = chain

        self._base_tok_id: Optional[md.TokenID] = None
        self._target_tok_id: Optional[md.TokenID] = None

        self._base_tok_ctrt: Optional[BaseTokCtrt] = None
        self._target_tok_ctrt: Optional[BaseTokCtrt] = None

    @property
    async def maker(self) -> md.Addr:
        """
        maker queries & returns the maker of the contract.

        Returns:
            md.Addr: The address of the maker of the contract.
        """
        raw_val = await self._query_db_key(self.DBKey.for_maker())
        return md.Addr(raw_val)

    @property
    async def base_tok_id(self) -> md.TokenID:
        """
        base_tok_id queries & returns the base token id.

        Returns:
            md.TokenID: The base token id.
        """
        if not self._base_tok_id:
            raw_val = await self._query_db_key(self.DBKey.for_base_token_id())
            self._base_tok_id = md.TokenID(raw_val)
        return self._base_tok_id

    @property
    async def target_tok_id(self) -> md.TokenID:
        """
        target_tok_id queries & returns the target token id.

        Returns:
            md.TokenID: The target token id.
        """
        if not self._target_tok_id:
            raw_val = await self._query_db_key(self.DBKey.for_target_token_id())
            self._target_tok_id = md.TokenID(raw_val)
        return self._target_tok_id

    @property
    async def base_tok_ctrt(self) -> BaseTokCtrt:
        """
        base_tok_ctrt returns the token contract instance for base token.

        Returns:
            BaseTokCtrt: The token contract intance.
        """
        if not self._base_tok_ctrt:
            base_tok_id = await self.base_tok_id
            self._base_tok_ctrt = await tcf.from_tok_id(base_tok_id, self.chain)
        return self._base_tok_ctrt

    @property
    async def target_tok_ctrt(self) -> BaseTokCtrt:
        """
        target_tok_ctrt returns the token contract instance for target token.

        Returns:
            BaseTokCtrt: The token contract intance.
        """
        if not self._target_tok_ctrt:
            target_tok_id = await self.target_tok_id
            self._target_tok_ctrt = await tcf.from_tok_id(target_tok_id, self.chain)
        return self._target_tok_ctrt

    @property
    async def base_tok_unit(self) -> int:
        """
        base_tok_unit queries & return the unit of base token.

        Returns:
            int: The unit of base token.
        """
        tc = await self.base_tok_ctrt
        return await tc.unit

    @property
    async def target_tok_unit(self) -> int:
        """
        target_tok_unit queries & return the unit of target token.

        Returns:
            int: The unit of target token.
        """
        tc = await self.target_tok_ctrt
        return await tc.unit

    @property
    async def max_order_per_user(self) -> int:
        """
        max_order_per_user queries & returns the max order number that each user can create.

        Returns:
            int: The max order number.
        """
        return await self._query_db_key(self.DBKey.for_max_order_per_user())

    @property
    async def base_price_unit(self) -> int:
        """
        base_price_unit queries & returns the price unit of base token.

        Returns:
            int: the price unit of base token.
        """
        return await self._query_db_key(self.DBKey.for_base_price_unit())

    @property
    async def target_price_unit(self) -> int:
        """
        target_price_unit queries & returns the price unit of target token.

        Returns:
            int: the price unit of target token.
        """
        return await self._query_db_key(self.DBKey.for_target_price_unit())

    async def get_base_tok_bal(self, addr: str) -> md.Token:
        """
        get_base_tok_bal queries & returns the balance of the available base tokens.

        Args:
            addr (str): The account address that deposits the token.

        Returns:
            md.Token: The balance of the token.
        """
        raw_val = await self._query_db_key(self.DBKey.for_base_token_balance(addr))
        return md.Token(raw_val, await self.base_tok_unit)

    async def get_target_tok_bal(self, addr: str) -> md.Token:
        """
        get_target_tok_bal queries & returns the balance of the available target tokens.

        Args:
            addr (str): The account address that deposits the token.

        Returns:
            md.Token: The balance of the token.
        """
        raw_val = await self._query_db_key(self.DBKey.for_target_token_balance(addr))
        return md.Token(raw_val, await self.target_tok_unit)

    async def get_user_orders(self, addr: str) -> int:
        """
        get_user_orders queries & returns the number of user orders.

        Args:
            addr (str): The account address.

        Returns:
            int: The number of user orders.
        """
        return await self._query_db_key(self.DBKey.for_user_orders(addr))

    async def get_order_owner(self, order_id: str) -> md.Addr:
        """
        get_order_owner queries & returns the address of the order owner.

        Args:
            order_id (str): The order id.

        Returns:
            md.Addr: The address of the order owner.
        """
        owner_addr = await self._query_db_key(self.DBKey.for_order_owner(order_id))
        return md.Addr(owner_addr)

    async def get_fee_base(self, order_id: str) -> md.Token:
        """
        get_fee_base queries & returns the fee for base token.

        Args:
            order_id (str): The order id.

        Returns:
            md.Token: The fee for base token..
        """
        fee_base = await self._query_db_key(self.DBKey.for_fee_base(order_id))
        return md.Token(fee_base, await self.base_tok_unit)

    async def get_fee_target(self, order_id: str) -> md.Token:
        """
        get_fee_target queries & returns the target fee.

        Args:
            order_id (str): The order id.

        Returns:
            md.Token: The target fee.
        """
        target_base = await self._query_db_key(self.DBKey.for_fee_target(order_id))
        return md.Token(target_base, await self.target_tok_unit)

    async def get_min_base(self, order_id: str) -> md.Token:
        """
        get_min_base queries & returns the minimum amount of base token.

        Args:
            order_id (str): The order id.

        Returns:
            md.Token: The minimum amount of base token.
        """
        min_base = await self._query_db_key(self.DBKey.for_min_base(order_id))
        return md.Token(min_base, await self.base_tok_unit)

    async def get_max_base(self, order_id: str) -> md.Token:
        """
        get_max_base queries & returns the maximum amount of base token.

        Args:
            order_id (str): The order id.

        Returns:
            md.Token: The maximum amount of base token.
        """
        max_base = await self._query_db_key(self.DBKey.for_max_base(order_id))
        return md.Token(max_base, await self.base_tok_unit)

    async def get_min_target(self, order_id: str) -> md.Token:
        """
        get_min_target queries & returns the minimum amount of target token.

        Args:
            order_id (str): The order id.

        Returns:
            md.Token: The minimum amount of target token.
        """
        min_target = await self._query_db_key(self.DBKey.for_min_target(order_id))
        return md.Token(min_target, await self.target_tok_unit)

    async def get_max_target(self, order_id: str) -> md.Token:
        """
        get_max_target queries & returns the maximum amount of target token.

        Args:
            order_id (str): The order id.

        Returns:
            md.Token: The maximum amount of target token.
        """
        max_target = await self._query_db_key(self.DBKey.for_max_target(order_id))
        return md.Token(max_target, await self.target_tok_unit)

    async def get_price_base(self, order_id: str) -> md.Token:
        """
        get_price_base queries & returns the price of base token.

        Args:
            order_id (str): The order id.

        Returns:
            md.Addr: The price of the base token.
        """
        price_base = await self._query_db_key(self.DBKey.for_price_base(order_id))
        return md.Token(price_base, await self.base_price_unit)

    async def get_price_target(self, order_id: str) -> md.Token:
        """
        get_price_target queries & returns the price of target token.

        Args:
            order_id (str): The order id.

        Returns:
            md.Token: The price of the target token.
        """
        price_target = await self._query_db_key(self.DBKey.for_price_target(order_id))
        return md.Token(price_target, await self.target_price_unit)

    async def get_base_tok_locked(self, order_id: str) -> md.Token:
        """
        get_base_tok_locked queries & returns the locked balance of base token.

        Args:
            order_id (str): The order id.

        Returns:
            md.Token: The balance of locked base token.
        """
        raw_val = await self._query_db_key(self.DBKey.for_base_token_locked(order_id))
        return md.Token(raw_val, await self.base_tok_unit)

    async def get_target_tok_locked(self, order_id: str) -> md.Token:
        """
        get_target_tok_locked queries & returns the locked balance of target token.

        Args:
            order_id (str): The order id.

        Returns:
            md.Token: The balance of locked target token.
        """
        raw_val = await self._query_db_key(self.DBKey.for_target_token_locked(order_id))
        return md.Token(raw_val, await self.target_tok_unit)

    async def get_order_status(self, order_id: str) -> bool:
        """
        get_order_status queries & returns the order status.

        Args:
            order_id (str): The order id.

        Returns:
            bool: The order status.
        """
        status = await self._query_db_key(self.DBKey.for_order_status(order_id))
        return status == "true"

    @classmethod
    async def register(
        cls,
        by: acnt.Account,
        base_tok_id: str,
        target_tok_id: str,
        max_order_per_user: int,
        base_price_unit: int,
        target_price_unit: int,
        ctrt_description: str = "",
        fee: int = md.RegCtrtFee.DEFAULT,
    ) -> VStableSwapCtrt:
        """
        register registers a v stable swap contract.

        Args:
            by (acnt.Account): The action taker.
            base_tok_id (str): The base token id.
            target_tok_id (str): The target token id.
            max_order_per_user (int): The max order number that per user can create.
            base_price_unit (int): The unit of price of the base token.
            target_price_unit (int): The unit of price of the target token.
            ctrt_description (str, optional): The description of the contract. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.RegCtrtFee.DEFAULT.

        Returns:
            VStableSwapCtrt: The VStableSwapCtrt object of the registered Stable Swap contract.
        """
        data = await by._register_contract(
            tx.RegCtrtTxReq(
                data_stack=de.DataStack(
                    de.TokenID(md.TokenID(base_tok_id)),
                    de.TokenID(md.TokenID(target_tok_id)),
                    de.Amount(md.Int(max_order_per_user)),
                    de.Amount(md.Int(base_price_unit)),
                    de.Amount(md.Int(target_price_unit)),
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
            new_owner (str): The new owner of the contract
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

    async def set_order(
        self,
        by: acnt.Account,
        fee_base: Union[int, float],
        fee_target: Union[int, float],
        min_base: Union[int, float],
        max_base: Union[int, float],
        min_target: Union[int, float],
        max_target: Union[int, float],
        price_base: Union[int, float],
        price_target: Union[int, float],
        base_deposit: Union[int, float],
        target_deposit: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, any]:
        """
        set_order creates the order.

        Args:
            by (acnt.Account): The action taker.
            fee_base (Union[int, float]): The fee of base token.
            fee_target (Union[int, float]): The fee of target token.
            min_base (Union[int, float]): The minimum value of base token.
            max_base (Union[int, float]): The maximum value of base token.
            min_target (Union[int, float]): The minimum value of target token.
            max_target (Union[int, float]): The maximum value of target token.
            price_base (Union[int, float]): The price of base token.
            price_target (Union[int, float]): The price of target token.
            base_deposit (Union[int, float]): The balance that base token deposits.
            target_deposit (Union[int, float]): The balance that target token deposits.
            attachment (str, optional): Defaults to "".
            fee (int, optional): Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, any]: The response returned by the Node API.
        """
        base_unit = await self.base_tok_unit
        target_unit = await self.target_tok_unit

        base_price_unit = await self.base_price_unit
        target_price_unit = await self.target_price_unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SET_ORDER,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(fee_base, base_unit),
                    de.Amount.for_tok_amount(fee_target, target_unit),
                    de.Amount.for_tok_amount(min_base, base_unit),
                    de.Amount.for_tok_amount(max_base, base_unit),
                    de.Amount.for_tok_amount(min_target, target_unit),
                    de.Amount.for_tok_amount(max_target, target_unit),
                    de.Amount.for_tok_amount(price_base, base_price_unit),
                    de.Amount.for_tok_amount(price_target, target_price_unit),
                    de.Amount.for_tok_amount(base_deposit, base_unit),
                    de.Amount.for_tok_amount(target_deposit, target_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def update_order(
        self,
        by: acnt.Account,
        order_id: str,
        fee_base: Union[int, float],
        fee_target: Union[int, float],
        min_base: Union[int, float],
        max_base: Union[int, float],
        min_target: Union[int, float],
        max_target: Union[int, float],
        price_base: Union[int, float],
        price_target: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, any]:
        """
        update_order updates the order settings.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order id.
            fee_base (Union[int, float]): The fee of base token.
            fee_target (Union[int, float]): The fee of target token.
            min_base (Union[int, float]): The minimum base token.
            max_base (Union[int, float]): The maximum base token.
            min_target (Union[int, float]): The minimum target token.
            max_target (Union[int, float]): The maximum target token.
            price_base (Union[int, float]): The price of base token.
            price_target (Union[int, float]): The price of target token.
            attachment (str, optional): Defaults to "".
            fee (int, optional): Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, any]: The response returned by the Node API.
        """
        base_unit = await self.base_tok_unit
        target_unit = await self.target_tok_unit

        base_price_unit = await self.base_price_unit
        target_price_unit = await self.target_price_unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.UPDATE_ORDER,
                data_stack=de.DataStack(
                    de.Bytes.from_base58_str(order_id),
                    de.Amount.for_tok_amount(fee_base, base_unit),
                    de.Amount.for_tok_amount(fee_target, target_unit),
                    de.Amount.for_tok_amount(min_base, base_unit),
                    de.Amount.for_tok_amount(max_base, base_unit),
                    de.Amount.for_tok_amount(min_target, target_unit),
                    de.Amount.for_tok_amount(max_target, target_unit),
                    de.Amount.for_tok_amount(price_base, base_price_unit),
                    de.Amount.for_tok_amount(price_target, target_price_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def order_deposit(
        self,
        by: acnt.Account,
        order_id: str,
        base_deposit: Union[int, float],
        target_deposit: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, any]:
        """
        order_deposit locks the tokens.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order id.
            base_deposit (Union[int, float]): The balance that base token deposits.
            target_deposit (Union[int, float]): The balance that target token deposits.
            attachment (str, optional): Defaults to "".
            fee (int, optional): Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, any]: The response returned by the Node API.
        """
        base_unit = await self.base_tok_unit
        target_unit = await self.target_tok_unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.ORDER_DEPOSIT,
                data_stack=de.DataStack(
                    de.Bytes.from_base58_str(order_id),
                    de.Amount.for_tok_amount(base_deposit, base_unit),
                    de.Amount.for_tok_amount(target_deposit, target_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def order_withdraw(
        self,
        by: acnt.Account,
        order_id: str,
        base_withdraw: Union[int, float],
        target_withdraw: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, any]:
        """
        order_withdraw unlocks the tokens.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order id.
            base_withdraw (Union[int, float]): The balance that base token withdraws.
            target_withdraw (Union[int, float]): The balance that target token withdraws.
            attachment (str, optional): Defaults to "".
            fee (int, optional): Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, any]: The response returned by the Node API.
        """
        base_unit = await self.base_tok_unit
        target_unit = await self.target_tok_unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.ORDER_WITHDRAW,
                data_stack=de.DataStack(
                    de.Bytes.from_base58_str(order_id),
                    de.Amount.for_tok_amount(base_withdraw, base_unit),
                    de.Amount.for_tok_amount(target_withdraw, target_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def close_order(
        self,
        by: acnt.Account,
        order_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, any]:
        """
        close_order closes the order.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order id.
            attachment (str, optional): Defaults to "".
            fee (int, optional): Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.CLOSE_ORDER,
                data_stack=de.DataStack(
                    de.Bytes.from_base58_str(order_id),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def swap_base_to_target(
        self,
        by: acnt.Account,
        order_id: str,
        amount: Union[int, float],
        swap_fee: Union[int, float],
        price: Union[int, float],
        deadline: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, any]:
        """
        swap_base_to_target swaps base token to target token.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order id.
            amount (Union[int, float]): The swap amount.
            swap_fee (Union[int, float]): The swap fee.
            price (Union[int, float]): The price.
            deadline (int): The deadline timestamp of the swap.
            attachment (str, optional): Defaults to "".
            fee (int, optional): Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, any]: The response returned by the Node API.
        """
        base_unit = await self.base_tok_unit
        base_price_unit = await self.base_price_unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SWAP_BASE_TO_TARGET,
                data_stack=de.DataStack(
                    de.Bytes.from_base58_str(order_id),
                    de.Amount.for_tok_amount(amount, base_unit),
                    de.Amount.for_tok_amount(swap_fee, base_unit),
                    de.Amount.for_tok_amount(price, base_price_unit),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(deadline)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def swap_target_to_base(
        self,
        by: acnt.Account,
        order_id: str,
        amount: Union[int, float],
        swap_fee: Union[int, float],
        price: Union[int, float],
        deadline: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, any]:
        """
        swap_target_to_base swaps target token to base token.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order id.
            amount (Union[int, float]): The swap amount.
            swap_fee (Union[int, float]): The swap fee.
            price (Union[int, float]): The price.
            deadline (int): The deadline timestamp of the swap.
            attachment (str, optional): Defaults to "".
            fee (int, optional): Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, any]: The response returned by the Node API.
        """
        target_unit = await self.target_tok_unit
        target_price_unit = await self.target_price_unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SWAP_TARGET_TO_BASE,
                data_stack=de.DataStack(
                    de.Bytes.from_base58_str(order_id),
                    de.Amount.for_tok_amount(amount, target_unit),
                    de.Amount.for_tok_amount(swap_fee, target_unit),
                    de.Amount.for_tok_amount(price, target_price_unit),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(deadline)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data
