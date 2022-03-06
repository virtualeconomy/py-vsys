import asyncio
import time
from typing import Tuple

import pytest

import py_vsys as pv
from test.func_test import conftest as cft


class TestPayChanCtrt:
    """
    TestPayChanCtrt is the collection of functional tests of Payment Channel Contract.
    """

    TOK_MAX = 100
    TOK_UNIT = 1
    INIT_LOAD = TOK_MAX // 2

    @pytest.fixture
    async def new_tok_ctrt(self, acnt0: pv.Account) -> pv.TokCtrtWithoutSplit:
        """
        new_tok_ctrt is the fixture that registers a new token contract without split instance.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: The token contract instance.
        """

        tc = await pv.TokCtrtWithoutSplit.register(acnt0, self.TOK_MAX, self.TOK_UNIT)
        await cft.wait_for_block()

        await tc.issue(acnt0, self.TOK_MAX)
        await cft.wait_for_block()

        return tc

    @pytest.fixture
    async def new_ctrt(
        self, acnt0: pv.Account, new_tok_ctrt: pv.TokCtrtWithoutSplit
    ) -> pv.PayChanCtrt:
        """
        new_ctrt is the fixture that registers a new Payment Channel contract.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_tok_ctrt (pv.TokCtrtWithoutSplit): The fixture that registers a new Token contract.

        Returns:
            pv.PayChanCtrt: The PayChanCtrt instance.
        """
        tc = new_tok_ctrt
        api = acnt0.api

        pc = await pv.PayChanCtrt.register(acnt0, tc.tok_id.data)
        await cft.wait_for_block()

        resp = await tc.deposit(acnt0, pc.ctrt_id, self.TOK_MAX)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        return pc

    @pytest.fixture
    async def new_ctrt_with_chan(
        self,
        acnt0: pv.Account,
        acnt1: pv.Account,
        new_ctrt: pv.PayChanCtrt,
    ) -> Tuple[pv.PayChanCtrt, str]:
        """
        new_ctrt_with_chan is the fixture that registers a new Payment Channel
        contract and creates a channel.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
            new_ctrt (pv.PayChanCtrt): The fixture that registers a new Payment Channel contract.

        Returns:
            Tuple[pv.PayChanCtrt, str]: The PayChanCtrt instance & channel id
        """
        pc = new_ctrt

        load_amount = self.INIT_LOAD
        later = int(time.time()) + 60 * 10

        resp = await pc.create_and_load(
            by=acnt0,
            recipient=acnt1.addr.data,
            amount=load_amount,
            expire_at=later,
        )
        await cft.wait_for_block()
        chan_id = resp["id"]
        return pc, chan_id

    async def test_register(
        self,
        acnt0: pv.Account,
        new_tok_ctrt: pv.TokCtrtWithoutSplit,
        new_ctrt: pv.PayChanCtrt,
    ) -> pv.PayChanCtrt:
        """
        test_register tests the method register.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_tok_ctrt (pv.TokCtrtWithoutSplit): The fixture that registers a new Token contract.
            new_ctrt (pv.PayChanCtrt): The fixture that registers a new Payment Channel contract.

        Returns:
            pv.PayChanCtrt: The PayChanCtrt instance.
        """
        tc = new_tok_ctrt

        pc = new_ctrt

        assert (await pc.maker) == acnt0.addr
        assert (await pc.tok_id) == tc.tok_id

        ctrt_bal = await pc.get_ctrt_bal(acnt0.addr.data)
        assert ctrt_bal.amount == self.TOK_MAX

        return pc

    async def test_create_and_load(
        self,
        acnt0: pv.Account,
        acnt1: pv.Account,
        new_ctrt: pv.PayChanCtrt,
    ) -> str:
        """
        test_create_and_load tests the method create_and_load.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
            new_ctrt (pv.PayChanCtrt): The fixture that registers a new Payment Channel contract.

        Returns:
            str: The channel ID.
        """

        pc = new_ctrt
        api = acnt0.api

        load_amount = self.INIT_LOAD
        later = int(time.time()) + 60 * 10

        resp = await pc.create_and_load(
            by=acnt0,
            recipient=acnt1.addr.data,
            amount=load_amount,
            expire_at=later,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        chan_id = resp["id"]

        chan_creator = await pc.get_chan_creator(chan_id)
        assert chan_creator == acnt0.addr

        chan_creator_pub_key = await pc.get_chan_creator_pub_key(chan_id)
        assert chan_creator_pub_key == acnt0.key_pair.pub

        chan_accum_load = await pc.get_chan_accum_load(chan_id)
        assert chan_accum_load.amount == load_amount

        chan_accum_pay = await pc.get_chan_accum_pay(chan_id)
        assert chan_accum_pay.amount == 0

        chan_exp_time = await pc.get_chan_exp_time(chan_id)
        assert chan_exp_time.unix_ts == later

        chan_status = await pc.get_chan_status(chan_id)
        assert chan_status is True

        return chan_id

    async def test_extend_exp_time(
        self,
        acnt0: pv.Account,
        new_ctrt_with_chan: Tuple[pv.PayChanCtrt, str],
    ) -> None:
        """
        test_extend_exp_time tests the method extend_exp_time.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_ctrt_with_chan (Tuple[pv.PayChanCtrt, str]): The fixture that registers a new Payment Channel contract
                and creates a new channel.
        """

        pc, chan_id = new_ctrt_with_chan
        api = acnt0.api

        chan_exp_time_old = await pc.get_chan_exp_time(chan_id)

        new_later = chan_exp_time_old.unix_ts + 300
        resp = await pc.extend_exp_time(
            by=acnt0,
            chan_id=chan_id,
            expire_at=new_later,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        chan_exp_time = await pc.get_chan_exp_time(chan_id)
        assert chan_exp_time.unix_ts == new_later

    async def test_load(
        self,
        acnt0: pv.Account,
        new_ctrt_with_chan: Tuple[pv.PayChanCtrt, str],
    ) -> None:
        """
        test_load tests the method load.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_ctrt_with_chan (Tuple[pv.PayChanCtrt, str]): The fixture that registers a new Payment Channel contract
                and creates a new channel.
        """

        pc, chan_id = new_ctrt_with_chan
        api = acnt0.api

        chan_load_old = await pc.get_chan_accum_load(chan_id)
        assert chan_load_old.amount == self.INIT_LOAD

        more_load = self.INIT_LOAD // 2

        resp = await pc.load(acnt0, chan_id, more_load)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        chan_load = await pc.get_chan_accum_load(chan_id)
        assert chan_load.amount == self.INIT_LOAD + more_load

    async def test_abort(
        self,
        acnt0: pv.Account,
        new_ctrt_with_chan: Tuple[pv.PayChanCtrt, str],
    ) -> None:
        """
        test_abort tests the method abort.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_ctrt_with_chan (Tuple[pv.PayChanCtrt, str]): The fixture that registers a new Payment Channel contract
                and creates a new channel.
        """

        pc, chan_id = new_ctrt_with_chan
        api = acnt0.api

        chan_status = await pc.get_chan_status(chan_id)
        assert chan_status is True

        resp = await pc.abort(acnt0, chan_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        chan_status = await pc.get_chan_status(chan_id)
        assert chan_status is False

    async def test_unload(
        self,
        acnt0: pv.Account,
        acnt1: pv.Account,
        new_ctrt: pv.PayChanCtrt,
    ) -> None:
        """
        test_unload tests the method unload.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
            new_ctrt (pv.PayChanCtrt): The fixture that registers a new Payment Channel contract.
        """

        pc = new_ctrt
        api = acnt0.api

        load_amount = self.TOK_MAX // 10

        later = int(time.time()) + cft.AVG_BLOCK_DELAY * 2

        # create a channel
        resp = await pc.create_and_load(
            by=acnt0,
            recipient=acnt1.addr.data,
            amount=load_amount,
            expire_at=later,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        chan_id = resp["id"]

        bal_old = await pc.get_ctrt_bal(acnt0.addr.data)

        # wait until the channel expires
        await asyncio.sleep(cft.AVG_BLOCK_DELAY * 2)

        resp = await pc.unload(acnt0, chan_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        bal = await pc.get_ctrt_bal(acnt0.addr.data)
        assert bal.amount == bal_old.amount + load_amount

    async def test_offchain_pay_and_collect_payment(
        self,
        acnt0: pv.Account,
        acnt1: pv.Account,
        new_ctrt_with_chan: Tuple[pv.PayChanCtrt, str],
    ) -> None:
        """
        test_offchain_pay_and_collect_payment tests the method
            - offchain_pay
            - collect_payment.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
            new_ctrt_with_chan (Tuple[pv.PayChanCtrt, str]): The fixture that registers a new Payment Channel contract
                and creates a new channel.
        """

        pc, chan_id = new_ctrt_with_chan
        api = acnt0.api

        sig = await pc.offchain_pay(
            key_pair=acnt0.key_pair,
            chan_id=chan_id,
            amount=self.INIT_LOAD,
        )

        resp = await pc.collect_payment(
            by=acnt1,
            chan_id=chan_id,
            amount=self.INIT_LOAD,
            signature=sig,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        accum_pay = await pc.get_chan_accum_pay(chan_id)
        assert accum_pay.amount == self.INIT_LOAD

        acnt1_bal = await pc.get_ctrt_bal(acnt1.addr.data)
        assert acnt1_bal.amount == self.INIT_LOAD

    @pytest.mark.whole
    async def test_as_whole(
        self,
        acnt0: pv.Account,
        acnt1: pv.Account,
        new_tok_ctrt: pv.TokCtrtWithoutSplit,
        new_ctrt: pv.PayChanCtrt,
    ) -> None:
        """
        test_as_whole tests methods of PayChanCtrt as a whole so as to reduce resource consumption.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
            new_tok_ctrt (pv.TokCtrtWithoutSplit): The token contract instance.
            new_ctrt (pv.PayChanCtrt): The fixture that registers a new Payment Channel contract.
        """
        tc = new_tok_ctrt
        pc = new_ctrt

        await self.test_register(acnt0, tc, pc)
        chan_id = await self.test_create_and_load(acnt0, acnt1, pc)

        pc_with_chan = (pc, chan_id)

        await self.test_extend_exp_time(acnt0, pc_with_chan)
        await self.test_load(acnt0, pc_with_chan)
        await self.test_offchain_pay_and_collect_payment(acnt0, acnt1, pc_with_chan)
        await self.test_abort(acnt0, pc_with_chan)
        await self.test_unload(acnt0, acnt1, pc)
