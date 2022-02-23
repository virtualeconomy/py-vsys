from multiprocessing.context import assert_spawning
import pytest

import py_v_sdk as pv
from test.func_test import conftest as cft
from py_v_sdk.utils.crypto.hashes import sha256_hash
from py_v_sdk.data_entry import DataStack
import base58, time


class TestAtomicSwapCtrt:
    """
    TestAtomicSwapCtrt is the collection of functional tests of atomic swap contract.
    """

    @pytest.fixture
    async def new_maker_tok_ctrt(self, acnt0: pv.Account) -> pv.TokenCtrtWithoutSplit:
        """
        new_maker_tok_ctrt is the fixture that registers a new token contract of maker's.

        Args:
            acnt0 (pv.Account): the account of nonce 0.

        Returns:
            pv.TokenCtrtWithoutSplit: the TokenCtrtWithoutSplit instance.
        """
        tc = await pv.TokenCtrtWithoutSplit.register(acnt0, 100, 1)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_taker_tok_ctrt(self, acnt1: pv.Account) -> pv.TokenCtrtWithoutSplit:
        """
        new_taker_tok_ctrt is the fixture that registers a new token contract of taker's.

        Args:
            acnt1 (pv.Account): the account of nonce 0.

        Returns:
            pv.TokenCtrtWithoutSplit: the TokenCtrtWithoutSplit instance.
        """
        tc = await pv.TokenCtrtWithoutSplit.register(acnt1, 100, 1)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_maker_tok_ctrt_with_tok(
        self, new_maker_tok_ctrt: pv.TokenCtrtWithoutSplit, acnt0: pv.Account
    ) -> pv.TokenCtrtWithoutSplit:
        """
        new_tok_ctrt_with_tok is the fixture that registers a new TokenWithoutSplit contract and issues tokens right after it.

        Args:
            new_maker_tok_ctrt (pv.TokenCtrtWithoutSplit): The fixture that registers a new TokenWithoutSplit contract.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokenCtrtWithoutSplit: The TokenCtrtWithoutSplit instance.
        """
        tc = new_maker_tok_ctrt
        await tc.issue(acnt0, 100)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_taker_tok_ctrt_with_tok(
        self, new_taker_tok_ctrt: pv.TokenCtrtWithoutSplit, acnt1: pv.Account
    ) -> pv.TokenCtrtWithoutSplit:
        """
        new_tok_ctrt_with_tok is the fixture that registers a new TokenWithoutSplit contract and issues tokens right after it.

        Args:
            new_taker_tok_ctrt (pv.TokenCtrtWithoutSplit): The fixture that registers a new TokenWithoutSplit contract.
            acnt1 (pv.Account): The account of nonce 1.

        Returns:
            pv.TokenCtrtWithoutSplit: The TokenCtrtWithoutSplit instance.
        """
        tc = new_taker_tok_ctrt
        await tc.issue(acnt1, 100)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_maker_atomic_swap_ctrt(
        self,
        new_maker_tok_ctrt_with_tok: pv.TokenCtrtWithoutSplit,
        acnt0: pv.Account,
    ) -> pv.AtomicSwapCtrt:
        """
        new_maker_atomic_swap_ctrt is the fixture that registers a new atomic swap contract.

        Args:
            new_maker_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new atomic swap contract and issues tokens right after it.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.AtomicSwapCtrt: The AtomicSwapCtrt instance.
        """
        tc = new_maker_tok_ctrt_with_tok

        tok_id = pv.Ctrt.get_tok_id(tc.ctrt_id, 0)
        ac = await pv.AtomicSwapCtrt.register(acnt0, tok_id)
        await cft.wait_for_block()

        await tc.deposit(acnt0, ac.ctrt_id, 100)
        await cft.wait_for_block()

        return ac

    @pytest.fixture
    async def new_taker_atomic_swap_ctrt(
        self,
        new_taker_tok_ctrt_with_tok: pv.TokenCtrtWithoutSplit,
        acnt1: pv.Account,
    ) -> pv.AtomicSwapCtrt:
        """
        new_taker_atomic_swap_ctrt is the fixture that registers a new atomic swap contract.

        Args:
            new_taker_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new token contract and issues tokens right after it.
            acnt1 (pv.Account): The account of nonce 1.

        Returns:
            pv.AtomicSwapCtrt: The AtomicSwapCtrt instance.
        """
        tc = new_taker_tok_ctrt_with_tok

        tok_id = pv.Ctrt.get_tok_id(tc.ctrt_id, 0)
        ac = await pv.AtomicSwapCtrt.register(acnt1, tok_id)
        await cft.wait_for_block()

        await tc.deposit(acnt1, ac.ctrt_id, 100)
        await cft.wait_for_block()

        return ac

    async def test_register(
        self, acnt0: pv.Account, new_maker_tok_ctrt_with_tok: pv.TokenCtrtWithoutSplit
    ) -> pv.AtomicSwapCtrt:
        """
        test_register tests the method register.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.AtomicSwapCtrt: the AtomicSwapCtrt instance.
        """
        tc = new_maker_tok_ctrt_with_tok
        tok_id = pv.Ctrt.get_tok_id(tc.ctrt_id, 0)
        ac = await pv.AtomicSwapCtrt.register(acnt0, tok_id)
        await cft.wait_for_block()

        assert (await ac.maker) == acnt0.addr.b58_str
        assert (await ac.token_id) == tok_id

        return ac

    async def test_maker_lock_and_taker_lock(
        self,
        acnt0: pv.Account,
        acnt1: pv.Account,
        new_maker_atomic_swap_ctrt: pv.AtomicSwapCtrt,
        new_taker_atomic_swap_ctrt: pv.AtomicSwapCtrt,
    ):
        """
        test_maker_lock_and_taker_lock tests the method maker_lock and taker_lock.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
            new_maker_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract of maker's.
            new_taker_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract of taker's.
        """
        maker_ctrt = new_maker_atomic_swap_ctrt
        taker_ctrt = new_taker_atomic_swap_ctrt
        api = maker_ctrt.chain.api
        a = await maker_ctrt.get_swap_balance(acnt0.addr.b58_str)
        b = await taker_ctrt.get_swap_balance(acnt1.addr.b58_str)

        assert 100 == a.data
        assert (await maker_ctrt.maker) == acnt0.addr.b58_str
        assert 100 == b.data
        assert (await taker_ctrt.maker) == acnt1.addr.b58_str

        # maker lock.
        maker_lock_timestamp = int(time.time()) + 1800
        maker_lock_tx_info = await maker_ctrt.maker_lock(
            acnt0, 10, acnt1.addr.b58_str, "abc", maker_lock_timestamp
        )
        await cft.wait_for_block()
        maker_lock_tx_id = maker_lock_tx_info["id"]
        await cft.assert_tx_success(api, maker_lock_tx_id)

        puzzle_DBKey = maker_ctrt.DBKey.for_puzzle(maker_lock_tx_id).b58_str
        puzzle_dict = await maker_ctrt.chain.api.ctrt.get_ctrt_data(
            maker_ctrt.ctrt_id, puzzle_DBKey
        )
        puzzle = puzzle_dict["value"]

        real_puzzle = base58.b58encode(sha256_hash("abc".encode("latin-1"))).decode(
            "latin-1"
        )

        c = await maker_ctrt.get_swap_balance(acnt0.addr.b58_str)
        assert 90 == c.data
        assert puzzle == real_puzzle

        # taker lock.
        taker_lock_timestamp = int(time.time()) + 1500
        taker_lock_tx_info = await taker_ctrt.taker_lock(
            acnt1,
            5,
            maker_ctrt.ctrt_id,
            acnt0.addr.b58_str,
            maker_lock_tx_id,
            taker_lock_timestamp,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, taker_lock_tx_info["id"])

        d = await taker_ctrt.get_swap_balance(acnt1.addr.b58_str)
        assert 95 == d.data

    async def test_maker_solve_and_taker_solve(
        self,
        acnt0: pv.Account,
        acnt1: pv.Account,
        new_maker_atomic_swap_ctrt: pv.AtomicSwapCtrt,
        new_taker_atomic_swap_ctrt: pv.AtomicSwapCtrt,
    ):
        """
        test_maker_solve_and_taker_solve tests the method maker_solve and taker_solve.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
            new_maker_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract of maker's.
            new_taker_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract of taker's.
        """
        maker_ctrt = new_maker_atomic_swap_ctrt
        taker_ctrt = new_taker_atomic_swap_ctrt
        api = maker_ctrt.chain.api

        maker_lock_timestamp = int(time.time()) + 1800
        maker_lock_tx_info = await maker_ctrt.maker_lock(
            acnt0, 10, acnt1.addr.b58_str, "abc", maker_lock_timestamp
        )
        await cft.wait_for_block()
        maker_lock_id = maker_lock_tx_info["id"]
        await cft.assert_tx_success(api, maker_lock_id)

        taker_lock_timestamp = int(time.time()) + 1500
        taker_lock_tx_info = await taker_ctrt.taker_lock(
            acnt1,
            5,
            maker_ctrt.ctrt_id,
            acnt0.addr.b58_str,
            maker_lock_id,
            taker_lock_timestamp,
        )
        await cft.wait_for_block()
        taker_lock_id = taker_lock_tx_info["id"]
        await cft.assert_tx_success(api, taker_lock_id)

        maker_solve_tx_info = await maker_ctrt.maker_solve(
            acnt0, taker_ctrt.ctrt_id, taker_lock_id, "abc"
        )
        await cft.wait_for_block()
        maker_solve_id = maker_solve_tx_info["id"]
        await cft.assert_tx_success(api, maker_solve_id)

        dict_data = await acnt0.chain.api.tx.get_info(maker_solve_id)
        func_data = dict_data["functionData"]
        ds = DataStack.deserialize(base58.b58decode(func_data))
        revealed_secret = ds.entries[1].data.data.decode("latin-1")

        assert revealed_secret == "abc"

        taker_solve_tx_info = await taker_ctrt.taker_solve(
            acnt1, maker_ctrt.ctrt_id, maker_lock_id, maker_solve_id
        )
        await cft.wait_for_block()
        taker_solve_id = taker_solve_tx_info["id"]
        await cft.assert_tx_success(api, taker_solve_id)

    async def test_exp_withdraw(
        self,
        acnt0: pv.Account,
        acnt1: pv.Account,
        new_maker_atomic_swap_ctrt: pv.AtomicSwapCtrt,
    ):
        """
        test_exp_withdraw tests the method exp_withdraw.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
            new_maker_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract of maker's.
        """
        maker_ctrt = new_maker_atomic_swap_ctrt
        api = maker_ctrt.chain.api

        maker_lock_tx_info = await maker_ctrt.maker_lock(
            acnt0, 10, acnt1.addr.b58_str, "abc", int(time.time()) + 10
        )
        await cft.wait_for_block()
        await cft.wait_for_block()  # wait for 12 seconds until the lock is expired.
        maker_lock_id = maker_lock_tx_info["id"]
        await cft.assert_tx_success(api, maker_lock_id)

        a = await maker_ctrt.get_swap_balance(acnt0.addr.b58_str)
        assert 90 == a.data

        exp_withdraw_tx_info = await maker_ctrt.exp_withdraw(acnt0, maker_lock_id)
        await cft.wait_for_block()
        exp_withdraw_id = exp_withdraw_tx_info["id"]
        await cft.assert_tx_success(api, exp_withdraw_id)

        b = await maker_ctrt.get_swap_balance(acnt0.addr.b58_str)
        assert 100 == b.data

    @pytest.mark.whole
    async def test_as_whole(
        self,
        acnt0: pv.Account,
        acnt1: pv.Account,
        new_maker_atomic_swap_ctrt: pv.AtomicSwapCtrt,
        new_taker_atomic_swap_ctrt: pv.AtomicSwapCtrt,
    ):
        """
        test_as_whole tests methods of AtomicSwapCtrt as a whole so as to reduce resource consumption.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
            new_maker_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract of maker's.
            new_taker_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract of taker's.
        """
        maker_ctrt = new_maker_atomic_swap_ctrt
        taker_ctrt = new_taker_atomic_swap_ctrt

        await self.test_maker_lock_and_taker_lock(acnt0, acnt1, maker_ctrt, taker_ctrt)
        await self.test_maker_solve_and_taker_solve(
            acnt0, acnt1, maker_ctrt, taker_ctrt
        )
