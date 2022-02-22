import time
from typing import Tuple

import pytest

import py_v_sdk as pv
from test.func_test import conftest as cft


class TestPayChanCtrt:
    """
    TestPayChanCtrt is the collection of functional tests of Payment Channel Contract.
    """

    TOK_MAX = 100
    TOK_UNIT = 1

    @pytest.fixture
    async def new_tok_ctrt(self, acnt0: pv.Account) -> pv.TokenCtrtWithoutSplit:
        """
        new_tok_ctrt is the fixture that registers a new token contract without split instance.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokenCtrtWithoutSplit: The token contract instance.
        """

        tc = await pv.TokenCtrtWithoutSplit.register(acnt0, self.TOK_MAX, self.TOK_UNIT)
        await cft.wait_for_block()

        await tc.issue(acnt0, self.TOK_MAX)
        await cft.wait_for_block()

        return tc

    @pytest.fixture
    async def new_ctrt(
        self, acnt0: pv.Account, new_tok_ctrt: pv.TokenCtrtWithoutSplit
    ) -> pv.PayChanCtrt:
        """
        new_ctrt is the fixture that registers a new Payment Channel contract.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.PayChanCtrt: The PayChanCtrt instance.
        """
        tc = new_tok_ctrt
        api = acnt0.api

        tok_id = pv.Ctrt.get_tok_id(tc.ctrt_id, 0)

        pc = await pv.PayChanCtrt.register(acnt0, tok_id)
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
            new_ctrt (pv.PayChanCtrt): The fixture that registers a new Payment Channel contract.

        Returns:
            Tuple[pv.PayChanCtrt, str]: The PayChanCtrt instance & channel id
        """
        pc = new_ctrt

        load_amount = self.TOK_MAX // 2
        later = int(time.time()) + 60 * 10

        resp = await pc.create_and_load(
            by=acnt0,
            recipient=acnt1.addr.b58_str,
            amount=load_amount,
            expire_at=later,
        )
        await cft.wait_for_block()
        chan_id = resp["id"]
        return pc, chan_id

    async def test_register(
        self,
        acnt0: pv.Account,
        new_tok_ctrt: pv.TokenCtrtWithoutSplit,
        new_ctrt: pv.PayChanCtrt,
    ) -> pv.PayChanCtrt:
        """
        test_register tests the method register.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_tok_ctrt (pv.TokenCtrtWithoutSplit): The fixture that registers a new Token contract.
            new_ctrt (pv.PayChanCtrt): The fixture that registers a new Payment Channel contract.

        Returns:
            pv.PayChanCtrt: The PayChanCtrt instance.
        """
        tc = new_tok_ctrt

        tok_id = pv.Ctrt.get_tok_id(tc.ctrt_id, 0)

        pc = new_ctrt

        maker = await pc.maker
        assert maker.data == acnt0.addr.b58_str

        tok_id_md = await pc.tok_id
        assert tok_id_md.data == tok_id

        ctrt_bal = await pc.get_ctrt_bal(acnt0.addr.b58_str)
        assert ctrt_bal.amount == self.TOK_MAX

        return pc

    async def test_create_and_load(
        self,
        acnt0: pv.Account,
        acnt1: pv.Account,
        new_ctrt: pv.PayChanCtrt,
    ) -> None:
        """
        test_create_and_load tests the method create_and_load.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
            new_ctrt (pv.PayChanCtrt): The fixture that registers a new Payment Channel contract.
        """

        pc = new_ctrt
        api = acnt0.api

        load_amount = self.TOK_MAX // 2
        later = int(time.time()) + 60 * 10

        resp = await pc.create_and_load(
            by=acnt0,
            recipient=acnt1.addr.b58_str,
            amount=load_amount,
            expire_at=later,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        chan_id = resp["id"]

        chan_creator = await pc.get_chan_creator(chan_id)
        assert chan_creator.data == acnt0.addr.b58_str

        chan_creator_pub_key = await pc.get_chan_creator_pub_key(chan_id)
        assert chan_creator_pub_key.data == acnt0.key_pair.pub.data

        chan_accum_load = await pc.get_chan_accum_load(chan_id)
        assert chan_accum_load.amount == load_amount

        chan_accum_pay = await pc.get_chan_accum_pay(chan_id)
        assert chan_accum_pay.amount == 0

        chan_exp_time = await pc.get_chan_exp_time(chan_id)
        assert chan_exp_time.unix_ts == later

        chan_status = await pc.get_chan_status(chan_id)
        assert chan_status is True

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
