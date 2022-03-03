import asyncio
import time

import pytest

import py_v_sdk as pv
from test.func_test import conftest as cft


class TestVSwapCtrt:
    """
    TestVSwapCtrt is the collection of functional tests of V Swap contract.
    """

    TOK_MAX = 1_000_000_000
    HALF_TOK_MAX = TOK_MAX // 2
    TOK_UNIT = 1_000
    MIN_LIQ = 10
    INIT_AMOUNT = 10_000

    async def new_tok_ctrt(self, acnt0: pv.Account) -> pv.TokCtrtWithoutSplit:
        """
        new_tok_ctrt is the fixture that registers a new token contract without split
        to be used in a V Swap contract.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: The TokCtrtWithoutSplit instance.
        """
        api = acnt0.api

        tc = await pv.TokCtrtWithoutSplit.register(
            by=acnt0,
            max=self.TOK_MAX,
            unit=self.TOK_UNIT,
        )
        await cft.wait_for_block()

        resp = await tc.issue(acnt0, self.TOK_MAX)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        return tc

    @pytest.fixture
    async def new_ctrt(
        self,
        acnt0: pv.Account,
        acnt1: pv.Account,
    ) -> pv.VSwapCtrt:
        """
        new_ctrt is the fixture that registers a new V Swap contract.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.

        Returns:
            pv.VSwapCtrt: The VSwapCtrt instance.
        """
        api = acnt0.api

        tca, tcb, tcl = await asyncio.gather(
            self.new_tok_ctrt(acnt0),
            self.new_tok_ctrt(acnt0),
            self.new_tok_ctrt(acnt0),
        )

        await asyncio.gather(
            tca.send(acnt0, acnt1.addr.data, self.HALF_TOK_MAX),
            tcb.send(acnt0, acnt1.addr.data, self.HALF_TOK_MAX),
        )

        await cft.wait_for_block()

        vc = await pv.VSwapCtrt.register(
            by=acnt0,
            tok_a_id=tca.tok_id.data,
            tok_b_id=tcb.tok_id.data,
            liq_tok_id=tcl.tok_id.data,
            min_liq=self.MIN_LIQ,
        )
        await cft.wait_for_block()

        resp_a0, resp_b0, resp_l, resp_a1, resp_b1 = await asyncio.gather(
            tca.deposit(acnt0, vc.ctrt_id, self.HALF_TOK_MAX),
            tcb.deposit(acnt0, vc.ctrt_id, self.HALF_TOK_MAX),
            tcl.deposit(acnt0, vc.ctrt_id, self.TOK_MAX),
            tca.deposit(acnt1, vc.ctrt_id, self.HALF_TOK_MAX),
            tcb.deposit(acnt1, vc.ctrt_id, self.HALF_TOK_MAX),
        )

        await cft.wait_for_block()

        await asyncio.gather(
            cft.assert_tx_success(api, resp_a0["id"]),
            cft.assert_tx_success(api, resp_b0["id"]),
            cft.assert_tx_success(api, resp_l["id"]),
            cft.assert_tx_success(api, resp_a1["id"]),
            cft.assert_tx_success(api, resp_b1["id"]),
        )

        return vc

    async def test_supersede(
        self, new_ctrt: pv.VSwapCtrt, acnt0: pv.Account, acnt1: pv.Account
    ):
        """
        test_supersede tests the method supersede.

        Args:
            new_ctrt (pv.VSwapCtrt): The fixture that registers a new V Swap contract.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        vc = new_ctrt
        api = vc.chain.api

        assert (await vc.maker) == acnt0.addr

        resp = await vc.supersede(acnt0, acnt1.addr.data)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await vc.maker) == acnt1.addr

    async def test_set_swap(self, new_ctrt: pv.VSwapCtrt, acnt0: pv.Account):
        """
        test_set_swap tests the method set_swap.

        Args:
            new_ctrt (pv.VSwapCtrt): The fixture that registers a new V Swap contract.
            acnt0 (pv.Account): The account of nonce 0.
        """

        vc = new_ctrt
        api = vc.chain.api

        assert (await vc.is_swap_active) is False

        resp = await vc.set_swap(
            by=acnt0,
            amount_a=self.INIT_AMOUNT,
            amount_b=self.INIT_AMOUNT,
        )

        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await vc.is_swap_active) is True

    @pytest.fixture
    async def new_ctrt_with_pool(
        self, new_ctrt: pv.VSwapCtrt, acnt0: pv.Account
    ) -> pv.VSwapCtrt:
        """
        new_ctrt_with_pool is the fixture that registers a new V Swap contract and
        initialize the swap pool.

        Args:
            new_ctrt (pv.VSwapCtrt): The V Swap instance.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.VSwapCtrt: The VSwapCtrt instance.
        """
        vc = new_ctrt
        api = vc.chain.api

        resp = await vc.set_swap(
            by=acnt0,
            amount_a=self.INIT_AMOUNT,
            amount_b=self.INIT_AMOUNT,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])
        assert (await vc.is_swap_active) is True

        return vc

    async def test_add_liquidity(
        self, new_ctrt_with_pool: pv.VSwapCtrt, acnt0: pv.Account
    ):
        """
        test_add_liquidity tests the method add_liquidity.

        Args:
            new_ctrt_with_pool (pv.VSwapCtrt): The VSwapCtrt instance where the pool is initialized.
            acnt0 (pv.Account): The account of nonce 0.
        """
        DELTA = 10_000
        DELTA_MIN = 9_000

        vc = new_ctrt_with_pool
        api = vc.chain.api

        tok_a_reserved_old, tok_b_reserved_old, liq_tok_left_old = await asyncio.gather(
            vc.tok_a_reserved, vc.tok_b_reserved, vc.liq_tok_left
        )

        ten_sec_later = int(time.time()) + 10

        resp = await vc.add_liquidity(
            by=acnt0,
            amount_a=DELTA,
            amount_b=DELTA,
            amount_a_min=DELTA_MIN,
            amount_b_min=DELTA_MIN,
            deadline=ten_sec_later,
        )

        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        tok_a_reserved, tok_b_reserved, liq_tok_left = await asyncio.gather(
            vc.tok_a_reserved,
            vc.tok_b_reserved,
            vc.liq_tok_left,
        )

        assert tok_a_reserved.amount == tok_a_reserved_old.amount + DELTA
        assert tok_b_reserved.amount == tok_b_reserved_old.amount + DELTA
        assert liq_tok_left.amount == liq_tok_left_old.amount - DELTA

    async def test_remove_liquidity(
        self, new_ctrt_with_pool: pv.VSwapCtrt, acnt0: pv.Account
    ):
        """
        test_remove_liquidity tests the method remove_liquidity.

        Args:
            new_ctrt_with_pool (pv.VSwapCtrt): The VSwapCtrt instance where the pool is initialized.
            acnt0 (pv.Account): The account of nonce 0.
        """
        DELTA = 1_000

        vc = new_ctrt_with_pool
        api = vc.chain.api

        tok_a_reserved_old, tok_b_reserved_old, liq_tok_left_old = await asyncio.gather(
            vc.tok_a_reserved,
            vc.tok_b_reserved,
            vc.liq_tok_left,
        )

        ten_sec_later = int(time.time()) + 10

        resp = await vc.remove_liquidity(
            by=acnt0,
            amount_liq=DELTA,
            amount_a_min=DELTA,
            amount_b_min=DELTA,
            deadline=ten_sec_later,
        )

        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        tok_a_reserved, tok_b_reserved, liq_tok_left = await asyncio.gather(
            vc.tok_a_reserved,
            vc.tok_b_reserved,
            vc.liq_tok_left,
        )

        assert liq_tok_left.amount == liq_tok_left_old.amount + DELTA

        tok_a_redeemed = tok_a_reserved_old.amount - tok_a_reserved.amount
        tok_b_redeemed = tok_b_reserved_old.amount - tok_b_reserved.amount

        assert tok_a_redeemed >= DELTA
        assert tok_b_redeemed >= DELTA

    async def test_swap_b_for_exact_a(
        self,
        new_ctrt_with_pool: pv.VSwapCtrt,
        acnt1: pv.Account,
    ):
        """
        test_swap_b_for_exact_a tests the method swap_b_for_exact_a.

        Args:
            new_ctrt_with_pool (pv.VSwapCtrt): The VSwapCtrt instance where the pool is initialized.
            acnt1 (pv.Account): The account of nonce 1.
        """
        vc = new_ctrt_with_pool
        api = vc.chain.api

        bal_a_old, bal_b_old = await asyncio.gather(
            vc.get_tok_a_bal(acnt1.addr.data),
            vc.get_tok_b_bal(acnt1.addr.data),
        )

        amount_a = 10
        amount_b_max = 20

        ten_sec_later = int(time.time()) + 10

        resp = await vc.swap_b_for_exact_a(
            by=acnt1,
            amount_a=amount_a,
            amount_b_max=amount_b_max,
            deadline=ten_sec_later,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"]),

        bal_a, bal_b = await asyncio.gather(
            vc.get_tok_a_bal(acnt1.addr.data),
            vc.get_tok_b_bal(acnt1.addr.data),
        )

        assert bal_a.amount == bal_a_old.amount + amount_a
        assert bal_b_old.amount - bal_b.amount <= amount_b_max

    async def test_swap_exact_b_for_a(
        self,
        new_ctrt_with_pool: pv.VSwapCtrt,
        acnt1: pv.Account,
    ):
        """
        test_swap_exact_b_for_a tests the method swap_exact_b_for_a.

        Args:
            new_ctrt_with_pool (pv.VSwapCtrt): The VSwapCtrt instance where the pool is initialized.
            acnt1 (pv.Account): The account of nonce 1.
        """

        vc = new_ctrt_with_pool
        api = vc.chain.api

        bal_a_old, bal_b_old = await asyncio.gather(
            vc.get_tok_a_bal(acnt1.addr.data),
            vc.get_tok_b_bal(acnt1.addr.data),
        )

        amount_a_min = 10
        amount_b = 20

        ten_sec_later = int(time.time()) + 10

        resp = await vc.swap_exact_b_for_a(
            by=acnt1,
            amount_a_min=amount_a_min,
            amount_b=amount_b,
            deadline=ten_sec_later,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"]),

        bal_a, bal_b = await asyncio.gather(
            vc.get_tok_a_bal(acnt1.addr.data),
            vc.get_tok_b_bal(acnt1.addr.data),
        )

        assert bal_a.amount - bal_a_old.amount >= amount_a_min
        assert bal_b.amount == bal_b_old.amount - amount_b

    async def test_swap_a_for_exact_b(
        self,
        new_ctrt_with_pool: pv.VSwapCtrt,
        acnt1: pv.Account,
    ):
        """
        test_swap_a_for_exact_b tests the method swap_a_for_exact_b.

        Args:
            new_ctrt_with_pool (pv.VSwapCtrt): The VSwapCtrt instance where the pool is initialized.
            acnt1 (pv.Account): The account of nonce 1.
        """

        vc = new_ctrt_with_pool
        api = vc.chain.api

        bal_a_old, bal_b_old = await asyncio.gather(
            vc.get_tok_a_bal(acnt1.addr.data),
            vc.get_tok_b_bal(acnt1.addr.data),
        )

        amount_a_max = 20
        amount_b = 10

        ten_sec_later = int(time.time()) + 10

        resp = await vc.swap_a_for_exact_b(
            by=acnt1,
            amount_a_max=amount_a_max,
            amount_b=amount_b,
            deadline=ten_sec_later,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"]),

        bal_a, bal_b = await asyncio.gather(
            vc.get_tok_a_bal(acnt1.addr.data),
            vc.get_tok_b_bal(acnt1.addr.data),
        )

        assert bal_a_old.amount - bal_a.amount <= amount_a_max
        assert bal_b.amount == bal_b_old.amount + amount_b

    async def test_swap_exact_a_for_b(
        self,
        new_ctrt_with_pool: pv.VSwapCtrt,
        acnt1: pv.Account,
    ):
        """
        test_swap_exact_a_for_b tests the method swap_exact_a_for_b.

        Args:
            new_ctrt_with_pool (pv.VSwapCtrt): The VSwapCtrt instance where the pool is initialized.
            acnt1 (pv.Account): The account of nonce 1.
        """

        vc = new_ctrt_with_pool
        api = vc.chain.api

        bal_a_old, bal_b_old = await asyncio.gather(
            vc.get_tok_a_bal(acnt1.addr.data),
            vc.get_tok_b_bal(acnt1.addr.data),
        )

        amount_a = 20
        amount_b_min = 10

        ten_sec_later = int(time.time()) + 10

        resp = await vc.swap_exact_a_for_b(
            by=acnt1,
            amount_a=amount_a,
            amount_b_min=amount_b_min,
            deadline=ten_sec_later,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"]),

        bal_a, bal_b = await asyncio.gather(
            vc.get_tok_a_bal(acnt1.addr.data),
            vc.get_tok_b_bal(acnt1.addr.data),
        )

        assert bal_a.amount == bal_a_old.amount - amount_a
        assert bal_b.amount - bal_b_old.amount >= amount_b_min

    @pytest.mark.whole
    async def test_as_whole(
        self,
        new_ctrt: pv.VSwapCtrt,
        acnt0: pv.Account,
        acnt1: pv.Account,
    ):
        """
        test_as_whole tests methods of VSwapCtrt as a whole so as to reduce resource consumption.

        Args:
            new_ctrt (pv.VSwapCtrt): The V Swap instance.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        vc = new_ctrt

        await self.test_set_swap(vc, acnt0)
        await self.test_add_liquidity(vc, acnt0)
        await self.test_remove_liquidity(vc, acnt0)
        await self.test_swap_b_for_exact_a(vc, acnt1)
        await self.test_swap_exact_b_for_a(vc, acnt1)
        await self.test_swap_a_for_exact_b(vc, acnt1)
        await self.test_swap_exact_a_for_b(vc, acnt1)
        await self.test_supersede(vc, acnt0, acnt1)
