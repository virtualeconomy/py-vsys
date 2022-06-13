"""
module contract/atomicSwapHelper provides higher level encapsulation of functionalities for V Atomic Swap contract on vsys chain.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any, Union, Optional

from loguru import logger
import base58

from py_vsys.contract.atomic_swap_ctrt import AtomicSwapCtrt

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_vsys import account as acnt
    from py_vsys import chain as ch

from py_vsys import data_entry as de
from py_vsys import tx_req as tx
from py_vsys import model as md
from py_vsys.contract import tok_ctrt_factory as tcf
from py_vsys.utils.crypto import hashes as hs
from . import CtrtMeta, Ctrt, BaseTokCtrt


class atomicSwapHelper(AtomicSwapCtrt):

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
            attachment (str, optional): Defaults to "".
            fee (int, optional): Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """
        puzzle_bytes = hs.sha256_hash(secret.encode("latin-1"))

        unit = await self.unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.LOCK,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount, unit),
                    de.Addr(md.Addr(recipient)),
                    de.Bytes(md.Bytes(puzzle_bytes)),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(int(expire_time))),
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
        taker_lock locks the token by the taker.

        Args:
            by (acnt.Account): The action taker.
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
        puzzle_db_key = self.DBKey.for_swap_puzzle(maker_lock_tx_id)
        data = await self.chain.api.ctrt.get_ctrt_data(
            maker_swap_ctrt_id, puzzle_db_key.b58_str
        )
        logger.debug(data)
        hashed_secret_b58str = data["value"]
        puzzle_bytes = base58.b58decode(hashed_secret_b58str)

        unit = await self.unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.LOCK,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount, unit),
                    de.Addr(md.Addr(recipient)),
                    de.Bytes(md.Bytes(puzzle_bytes)),
                    de.Timestamp(md.VSYSTimestamp.from_unix_ts(expire_time)),
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
        taker_swap_ctrt_id: str,
        tx_id: str,
        secret: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        maker_solve solves the puzzle and reveals the secret to get taker's locked tokens for maker.

        Args:
            by (acnt.Account): The action taker.
            taker_swap_ctrt_id (str): The swap ctrt id of the taker's.
            tx_id (str): The lock transaction id of taker's .
            secret (str): The secret.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=md.CtrtID(taker_swap_ctrt_id),
                func_id=self.FuncIdx.SOLVE_PUZZLE,
                data_stack=de.DataStack(
                    de.Bytes.from_base58_str(tx_id),
                    de.Bytes.from_str(secret),
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
        maker_swap_ctrt_id: str,
        maker_lock_tx_id: str,
        maker_solve_tx_id: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        taker_solve solves the puzzle by the secret the maker reveals and gets the makers' locked tokens
        for taker.

        Args:
            by (acnt.Account): The action taker.
            maker_swap_ctrt_id (str): The contract id of the maker's.
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
        ds = de.DataStack.deserialize(base58.b58decode(func_data))
        revealed_secret = ds.entries[1].data.data.decode("latin-1")

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=md.CtrtID(maker_swap_ctrt_id),
                func_id=self.FuncIdx.SOLVE_PUZZLE,
                data_stack=de.DataStack(
                    de.Bytes.from_base58_str(maker_lock_tx_id),
                    de.Bytes.from_str(revealed_secret),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

