"""
sys_ctrt contains System contract.
"""

from __future__ import annotations
from typing import Dict, Any, TYPE_CHECKING, Union

from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import account as acnt
    from py_v_sdk import chain as ch

from py_v_sdk import data_entry as de
from py_v_sdk import tx_req as tx
from py_v_sdk import model as md

from . import Ctrt


class SysCtrt(Ctrt):
    """
    SysCtrt is the class for VSYS System contract.
    """

    MAINNET_CTRT_ID = "CCL1QGBqPAaFjYiA8NMGVhzkd3nJkGeKYBq"
    TESTNET_CTRT_ID = "CF9Nd9wvQ8qVsGk8jYHbj6sf8TK7MJ2GYgt"

    class FuncIdx(Ctrt.FuncIdx):
        """
        FuncIdx is the enum class for function indexes of a contract.
        """

        SEND = 0
        DEPOSIT = 1
        WITHDRAW = 2
        TRANSFER = 3

    @classmethod
    def for_mainnet(cls, chain: ch.Chain) -> SysCtrt:
        """
        for_mainnet returns the SysCtrt instance for mainnet.

        Args:
            chain (ch.Chain): The object of the chain where the contract is on.

        Returns:
            SysCtrt: The SysCtrt object.
        """
        return cls(
            ctrt_id=cls.MAINNET_CTRT_ID,
            chain=chain,
        )

    @classmethod
    def for_testnet(cls, chain: ch.Chain) -> SysCtrt:
        """
        for_testnet returns the SysCtrt instance for testnet.

        Args:
            chain (ch.Chain): The object of the chain where the contract is on.

        Returns:
            SysCtrt: The SysCtrt object.
        """
        return cls(
            ctrt_id=cls.TESTNET_CTRT_ID,
            chain=chain,
        )

    async def send(
        self,
        by: acnt.Account,
        recipient: str,
        amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        send sends VSYS coins to another account

        Args:
            by (acnt.Account): The action taker
            recipient (str): The recipient account
            amount (Union[int, float]): The amount of token to be sent
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        rcpt_md = md.Addr(recipient)
        rcpt_md.must_on(by.chain)

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SEND,
                data_stack=de.DataStack(
                    de.Addr(rcpt_md),
                    de.Amount.for_vsys_amount(amount),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def transfer(
        self,
        by: acnt.Account,
        sender: str,
        recipient: str,
        amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        transfer transfers tokens from sender to recipient

        Args:
            by (acnt.Account): The action taker
            sender (str): The sender account
            recipient (str): The recipient account
            amount (Union[int, float]): The amount to transfer
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        sender_md = md.Addr(sender)
        rcpt_md = md.Addr(recipient)

        sender_md.must_on(by.chain)
        rcpt_md.must_on(by.chain)

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.TRANSFER,
                data_stack=de.DataStack(
                    de.Addr(sender_md),
                    de.Addr(rcpt_md),
                    de.Amount.for_vsys_amount(amount),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def deposit(
        self,
        by: acnt.Account,
        ctrt_id: str,
        amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        deposit deposits the tokens into the contract

        Args:
            by (acnt.Account): The action maker.
            ctrt_id (str): The contract id to deposit into
            amount (Union[int, float]): The amount to deposit
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        sender_md = md.Addr(by.addr.b58_str)
        sender_md.must_on(by.chain)

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.DEPOSIT,
                data_stack=de.DataStack(
                    de.Addr(sender_md),
                    de.CtrtAcnt(md.CtrtID(ctrt_id)),
                    de.Amount.for_vsys_amount(amount),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def withdraw(
        self,
        by: acnt.Account,
        ctrt_id: str,
        amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        withdraw withdraws tokens from another contract

        Args:
            by (acnt.Account): The action maker.
            ctrt_id (str): The contract id that you want to withdraw token from
            amount (Union[int, float]): The amount to withdraw
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        rcpt_md = md.Addr(by.addr.b58_str)
        rcpt_md.must_on(by.chain)

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.WITHDRAW,
                data_stack=de.DataStack(
                    de.CtrtAcnt(md.CtrtID(ctrt_id)),
                    de.Addr(rcpt_md),
                    de.Amount.for_vsys_amount(amount),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data
