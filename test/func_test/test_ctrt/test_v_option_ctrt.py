import pytest
import time
import asyncio

import py_vsys as pv
from test.func_test import conftest as cft


class TestVOptionCtrt:
    """
    TestVOptionCtrt is the collection of functional tests of V Option contract.
    """

    @pytest.fixture
    async def new_base_ctrt(self, acnt0: pv.Account) -> pv.TokCtrtWithoutSplit:
        """
        new_base_ctrt is the fixture that registers a new base token contract.

        Args:
            acnt0 (pv.Account): the account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: the TokCtrtWithoutSplit instance.
        """
        tc = await pv.TokCtrtWithoutSplit.register(acnt0, 1000, 1)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_target_ctrt(self, acnt0: pv.Account) -> pv.TokCtrtWithoutSplit:
        """
        new_target_ctrt is the fixture that registers a new target token contract.

        Args:
            acnt0 (pv.Account): the account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: the TokCtrtWithoutSplit instance.
        """
        tc = await pv.TokCtrtWithoutSplit.register(acnt0, 1000, 1)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_option_ctrt(self, acnt0: pv.Account) -> pv.TokCtrtWithoutSplit:
        """
        new_option_ctrt is the fixture that registers a new option token contract.

        Args:
            acnt0 (pv.Account): the account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: the TokCtrtWithoutSplit instance.
        """
        tc = await pv.TokCtrtWithoutSplit.register(acnt0, 1000, 1)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_proof_ctrt(self, acnt0: pv.Account) -> pv.TokCtrtWithoutSplit:
        """
        new_proof_ctrt is the fixture that registers a new proof token contract.

        Args:
            acnt0 (pv.Account): the account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: the TokCtrtWithoutSplit instance.
        """
        tc = await pv.TokCtrtWithoutSplit.register(acnt0, 1000, 1)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_base_ctrt_with_tok(
        self, new_base_ctrt: pv.TokCtrtWithoutSplit, acnt0: pv.Account
    ) -> pv.TokCtrtWithoutSplit:
        """
        new_base_ctrt_with_tok is the fixture that registers a new TokenWithoutSplit contract and issues base tokens right after it.

        Args:
            new_base_ctrt (pv.TokCtrtWithoutSplit): The fixture that registers a new TokenWithoutSplit contract.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: The TokCtrtWithoutSplit instance.
        """
        tc = new_base_ctrt
        await tc.issue(acnt0, 1000)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_target_ctrt_with_tok(
        self, new_target_ctrt: pv.TokCtrtWithoutSplit, acnt0: pv.Account
    ) -> pv.TokCtrtWithoutSplit:
        """
        new_target_ctrt_with_tok is the fixture that registers a new TokenWithoutSplit contract and issues target tokens right after it.

        Args:
            new_target_ctrt (pv.TokCtrtWithoutSplit): The fixture that registers a new TokenWithoutSplit contract.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: The TokCtrtWithoutSplit instance.
        """
        tc = new_target_ctrt
        await tc.issue(acnt0, 1000)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_option_ctrt_with_tok(
        self, new_option_ctrt: pv.TokCtrtWithoutSplit, acnt0: pv.Account
    ) -> pv.TokCtrtWithoutSplit:
        """
        new_option_ctrt_with_tok is the fixture that registers a new TokenWithoutSplit contract and issues option tokens right after it.

        Args:
            new_option_ctrt (pv.TokCtrtWithoutSplit): The fixture that registers a new TokenWithoutSplit contract.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: The TokCtrtWithoutSplit instance.
        """
        tc = new_option_ctrt
        await tc.issue(acnt0, 1000)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_proof_ctrt_with_tok(
        self, new_proof_ctrt: pv.TokCtrtWithoutSplit, acnt0: pv.Account
    ) -> pv.TokCtrtWithoutSplit:
        """
        new_proof_ctrt_with_tok is the fixture that registers a new TokenWithoutSplit contract and issues proof tokens right after it.

        Args:
            new_proof_ctrt (pv.TokCtrtWithoutSplit): The fixture that registers a new TokenWithoutSplit contract.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: The TokCtrtWithoutSplit instance.
        """
        tc = new_proof_ctrt
        await tc.issue(acnt0, 1000)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_v_option_ctrt(
        self,
        acnt0: pv.Account,
        new_base_ctrt_with_tok: pv.TokCtrtWithoutSplit,
        new_target_ctrt_with_tok: pv.TokCtrtWithoutSplit,
        new_option_ctrt_with_tok: pv.TokCtrtWithoutSplit,
        new_proof_ctrt_with_tok: pv.TokCtrtWithoutSplit,
    ) -> pv.VStableSwapCtrt:
        """
        new_v_option_ctrt is the fixture that registers a new V Option contract.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_base_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues base tokens right after it.
            new_target_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues target tokens right after it.
            new_option_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues option tokens right after it.
            new_proof_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues proof tokens right after it.

        Returns:
            pv.VStableSwapCtrt: The VStableSwapCtrt instance.
        """
        base_tc = new_base_ctrt_with_tok
        target_tc = new_target_ctrt_with_tok
        option_tc = new_option_ctrt_with_tok
        proof_tc = new_proof_ctrt_with_tok

        base_tok_id = pv.Ctrt.get_tok_id(base_tc.ctrt_id, 0)
        target_tok_id = pv.Ctrt.get_tok_id(target_tc.ctrt_id, 0)
        option_tok_id = pv.Ctrt.get_tok_id(option_tc.ctrt_id, 0)
        proof_tok_id = pv.Ctrt.get_tok_id(proof_tc.ctrt_id, 0)

        oc = await pv.VOptionCtrt.register(
            acnt0,
            base_tok_id,
            target_tok_id,
            option_tok_id,
            proof_tok_id,
            int(time.time() + 50),
            int(time.time() + 95),
        )
        await cft.wait_for_block()

        await asyncio.gather(
            base_tc.deposit(acnt0, oc.ctrt_id, 1000),
            target_tc.deposit(acnt0, oc.ctrt_id, 1000),
            option_tc.deposit(acnt0, oc.ctrt_id, 1000),
            proof_tc.deposit(acnt0, oc.ctrt_id, 1000),
        )
        await cft.wait_for_block()

        return oc

    @pytest.fixture
    async def new_v_option_ctrt_activated_and_minted(
        self,
        acnt0: pv.Account,
        new_v_option_ctrt: pv.VOptionCtrt,
    ) -> pv.VOptionCtrt:
        """
        new_v_option_ctrt is the fixture that registers a new V Option contract.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_base_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues base tokens right after it.
            new_target_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues target tokens right after it.
            new_option_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues option tokens right after it.
            new_proof_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues proof tokens right after it.

        Returns:
            pv.VOptionCtrt: The VOptionCtrt instance.
        """
        oc = new_v_option_ctrt

        await oc.activate(acnt0, 1000, 10, 1)
        await cft.wait_for_block()

        await oc.mint(acnt0, 100)
        await cft.wait_for_block()

        return oc

    async def test_register(
        self,
        acnt0: pv.Account,
        new_base_ctrt_with_tok: pv.TokCtrtWithoutSplit,
        new_target_ctrt_with_tok: pv.TokCtrtWithoutSplit,
        new_option_ctrt_with_tok: pv.TokCtrtWithoutSplit,
        new_proof_ctrt_with_tok: pv.TokCtrtWithoutSplit,
    ) -> pv.VOptionCtrt:
        """
        test_register tests the method register.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_base_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues base tokens right after it.
            new_target_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues target tokens right after it.
            new_option_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues option tokens right after it.
            new_proof_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues proof tokens right after it.

        Returns:
            pv.VOptionCtrt: The VOptionCtrt instance.
        """
        base_tc = new_base_ctrt_with_tok
        target_tc = new_target_ctrt_with_tok
        option_tc = new_option_ctrt_with_tok
        proof_tc = new_proof_ctrt_with_tok

        base_tok_id = pv.Ctrt.get_tok_id(base_tc.ctrt_id, 0)
        target_tok_id = pv.Ctrt.get_tok_id(target_tc.ctrt_id, 0)
        option_tok_id = pv.Ctrt.get_tok_id(option_tc.ctrt_id, 0)
        proof_tok_id = pv.Ctrt.get_tok_id(proof_tc.ctrt_id, 0)

        oc = await pv.VOptionCtrt.register(
            acnt0,
            base_tok_id,
            target_tok_id,
            option_tok_id,
            proof_tok_id,
            int(time.time() + 50),
            int(time.time() + 96),
        )
        await cft.wait_for_block()

        await asyncio.gather(
            base_tc.deposit(acnt0, oc.ctrt_id, 1000),
            target_tc.deposit(acnt0, oc.ctrt_id, 1000),
            option_tc.deposit(acnt0, oc.ctrt_id, 1000),
            proof_tc.deposit(acnt0, oc.ctrt_id, 1000),
        )
        await cft.wait_for_block()

        assert (await oc.maker) == acnt0.addr.b58_str
        return oc

    async def test_activate(
        self, acnt0: pv.Account, new_v_option_ctrt: pv.VOptionCtrt
    ) -> None:
        """
        test_activate tests the method activate.

        Args:
            new_v_option_ctrt (pv.VOptionCtrt): The fixture that registers a new V Option contract.
        """
        oc = new_v_option_ctrt
        api = acnt0.api

        resp = await oc.activate(acnt0, 1000, 10, 1)
        await cft.wait_for_block()
        activate_tx_id = resp["id"]
        await cft.assert_tx_success(api, activate_tx_id)

        a = await oc.max_issue_num
        assert a.data == 1000

    async def test_mint(
        self, acnt0: pv.Account, new_v_option_ctrt: pv.VOptionCtrt
    ) -> None:
        """
        test_mint tests the method mint.

        Args:
            new_v_option_ctrt (pv.VOptionCtrt): The fixture that registers a new V Option contract.
        """
        oc = new_v_option_ctrt
        api = acnt0.api

        await oc.activate(acnt0, 1000, 10, 1)
        await cft.wait_for_block()

        resp = await oc.mint(acnt0, 100)
        await cft.wait_for_block()
        mint_tx_id = resp["id"]
        await cft.assert_tx_success(api, mint_tx_id)

        a = await oc.get_target_tok_bal(acnt0.addr.b58_str)
        assert a.data == 900

    async def test_unlock(
        self, acnt0: pv.Account, new_v_option_ctrt_activated_and_minted: pv.VOptionCtrt
    ) -> None:
        """
        test_unlock tests the method unlock.

        Args:
            new_v_option_ctrt_activated_and_minted (pv.VOptionCtrt): The fixture that registers a new V Option contract activated and minted.
        """
        oc = new_v_option_ctrt_activated_and_minted
        api = acnt0.api

        resp = await oc.unlock(acnt0, 100)
        await cft.wait_for_block()
        unlock_tx_id = resp["id"]
        await cft.assert_tx_success(api, unlock_tx_id)

        b = await oc.get_target_tok_bal(acnt0.addr.b58_str)
        assert b.data == 1000

        await oc.mint(acnt0, 100)
        await cft.wait_for_block()

    async def test_execute_and_collect(
        self, acnt0: pv.Account, new_v_option_ctrt_activated_and_minted: pv.VOptionCtrt
    ) -> None:
        """
        test_execute_and_collect tests the method execute and collect.

        Args:
            new_v_option_ctrt_activated_and_minted (pv.VOptionCtrt): The fixture that registers a new V Option contract activated and minted.
        """
        oc = new_v_option_ctrt_activated_and_minted
        api = acnt0.api

        a = await oc.get_target_tok_bal(acnt0.addr.b58_str)
        assert a.data == 900

        await asyncio.sleep(cft.AVG_BLOCK_DELAY * 6)

        exe_tx = await oc.execute(acnt0, 10)
        await cft.wait_for_block()
        exe_tx_id = exe_tx["id"]
        await cft.assert_tx_success(api, exe_tx_id)

        b = await oc.get_target_tok_bal(acnt0.addr.b58_str)
        assert b.data == 910

        await asyncio.sleep(cft.AVG_BLOCK_DELAY * 5)

        col_tx = await oc.collect(acnt0, 100)
        await cft.wait_for_block()
        col_tx_id = col_tx["id"]
        await cft.assert_tx_success(api, col_tx_id)

        b = await oc.get_target_tok_bal(acnt0.addr.b58_str)
        assert b.data == 1000

    @pytest.mark.whole
    async def test_as_whole(
        self,
        acnt0: pv.Account,
        new_base_ctrt_with_tok: pv.TokCtrtWithoutSplit,
        new_target_ctrt_with_tok: pv.TokCtrtWithoutSplit,
        new_option_ctrt_with_tok: pv.TokCtrtWithoutSplit,
        new_proof_ctrt_with_tok: pv.TokCtrtWithoutSplit,
    ) -> None:
        """
        test_as_whole tests methods of VOptionVtrt as a whole so as to reduce resource consumption.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_base_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues base tokens right after it.
            new_target_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues target tokens right after it.
            new_option_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues option tokens right after it.
            new_proof_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues proof tokens right after it.
        """
        option_ctrt = await self.test_register(
            acnt0,
            new_base_ctrt_with_tok,
            new_target_ctrt_with_tok,
            new_option_ctrt_with_tok,
            new_proof_ctrt_with_tok,
        )
        await self.test_activate(acnt0, option_ctrt)
        await self.test_mint(acnt0, option_ctrt)
        await self.test_unlock(acnt0, option_ctrt)
        await self.test_execute_and_collect(acnt0, option_ctrt)
