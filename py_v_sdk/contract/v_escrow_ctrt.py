"""
v_escrow_ctrt contains V Escrow contract.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict, Union, Optional

from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import account as acnt
    from py_v_sdk import chain as ch

from py_v_sdk import data_entry as de
from py_v_sdk import tx_req as tx
from py_v_sdk.contract import tok_ctrt_factory as tcf
from py_v_sdk import model as md
from . import CtrtMeta, Ctrt


class VEscrowCtrt(Ctrt):
    """
    VEscrowCtrt is the class for VSYS V Escrow contract.
    """

    CTRT_META = CtrtMeta.from_b58_str(
        "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"
    )

    class FuncIdx(Ctrt.FuncIdx):
        """
        FuncIdx is the enum class for function indexes of a contract.
        """

        SUPERSEDE = 0
        CREATE = 1
        RECIPIENT_DEPOSIT = 2
        JUDGE_DEPOSIT = 3
        PAYER_CANCEL = 4
        RECIPIENT_CANCEL = 5
        JUDGE_CANCEL = 6
        SUBMIT_WORK = 7
        APPROVE_WORK = 8
        APPLY_TO_JUDGE = 9
        JUDGE = 10
        SUBMIT_PENALTY = 11
        PAYER_REFUND = 12
        RECIPIENT_REFUND = 13
        COLLECT = 14

    class StateVar(Ctrt.StateVar):
        """
        StateVar is the enum class for state variables of a contract.
        """

        MAKER = 0
        JUDGE = 1
        TOKEN_ID = 2
        DURATION = 3
        JUDGE_DURATION = 4

    class StateMapIdx(Ctrt.StateMapIdx):
        """
        StateMapIdx is the enum class for state map indexes.
        """

        CONTRACT_BALANCE = 0
        ORDER_PAYER = 1
        ORDER_RECIPIENT = 2
        ORDER_AMOUNT = 3
        ORDER_RECIPIENT_DEPOSIT = 4
        ORDER_JUDGE_DEPOSIT = 5
        ORDER_FEE = 6
        ORDER_RECIPIENT_AMOUNT = 7
        ORDER_REFUND = 8
        ORDER_RECIPIENT_REFUND = 9
        ORDER_EXPIRATION_TIME = 10
        ORDER_STATUS = 11
        ORDER_RECIPIENT_DEPOSIT_STATUS = 12
        ORDER_JUDGE_DEPOSIT_STATUS = 13
        ORDER_SUBMIT_STATUS = 14
        ORDER_JUDGE_STATUS = 15
        ORDER_RECIPIENT_LOCKED_AMOUNT = 16
        ORDER_JUDGE_LOCKED_AMOUNT = 17

    class DBKey(Ctrt.DBKey):
        """
        DBKey is the class for DB key of a contract used to query data.
        """

        @classmethod
        def for_maker(cls) -> VEscrowCtrt.DBKey:
            """
            for_maker returns the VEscrowCtrt.DBKey object for querying
            the address of the maker of the contract.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateVar.MAKER.serialize()
            return cls(b)

        @classmethod
        def for_judge(cls) -> VEscrowCtrt.DBKey:
            """
            for_judge returns the VEscrowCtrt.DBKey object for querying
            the address of the judge of the contract.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateVar.JUDGE.serialize()
            return cls(b)

        @classmethod
        def for_token_id(cls) -> VEscrowCtrt.DBKey:
            """
            for_token_id returns the VEscrowCtrt.DBKey object for querying
            the token ID of the contract.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateVar.TOKEN_ID.serialize()
            return cls(b)

        @classmethod
        def for_duration(cls) -> VEscrowCtrt.DBKey:
            """
            for_duration returns the VEscrowCtrt.DBKey object for querying
            the duration where the recipient can take actions in the contract.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateVar.DURATION.serialize()
            return cls(b)

        @classmethod
        def for_judge_duration(cls) -> VEscrowCtrt.DBKey:
            """
            for_judge_duration returns the VEscrowCtrt.DBKey object for querying
            the duration where the judge can take actions in the contract.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateVar.JUDGE_DURATION.serialize()
            return cls(b)

        @classmethod
        def for_contract_balance(cls, addr: str) -> VEscrowCtrt.DBKey:
            """
            for_contract_balance returns the VEscrowCtrt.DBKey object for querying the contract balance.

            Args:
                addr (str): The account address.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.CONTRACT_BALANCE,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_payer(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_payer returns the VEscrowCtrt.DBKey object for querying
            the payer of the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_PAYER,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_recipient(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_recipient returns the VEscrowCtrt.DBKey object for querying
            the recipient of the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_RECIPIENT,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_amount(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_amount returns the VEscrowCtrt.DBKey object for querying
            the amount of the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_AMOUNT,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_recipient_deposit(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_recipient_deposit returns the VEscrowCtrt.DBKey object for querying
            the amount the recipient deposits in the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_RECIPIENT_DEPOSIT,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_judge_deposit(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_judge_deposit returns the VEscrowCtrt.DBKey object for querying
            the amount the judge deposits in the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_JUDGE_DEPOSIT,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_fee(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_fee returns the VEscrowCtrt.DBKey object for querying
            the fee of the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_FEE,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_recipient_amount(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_recipient_amount returns the VEscrowCtrt.DBKey object for querying
            the recipient amount of the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_RECIPIENT_AMOUNT,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_refund(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_refund returns the VEscrowCtrt.DBKey object for querying
            the refund amount of the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_REFUND,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_recipient_refund(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_recipient_refund returns the VEscrowCtrt.DBKey object for querying
            the recipient refund amount of the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_RECIPIENT_REFUND,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_expiration_time(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_expiration_time returns the VEscrowCtrt.DBKey object for querying
            the expiration time of the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_EXPIRATION_TIME,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_status(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_status returns the VEscrowCtrt.DBKey object for querying
            the status of the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_STATUS,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_recipient_deposit_status(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_recipient_deposit_status returns the VEscrowCtrt.DBKey object for querying
            the recipient deposit status of the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_RECIPIENT_DEPOSIT_STATUS,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_judge_deposit_status(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_judge_deposit_status returns the VEscrowCtrt.DBKey object for querying
            the judge deposit status of the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_JUDGE_DEPOSIT_STATUS,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_submit_status(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_submit_status returns the VEscrowCtrt.DBKey object for querying
            the submit status of the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_SUBMIT_STATUS,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_judge_status(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_judge_status returns the VEscrowCtrt.DBKey object for querying
            the judge status of the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_JUDGE_STATUS,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_recipient_locked_amount(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_recipient_locked_amount returns the VEscrowCtrt.DBKey object for querying
            the recipient locked amount of the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_RECIPIENT_LOCKED_AMOUNT,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

        @classmethod
        def for_order_judge_locked_amount(cls, order_id: str) -> VEscrowCtrt.DBKey:
            """
            for_order_judge_locked_amount returns the VEscrowCtrt.DBKey object for querying
            the judge locked amount of the order.

            Args:
                order_id (str): The order ID.

            Returns:
                VEscrowCtrt.DBKey: The VEscrowCtrt.DBKey object.
            """
            b = VEscrowCtrt.StateMap(
                idx=VEscrowCtrt.StateMapIdx.ORDER_JUDGE_LOCKED_AMOUNT,
                data_entry=de.Bytes.for_base58_str(order_id),
            ).serialize()
            return cls(b)

    def __init__(self, ctrt_id: str, chain: ch.Chain) -> None:
        """
        Args:
            ctrt_id (str): The id of the contract.
            chain (ch.Chain): The object of the chain where the contract is on.
        """
        super().__init__(ctrt_id, chain)
        self._tok_id: Optional[md.TokenID] = None

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
    async def judge(self) -> md.Addr:
        """
        judge queries & returns the judge of the contract.

        Returns:
            md.Addr: The address of the judge of the contract.
        """
        raw_val = await self._query_db_key(self.DBKey.for_judge())
        return md.Addr(raw_val)

    @property
    async def tok_id(self) -> md.TokenID:
        """
        tok_id queries & returns the token_id of the contract.

        Returns:
            md.TokenID: The token_id of the contract.
        """
        if not self._tok_id:
            raw_val = await self._query_db_key(self.DBKey.for_token_id())
            self._tok_id = md.TokenID(raw_val)
        return self._tok_id

    @property
    async def duration(self) -> md.VSYSTimestamp:
        """
        duration queries & returns the duration where the recipient can
        take actions in the contract.

        Returns:
            md.VSYSTimestamp: The duration.
        """
        raw_val = await self._query_db_key(self.DBKey.for_duration())
        return md.VSYSTimestamp(raw_val)

    @property
    async def judge_duration(self) -> md.VSYSTimestamp:
        """
        judge_duration queries & returns the duration where the judge can
        take actions in the contract.

        Returns:
            md.VSYSTimestamp: The duration.
        """
        raw_val = await self._query_db_key(self.DBKey.for_judge_duration())
        return md.VSYSTimestamp(raw_val)

    @property
    async def unit(self) -> int:
        """
        unit returns the unit of the token specified in this contract.

        Returns:
            int: The token unit.
        """
        tok_id = await self.tok_id

        if tok_id.is_vsys_tok:
            return md.VSYS.UNIT
        else:
            tc = await tcf.from_tok_id(tok_id.data, self.chain)
            return await tc.unit

    async def get_ctrt_bal(self, addr: str) -> md.Token:
        """
        get_ctrt_bal queries & returns the balance of the token within this contract
        belonging to the user address.

        Args:
            addr (str): The account address.

        Returns:
            md.Token: The balance of the token.
        """
        raw_val = await self._query_db_key(self.DBKey.for_contract_balance(addr))
        unit = await self.unit
        return md.Token(data=raw_val, unit=unit)

    async def get_order_payer(self, order_id: str) -> md.Addr:
        """
        get_order_payer queries & returns the payer of the order.

        Args:
            order_id (str): The order ID.

        Returns:
            md.Addr: The order payer.
        """
        raw_val = await self._query_db_key(self.DBKey.for_order_payer(order_id))
        return md.Addr(raw_val)

    async def get_order_recipient(self, order_id: str) -> md.Addr:
        """
        get_order_recipient queries & returns the recipient of the order.

        Args:
            order_id (str): The order ID.

        Returns:
            md.Addr: The order recipient.
        """
        raw_val = await self._query_db_key(self.DBKey.for_order_recipient(order_id))
        return md.Addr(raw_val)

    async def get_order_amount(self, order_id: str) -> md.Token:
        """
        get_order_amount queries & returns the amount of the order.

        Args:
            order_id (str): The order ID.

        Returns:
            md.Token: The order amount.
        """
        raw_val = await self._query_db_key(self.DBKey.for_order_amount(order_id))
        unit = await self.unit
        return md.Token(data=raw_val, unit=unit)

    async def get_order_recipient_deposit(self, order_id: str) -> md.Token:
        """
        get_order_recipient_deposit queries & returns the amount the recipient
        should deposit in the order.

        Args:
            order_id (str): The order ID.

        Returns:
            md.Token: The recipient deposit amount.
        """
        raw_val = await self._query_db_key(
            self.DBKey.for_order_recipient_deposit(order_id)
        )
        unit = await self.unit
        return md.Token(data=raw_val, unit=unit)

    async def get_order_judge_deposit(self, order_id: str) -> md.Token:
        """
        get_order_judge_deposit queries & returns the amount the judge
        should deposit in the order.

        Args:
            order_id (str): The order ID.

        Returns:
            md.Token: The judge deposit amount.
        """
        raw_val = await self._query_db_key(self.DBKey.for_order_judge_deposit(order_id))
        unit = await self.unit
        return md.Token(data=raw_val, unit=unit)

    async def get_order_fee(self, order_id: str) -> md.Token:
        """
        get_order_fee queries & returns the fee of the order.

        Args:
            order_id (str): The order ID.

        Returns:
            md.Token: The fee of the order.
        """
        raw_val = await self._query_db_key(self.DBKey.for_order_fee(order_id))
        unit = await self.unit
        return md.Token(data=raw_val, unit=unit)

    async def get_order_recipient_amount(self, order_id: str) -> md.Token:
        """
        get_order_recipient_amount queries & returns the how much the recipient will receive
        from the order if the order goes smoothly(i.e. work is submitted & approved).
        The recipient amount = order amount - order fee.

        Args:
            order_id (str): The order ID.

        Returns:
            md.Token: The recipient amount of the order.
        """
        raw_val = await self._query_db_key(
            self.DBKey.for_order_recipient_amount(order_id)
        )
        unit = await self.unit
        return md.Token(data=raw_val, unit=unit)

    async def get_order_refund(self, order_id: str) -> md.Token:
        """
        get_order_refund queries & returns the refund amount of the order.
        The refund amount means how much the payer will receive if the refund occurs.
        It is defined when the order is created.

        Args:
            order_id (str): The order ID.

        Returns:
            md.Token: The refund amount of the order.
        """
        raw_val = await self._query_db_key(self.DBKey.for_order_refund(order_id))
        unit = await self.unit
        return md.Token(data=raw_val, unit=unit)

    async def get_order_recipient_refund(self, order_id: str) -> md.Token:
        """
        get_order_recipient_refund queries & returns the recipient refund amount of the order.
        the recipient refund amount means how much the recipient will receive if the refund occurs.
        The recipient refund amount = The total deposit(order amount + judge deposit + recipient deposit) - payer refund

        Args:
            order_id (str): The order ID.

        Returns:
            md.Token: The recipient refund amount of the order.
        """
        raw_val = await self._query_db_key(
            self.DBKey.for_order_recipient_refund(order_id)
        )
        unit = await self.unit
        return md.Token(data=raw_val, unit=unit)

    async def get_order_expiration_time(self, order_id: str) -> md.VSYSTimestamp:
        """
        get_order_expiration_time queries & returns the expiration time of the order.

        Args:
            order_id (str): The order ID.

        Returns:
            md.VSYSTimestamp: The expiration time of the order.
        """
        raw_val = await self._query_db_key(
            self.DBKey.for_order_expiration_time(order_id)
        )
        return md.VSYSTimestamp(raw_val)

    async def get_order_status(self, order_id: str) -> bool:
        """
        get_order_status queries & returns the status of the order.
        The order status means if the order is active.
        The order is considered active if it is created & it is NOT finished.

        Args:
            order_id (str): The order ID.

        Returns:
            bool: The status of the order.
        """
        raw_val = await self._query_db_key(self.DBKey.for_order_status(order_id))
        return raw_val == "true"

    async def get_order_recipient_deposit_status(self, order_id: str) -> bool:
        """
        get_order_recipient_deposit_status queries & returns the recipient deposit status of the order.
        The order recipient deposit status means if the recipient has deposited into the order.

        Args:
            order_id (str): The order ID.

        Returns:
            bool: The recipient deposit status of the order.
        """
        raw_val = await self._query_db_key(
            self.DBKey.for_order_recipient_deposit_status(order_id)
        )
        return raw_val == "true"

    async def get_order_judge_deposit_status(self, order_id: str) -> bool:
        """
        get_order_judge_deposit_status queries & returns the judge deposit status of the order.
        The order judge deposit status means if the judge has deposited into the order.

        Args:
            order_id (str): The order ID.

        Returns:
            bool: The judge deposit status of the order.
        """
        raw_val = await self._query_db_key(
            self.DBKey.for_order_judge_deposit_status(order_id)
        )
        return raw_val == "true"

    async def get_order_submit_status(self, order_id: str) -> bool:
        """
        get_order_submit_status queries & returns the submit status of the order.

        Args:
            order_id (str): The order ID.

        Returns:
            bool: The submit status of the order.
        """
        raw_val = await self._query_db_key(self.DBKey.for_order_submit_status(order_id))
        return raw_val == "true"

    async def get_order_judge_status(self, order_id: str) -> bool:
        """
        get_order_judge_status queries & returns the judge status of the order.

        Args:
            order_id (str): The order ID.

        Returns:
            bool: The judge status of the order.
        """
        raw_val = await self._query_db_key(self.DBKey.for_order_judge_status(order_id))
        return raw_val == "true"

    async def get_order_recipient_locked_amount(self, order_id: str) -> md.Token:
        """
        get_order_recipient_locked_amount queries & returns the amount from the recipient
        that is locked(deposited) in the order.

        Args:
            order_id (str): The order ID.

        Returns:
            md.Token: The recipient locked amount of the order.
        """
        raw_val = await self._query_db_key(
            self.DBKey.for_order_recipient_locked_amount(order_id)
        )
        unit = await self.unit
        return md.Token(data=raw_val, unit=unit)

    async def get_order_judge_locked_amount(self, order_id: str) -> md.Token:
        """
        get_order_judge_locked_amount queries & returns the amount from the judge
        that is locked(deposited) in the order.

        Args:
            order_id (str): The order ID.

        Returns:
            md.Token: The judge locked amount of the order.
        """
        raw_val = await self._query_db_key(
            self.DBKey.for_order_judge_locked_amount(order_id)
        )
        unit = await self.unit
        return md.Token(data=raw_val, unit=unit)

    @classmethod
    async def register(
        cls,
        by: acnt.Account,
        tok_id: str,
        duration: int,
        judge_duration: int,
        ctrt_description: str = "",
        fee: int = md.RegCtrtFee.DEFAULT,
    ) -> VEscrowCtrt:
        """
        register registers a V Escrow Contract.

        Args:
            by (acnt.Account): The action taker.
            tok_id (str): The token ID.
            duration (int): The duration where the recipient can take actions.
            judge_duration (int): the duration where the judge can take actions.
            ctrt_description (str, optional): The description of the contract. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.RegCtrtFee.DEFAULT.

        Returns:
            VEscrowCtrt: The VEscrowCtrt object of the registered V Escrow Contract.
        """
        data = await by._register_contract(
            tx.RegCtrtTxReq(
                data_stack=de.DataStack(
                    de.TokenID(md.TokenID(tok_id)),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(duration)),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(judge_duration)),
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
        new_judge: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        supersede transfers the judge right of the contract to another account.

        Args:
            by (acnt.Account): The action taker
            new_issuer (int): The new judge of the contract
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str,any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SUPERSEDE,
                data_stack=de.DataStack(de.Addr(md.Addr(new_judge))),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def create(
        self,
        by: acnt.Account,
        recipient: str,
        amount: Union[int, float],
        rcpt_deposit_amount: Union[int, float],
        judge_deposit_amount: Union[int, float],
        order_fee: Union[int, float],
        refund_amount: Union[int, float],
        expire_at: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        create an escrow order.
        NOTE that the transaction id of this action is the order ID.

        Args:
            by (acnt.Account): The action taker.
            recipient (str): The recipient account.
            amount (Union[int, float]): The amount of tokens.
            rcpt_deposit_amount (Union[int, float]): The amount that the recipient needs to deposit.
            judge_deposit_amount (Union[int, float]): The amount that the judge needs to deposit.
            order_fee (Union[int, float]): The fee for this order.
            refund_amount (Union[int, float]): The amount to refund.
            expire_at (int): The expiration time of the order.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        rcpt_md = md.Addr(recipient)
        rcpt_md.must_on(self.chain)

        unit = await self.unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.CREATE,
                data_stack=de.DataStack(
                    de.Addr(md.Addr(recipient)),
                    de.Amount.for_tok_amount(amount, unit),
                    de.Amount.for_tok_amount(rcpt_deposit_amount, unit),
                    de.Amount.for_tok_amount(judge_deposit_amount, unit),
                    de.Amount.for_tok_amount(order_fee, unit),
                    de.Amount.for_tok_amount(refund_amount, unit),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(expire_at)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def recipient_deposit(
        self,
        by: acnt.Account,
        order_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        recipient_deposit deposits tokens the recipient deposited into the contract into the order.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order ID.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.RECIPIENT_DEPOSIT,
                data_stack=de.DataStack(
                    de.Bytes.for_base58_str(order_id),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def judge_deposit(
        self,
        by: acnt.Account,
        order_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        judge_deposit deposits tokens the judge deposited into the contract into the order.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order ID.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.JUDGE_DEPOSIT,
                data_stack=de.DataStack(
                    de.Bytes.for_base58_str(order_id),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def payer_cancel(
        self,
        by: acnt.Account,
        order_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        payer_cancel cancels the order by the payer.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order ID.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.PAYER_CANCEL,
                data_stack=de.DataStack(
                    de.Bytes.for_base58_str(order_id),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def recipient_cancel(
        self,
        by: acnt.Account,
        order_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        recipient_cancel cancels the order by the recipient.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order ID.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.RECIPIENT_CANCEL,
                data_stack=de.DataStack(
                    de.Bytes.for_base58_str(order_id),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def judge_cancel(
        self,
        by: acnt.Account,
        order_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        judge_cancel cancels the order by the judge.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order ID.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.JUDGE_CANCEL,
                data_stack=de.DataStack(
                    de.Bytes.for_base58_str(order_id),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def submit_work(
        self,
        by: acnt.Account,
        order_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        submit_work submits the work by the recipient.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order ID.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SUBMIT_WORK,
                data_stack=de.DataStack(
                    de.Bytes.for_base58_str(order_id),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def approve_work(
        self,
        by: acnt.Account,
        order_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        approve_work approves the work and agrees the amounts are paid by the payer.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order ID.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.APPROVE_WORK,
                data_stack=de.DataStack(
                    de.Bytes.for_base58_str(order_id),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def apply_to_judge(
        self,
        by: acnt.Account,
        order_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        apply_to_judge applies for the help from judge by the payer.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order ID.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.APPLY_TO_JUDGE,
                data_stack=de.DataStack(
                    de.Bytes.for_base58_str(order_id),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def do_judge(
        self,
        by: acnt.Account,
        order_id: str,
        payer_amount: Union[int, float],
        rcpt_amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        do_judge judges the work and decides on how much the payer & recipient
        will receive.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order ID.
            payer_amount (Union[int, float]): The amount the payer will get.
            rcpt_amount (Union[int, float]): The amount the recipient will get.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """
        unit = await self.unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.JUDGE,
                data_stack=de.DataStack(
                    de.Bytes.for_base58_str(order_id),
                    de.Amount.for_tok_amount(payer_amount, unit),
                    de.Amount.for_tok_amount(rcpt_amount, unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def submit_penalty(
        self,
        by: acnt.Account,
        order_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        submit_penalty submits penalty by the payer for the case where the recipient does not submit
        work before the expiration time. The payer will obtain the recipient deposit amount and the payer amount(fee deducted).
        The judge will still get the fee.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order ID.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SUBMIT_PENALTY,
                data_stack=de.DataStack(
                    de.Bytes.for_base58_str(order_id),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def payer_refund(
        self,
        by: acnt.Account,
        order_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        payer_refund makes the refund action by the payer when the judge does not judge the work in time
        after the apply_to_judge function is invoked.
        The judge loses his deposit amount and the payer receives the refund amount.
        The recipient receives the rest.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order ID.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.PAYER_REFUND,
                data_stack=de.DataStack(
                    de.Bytes.for_base58_str(order_id),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def recipient_refund(
        self,
        by: acnt.Account,
        order_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        recipient_refund makes the refund action by the recipient when the judge does not judge the work in time
        after the apply_to_judge function is invoked.
        The judge loses his deposit amount and the payer receives the refund amount.
        The recipient receives the rest.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order ID.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.RECIPIENT_REFUND,
                data_stack=de.DataStack(
                    de.Bytes.for_base58_str(order_id),
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
        order_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        collect collects the order amount & recipient deposited amount by the recipient when the work is submitted
        while the payer doesn't either approve or apply to judge in his action duration.
        The judge will get judge deposited amount & fee.

        Args:
            by (acnt.Account): The action taker.
            order_id (str): The order ID.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.COLLECT,
                data_stack=de.DataStack(
                    de.Bytes.for_base58_str(order_id),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data
