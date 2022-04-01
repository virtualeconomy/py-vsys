import pytest
import time
import asyncio

import py_vsys as pv
from test.func_test import conftest as cft


class TestVOptionCtrt:
    """
    TestVOptionCtrt is the collection of functional tests of V Option contract.
    """

    MAX_ISSUE_AMOUNT = 1000
    MINT_AMOUNT = 200
    UNLOCK_AMOUNT = 100
    EXEC_TIME_DELTA = 50
    EXEC_DDL_DELTA = 95

    @pytest.fixture
    async def new_base_tok_ctrt(self, acnt0: pv.Account) -> pv.TokCtrtWithoutSplit:
        """
        new_base_tok_ctrt is the fixture that registers a new base token contract.

        Args:
            acnt0 (pv.Account): the account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: the TokCtrtWithoutSplit instance.
        """
        tc = await pv.TokCtrtWithoutSplit.register(acnt0, 1000, 1)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_target_tok_ctrt(self, acnt0: pv.Account) -> pv.TokCtrtWithoutSplit:
        """
        new_target_tok_ctrt is the fixture that registers a new target token contract.

        Args:
            acnt0 (pv.Account): the account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: the TokCtrtWithoutSplit instance.
        """
        tc = await pv.TokCtrtWithoutSplit.register(acnt0, 1000, 1)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_option_tok_ctrt(self, acnt0: pv.Account) -> pv.TokCtrtWithoutSplit:
        """
        new_option_tok_ctrt is the fixture that registers a new option token contract.

        Args:
            acnt0 (pv.Account): the account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: the TokCtrtWithoutSplit instance.
        """
        tc = await pv.TokCtrtWithoutSplit.register(acnt0, 1000, 1)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_proof_tok_ctrt(self, acnt0: pv.Account) -> pv.TokCtrtWithoutSplit:
        """
        new_proof_tok_ctrt is the fixture that registers a new proof token contract.

        Args:
            acnt0 (pv.Account): the account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: the TokCtrtWithoutSplit instance.
        """
        tc = await pv.TokCtrtWithoutSplit.register(acnt0, 1000, 1)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_base_tok_ctrt_with_tok(
        self, new_base_tok_ctrt: pv.TokCtrtWithoutSplit, acnt0: pv.Account
    ) -> pv.TokCtrtWithoutSplit:
        """
        new_base_tok_ctrt_with_tok is the fixture that registers a new TokenWithoutSplit contract and issues base tokens right after it.

        Args:
            new_base_tok_ctrt (pv.TokCtrtWithoutSplit): The fixture that registers a new TokenWithoutSplit contract.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: The TokCtrtWithoutSplit instance.
        """
        tc = new_base_tok_ctrt
        await tc.issue(acnt0, 1000)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_target_tok_ctrt_with_tok(
        self, new_target_tok_ctrt: pv.TokCtrtWithoutSplit, acnt0: pv.Account
    ) -> pv.TokCtrtWithoutSplit:
        """
        new_target_tok_ctrt_with_tok is the fixture that registers a new TokenWithoutSplit contract and issues target tokens right after it.

        Args:
            new_target_tok_ctrt (pv.TokCtrtWithoutSplit): The fixture that registers a new TokenWithoutSplit contract.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: The TokCtrtWithoutSplit instance.
        """
        tc = new_target_tok_ctrt
        await tc.issue(acnt0, 1000)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_option_tok_ctrt_with_tok(
        self, new_option_tok_ctrt: pv.TokCtrtWithoutSplit, acnt0: pv.Account
    ) -> pv.TokCtrtWithoutSplit:
        """
        new_option_tok_ctrt_with_tok is the fixture that registers a new TokenWithoutSplit contract and issues option tokens right after it.

        Args:
            new_option_tok_ctrt (pv.TokCtrtWithoutSplit): The fixture that registers a new TokenWithoutSplit contract.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: The TokCtrtWithoutSplit instance.
        """
        tc = new_option_tok_ctrt
        await tc.issue(acnt0, 1000)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_proof_tok_ctrt_with_tok(
        self, new_proof_tok_ctrt: pv.TokCtrtWithoutSplit, acnt0: pv.Account
    ) -> pv.TokCtrtWithoutSplit:
        """
        new_proof_tok_ctrt_with_tok is the fixture that registers a new TokenWithoutSplit contract and issues proof tokens right after it.

        Args:
            new_proof_tok_ctrt (pv.TokCtrtWithoutSplit): The fixture that registers a new TokenWithoutSplit contract.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokCtrtWithoutSplit: The TokCtrtWithoutSplit instance.
        """
        tc = new_proof_tok_ctrt
        await tc.issue(acnt0, 1000)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_v_option_ctrt(
        self,
        acnt0: pv.Account,
        new_base_tok_ctrt_with_tok: pv.TokCtrtWithoutSplit,
        new_target_tok_ctrt_with_tok: pv.TokCtrtWithoutSplit,
        new_option_tok_ctrt_with_tok: pv.TokCtrtWithoutSplit,
        new_proof_tok_ctrt_with_tok: pv.TokCtrtWithoutSplit,
    ) -> pv.VStableSwapCtrt:
        """
        new_v_option_ctrt is the fixture that registers a new V Option contract.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_base_tok_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues base tokens right after it.
            new_target_tok_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues target tokens right after it.
            new_option_tok_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues option tokens right after it.
            new_proof_tok_ctrt_with_tok (pv.TokCtrtWithoutSplit): The fixture that registers a new token contract without split and issues proof tokens right after it.

        Returns:
            pv.VStableSwapCtrt: The VStableSwapCtrt instance.
        """
        base_tc = new_base_tok_ctrt_with_tok
        target_tc = new_target_tok_ctrt_with_tok
        option_tc = new_option_tok_ctrt_with_tok
        proof_tc = new_proof_tok_ctrt_with_tok

        base_tok_id = pv.Ctrt.get_tok_id(base_tc.ctrt_id, pv.TokenIdx(0))
        target_tok_id = pv.Ctrt.get_tok_id(target_tc.ctrt_id, pv.TokenIdx(0))
        option_tok_id = pv.Ctrt.get_tok_id(option_tc.ctrt_id, pv.TokenIdx(0))
        proof_tok_id = pv.Ctrt.get_tok_id(proof_tc.ctrt_id, pv.TokenIdx(0))

        oc = await pv.VOptionCtrt.register(
            acnt0,
            base_tok_id.data,
            target_tok_id.data,
            option_tok_id.data,
            proof_tok_id.data,
            int(time.time() + self.EXEC_TIME_DELTA),
            int(time.time() + self.EXEC_DDL_DELTA),
        )
        await cft.wait_for_block()

        await asyncio.gather(
            base_tc.deposit(acnt0, oc.ctrt_id.data, 1000),
            target_tc.deposit(acnt0, oc.ctrt_id.data, 1000),
            option_tc.deposit(acnt0, oc.ctrt_id.data, 1000),
            proof_tc.deposit(acnt0, oc.ctrt_id.data, 1000),
        )
        await cft.wait_for_block()

        return oc

    @pytest.fixture
    async def new_v_option_ctrt_activated(
        self,
        acnt0: pv.Account,
        new_v_option_ctrt: pv.VOptionCtrt,
    ) -> pv.VOptionCtrt:
        """
        new_v_option_ctrt_activated is the fixture that registers a new V Option contract and activate it.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_v_option_ctrt (pv.VOptionCtrt): The fixture that registers a new V Option contract.

        Returns:
            pv.VOptionCtrt: The VOptionCtrt instance.
        """
        oc = new_v_option_ctrt
        api = acnt0.api

        resp = await oc.activate(
            by=acnt0,
            max_issue_num=self.MAX_ISSUE_AMOUNT,
            price=10,
            price_unit=1,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        return oc

    @pytest.fixture
    async def new_v_option_ctrt_activated_and_minted(
        self,
        acnt0: pv.Account,
        new_v_option_ctrt_activated: pv.VOptionCtrt,
    ) -> pv.VOptionCtrt:
        """
        new_v_option_ctrt_activated_and_minted is the fixture that
        - registers a new V Option contract.
        - activate it
        - mint option tokens

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_v_option_ctrt_activated (pv.VOptionCtrt): The fixture that registers a new V Option contract & activates it.

        Returns:
            pv.VOptionCtrt: The VOptionCtrt instance.
        """
        oc = new_v_option_ctrt_activated
        api = acnt0.api

        resp = await oc.mint(
            by=acnt0,
            amount=self.MINT_AMOUNT,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        return oc

    async def test_register(
        self,
        acnt0: pv.Account,
        new_v_option_ctrt: pv.VOptionCtrt,
    ) -> pv.VOptionCtrt:
        """
        test_register tests the method register.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_v_option_ctrt (pv.VOptionCtrt): The fixture that registers a new V Option contract.

        Returns:
            pv.VOptionCtrt: The VOptionCtrt instance.
        """
        oc = new_v_option_ctrt
        assert (await oc.maker) == acnt0.addr
        return oc

    async def test_activate(self, new_v_option_ctrt_activated: pv.VOptionCtrt) -> None:
        """
        test_activate tests the method activate.

        Args:
            new_v_option_ctrt_activated (pv.VOptionCtrt): The fixture that registers a new V Option contract and activates it.
        """
        oc = new_v_option_ctrt_activated
        assert (await oc.max_issue_num).data == self.MAX_ISSUE_AMOUNT

    async def test_mint(
        self, acnt0: pv.Account, new_v_option_ctrt_activated_and_minted: pv.VOptionCtrt
    ) -> None:
        """
        test_mint tests the method mint.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_v_option_ctrt_activated_and_minted (pv.VOptionCtrt): The fixture that registers a new V Option contract, activates it, and mints option tokens.
        """
        oc = new_v_option_ctrt_activated_and_minted
        assert (await oc.get_target_tok_bal(acnt0.addr.data)).data == (
            self.MAX_ISSUE_AMOUNT - self.MINT_AMOUNT
        )

    async def test_unlock(
        self, acnt0: pv.Account, new_v_option_ctrt_activated_and_minted: pv.VOptionCtrt
    ) -> None:
        """
        test_unlock tests the method unlock.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_v_option_ctrt_activated_and_minted (pv.VOptionCtrt): The fixture that registers a new V Option contract activated and minted.
        """
        oc = new_v_option_ctrt_activated_and_minted
        api = acnt0.api

        resp = await oc.unlock(by=acnt0, amount=self.UNLOCK_AMOUNT)
        await cft.wait_for_block()
        unlock_tx_id = resp["id"]
        await cft.assert_tx_success(api, unlock_tx_id)

        assert (
            await oc.get_target_tok_bal(acnt0.addr.data)
        ).data == self.MAX_ISSUE_AMOUNT - self.MINT_AMOUNT + self.UNLOCK_AMOUNT

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

        exec_amount = 10
        target_tok_bal_init = await oc.get_target_tok_bal(acnt0.addr.data)

        await asyncio.sleep(cft.AVG_BLOCK_DELAY * 6)

        exe_tx = await oc.execute(acnt0, exec_amount)
        await cft.wait_for_block()
        exe_tx_id = exe_tx["id"]
        await cft.assert_tx_success(api, exe_tx_id)

        target_tok_bal_exec = await oc.get_target_tok_bal(acnt0.addr.data)
        assert (target_tok_bal_exec.data - target_tok_bal_init.data) == exec_amount

        await asyncio.sleep(cft.AVG_BLOCK_DELAY * 5)

        col_tx = await oc.collect(acnt0, 10)
        await cft.wait_for_block()
        col_tx_id = col_tx["id"]
        await cft.assert_tx_success(api, col_tx_id)

        target_tok_bal_col = await oc.get_target_tok_bal(acnt0.addr.data)
        assert (target_tok_bal_col.data - target_tok_bal_exec.data) == 9

    @pytest.mark.whole
    async def test_as_whole(
        self,
        acnt0: pv.Account,
        new_v_option_ctrt_activated_and_minted: pv.VOptionCtrt,
    ) -> None:
        """
        test_as_whole tests methods of VOptionVtrt as a whole so as to reduce resource consumption.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_v_option_ctrt_activated_and_minted (pv.VOptionCtrt): The fixture that registers a new V Option contract, activates it, and mints.
        """
        oc = new_v_option_ctrt_activated_and_minted
        await self.test_register(acnt0, oc)
        await self.test_activate(oc)
        await self.test_mint(acnt0, oc)
        await self.test_unlock(acnt0, oc)
        await self.test_execute_and_collect(acnt0, oc)
