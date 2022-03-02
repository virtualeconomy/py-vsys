import asyncio
import time

import pytest

import py_v_sdk as pv
from test.func_test import conftest as cft


class TestLockCtrt:
    """
    TestLockCtrt is the collection of functional tests of Lock contract.
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
    ) -> pv.LockCtrt:
        """
        new_ctrt is the fixture that registers a new Lock contract.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.LockCtrt: The LockCtrt instance.
        """
        tc = new_tok_ctrt

        nc = await pv.LockCtrt.register(acnt0, tc.tok_id.data)
        await cft.wait_for_block()
        return nc

    async def test_register(
        self,
        acnt0: pv.Account,
        new_tok_ctrt: pv.TokenCtrtWithoutSplit,
        new_ctrt: pv.LockCtrt,
    ) -> pv.LockCtrt:
        """
        test_register tests the method register.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_tok_ctrt (pv.TokenCtrtWithoutSplit): The fixture that registers a new Token contract.
            new_ctrt (pv.LockCtrt): The fixture that registers a new Lock contract.

        Returns:
            pv.LockCtrt: The LockCtrt instance.
        """
        tc = new_tok_ctrt
        lc = new_ctrt

        assert (await lc.maker).data == acnt0.addr.b58_str
        assert (await lc.tok_id).data == tc.tok_id.data
        assert (await lc.get_ctrt_bal(acnt0.addr.b58_str)).amount == 0
        assert (await lc.get_ctrt_lock_time(acnt0.addr.b58_str)).unix_ts == 0

        return lc

    async def test_lock(
        self,
        acnt0: pv.Account,
        new_tok_ctrt: pv.TokenCtrtWithoutSplit,
        new_ctrt: pv.LockCtrt,
    ):
        """
        test_lock tests the method lock.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_tok_ctrt (pv.TokenCtrtWithoutSplit): The fixture that registers a new Token contract.
            new_ctrt (pv.LockCtrt): The fixture that registers a new Lock contract.
        """
        tc = new_tok_ctrt
        lc = new_ctrt
        api = acnt0.api

        resp = await tc.deposit(acnt0, lc.ctrt_id, self.TOK_MAX)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])
        assert (await lc.get_ctrt_bal(acnt0.addr.b58_str)).amount == self.TOK_MAX

        later = int(time.time()) + cft.AVG_BLOCK_DELAY * 2 + 2
        resp = await lc.lock(acnt0, later)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])
        assert (await lc.get_ctrt_lock_time(acnt0.addr.b58_str)).unix_ts == later

        # withdraw before the expiration will fail
        resp = await tc.withdraw(acnt0, lc.ctrt_id, self.TOK_MAX)
        await cft.wait_for_block()
        await cft.assert_tx_status(api, resp["id"], "Failed")
        assert (await lc.get_ctrt_bal(acnt0.addr.b58_str)).amount == self.TOK_MAX

        # till here, 2 block time has passed, wait for a few seconds more the lock will expire
        await asyncio.sleep(6)

        # withdraw after the expiration will succeed
        resp = await tc.withdraw(acnt0, lc.ctrt_id, self.TOK_MAX)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])
        assert (await lc.get_ctrt_bal(acnt0.addr.b58_str)).amount == 0

    @pytest.mark.whole
    async def test_as_whole(
        self,
        acnt0: pv.Account,
        new_tok_ctrt: pv.TokenCtrtWithoutSplit,
        new_ctrt: pv.LockCtrt,
    ):
        """
        test_as_whole tests methods of LockCtrt as a whole so as to reduce resource consumption.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_tok_ctrt (pv.TokenCtrtWithoutSplit): The fixture that registers a new Token contract.
            new_ctrt (pv.LockCtrt): The fixture that registers a new Lock contract.
        """
        tc = new_tok_ctrt
        lc = new_ctrt

        lc = await self.test_register(acnt0, tc, lc)
        await self.test_lock(acnt0, tc, lc)
