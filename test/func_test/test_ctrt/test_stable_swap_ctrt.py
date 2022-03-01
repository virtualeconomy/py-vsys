import pytest
import time

import py_v_sdk as pv
from test.func_test import conftest as cft


class TestStableSwapCtrt:
    """
    TestStableSwapCtrt is the collection of functional tests of stable swap contract.
    """

    @pytest.fixture
    async def new_base_ctrt(self, acnt0: pv.Account) -> pv.TokenCtrtWithoutSplit:
        """
        new_base_ctrt is the fixture that registers a new base token contract.

        Args:
            acnt0 (pv.Account): the account of nonce 0.

        Returns:
            pv.TokenCtrtWithoutSplit: the TokenCtrtWithoutSplit instance.
        """
        tc = await pv.TokenCtrtWithoutSplit.register(acnt0, 1000, 1)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_base_ctrt_with_tok(
        self, new_base_ctrt: pv.TokenCtrtWithoutSplit, acnt0: pv.Account
    ) -> pv.TokenCtrtWithoutSplit:
        """
        new_base_ctrt_with_tok is the fixture that registers a new TokenWithoutSplit contract and issues base tokens right after it.

        Args:
            new_base_ctrt (pv.TokenCtrtWithoutSplit): The fixture that registers a new TokenWithoutSplit contract.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokenCtrtWithoutSplit: The TokenCtrtWithoutSplit instance.
        """
        tc = new_base_ctrt
        await tc.issue(acnt0, 1000)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_target_ctrt(self, acnt0: pv.Account) -> pv.TokenCtrtWithoutSplit:
        """
        new_target_ctrt is the fixture that registers a new target token contract.

        Args:
            acnt0 (pv.Account): the account of nonce 0.

        Returns:
            pv.TokenCtrtWithoutSplit: the TokenCtrtWithoutSplit instance.
        """
        tc = await pv.TokenCtrtWithoutSplit.register(acnt0, 1000, 1)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_target_ctrt_with_tok(
        self, new_target_ctrt: pv.TokenCtrtWithoutSplit, acnt0: pv.Account
    ) -> pv.TokenCtrtWithoutSplit:
        """
        new_target_ctrt_with_tok is the fixture that registers a new TokenWithoutSplit contract and issues target tokens right after it.

        Args:
            new_target_ctrt (pv.TokenCtrtWithoutSplit): The fixture that registers a new TokenWithoutSplit contract.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokenCtrtWithoutSplit: The TokenCtrtWithoutSplit instance.
        """
        tc = new_target_ctrt
        await tc.issue(acnt0, 1000)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_stable_ctrt(
        self,
        acnt0: pv.Account,
        new_base_ctrt_with_tok: pv.TokenCtrtWithoutSplit,
        new_target_ctrt_with_tok: pv.TokenCtrtWithoutSplit,
    ) -> pv.VStableSwapCtrt:
        """
        new_stable_ctrt is the fixture that registers a new V Stable Swap contract.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_base_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new token contract without split and issues base tokens right after it.
            new_target_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new token contract without split and issues target tokens right after it.

        Returns:
            pv.VStableSwapCtrt: The VStableSwapCtrt instance.
        """
        base_tc = new_base_ctrt_with_tok
        target_tc = new_target_ctrt_with_tok
        base_tok_id = pv.Ctrt.get_tok_id(base_tc.ctrt_id, 0)
        target_tok_id = pv.Ctrt.get_tok_id(target_tc.ctrt_id, 0)

        ssc = await pv.VStableSwapCtrt.register(
            acnt0, base_tok_id, target_tok_id, 5, 1, 1
        )
        await cft.wait_for_block()
        await base_tc.deposit(acnt0, ssc.ctrt_id, 1000)
        await target_tc.deposit(acnt0, ssc.ctrt_id, 1000)
        await cft.wait_for_block()

        return ssc

    @pytest.fixture
    def order_exist() -> bool:
        """
        order_exist shows whether the order exists or not, in case in test_as_whole creates another order.

        Returns:
            bool: True is exist and false is not.
        """
        return False

    @pytest.fixture
    def exist_order_id() -> str:
        """
        exist_order_id is the existing order id.

        Returns:
            bool: True is exist and false is not.
        """
        return str("ss")

    async def test_register(
        self,
        acnt0: pv.Account,
        new_base_ctrt_with_tok: pv.TokenCtrtWithoutSplit,
        new_target_ctrt_with_tok: pv.TokenCtrtWithoutSplit,
    ) -> pv.VStableSwapCtrt:
        """
        test_register tests the method register.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_base_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new token contract without split and issues base tokens right after it.
            new_target_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new token contract without split and issues target tokens right after it.

        Returns:
            pv.VStableSwapCtrt: The VStableSwapCtrt instance.
        """
        base_tc = new_base_ctrt_with_tok
        target_tc = new_target_ctrt_with_tok
        base_tok_id = pv.Ctrt.get_tok_id(base_tc.ctrt_id, 0)
        target_tok_id = pv.Ctrt.get_tok_id(target_tc.ctrt_id, 0)

        ssc = await pv.VStableSwapCtrt.register(
            acnt0, base_tok_id, target_tok_id, 5, 1, 1
        )
        await cft.wait_for_block()

        await base_tc.deposit(acnt0, ssc.ctrt_id, 1000)
        await target_tc.deposit(acnt0, ssc.ctrt_id, 1000)
        await cft.wait_for_block()

        assert (await ssc.maker) == acnt0.addr.b58_str
        return ssc

    async def test_set_and_update_order(
        self,
        acnt0: pv.Account,
        new_stable_ctrt: pv.VStableSwapCtrt,
    ) -> str:
        """
        test_set_order tests the method set_order.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_stable_ctrt (pv.VStableSwapCtrt): The fixture that registers a new V Stable Swap contract.

        return:
            str: The order id.
        """
        api = acnt0.api
        ssc = new_stable_ctrt

        resp = await ssc.set_order(acnt0, 1, 1, 0, 100, 0, 100, 2, 1, 500, 500)
        await cft.wait_for_block()
        order_id = resp["id"]
        await cft.assert_tx_success(api, order_id)

        base_tok_bal = await ssc.get_base_tok_bal(acnt0.addr.b58_str)
        target_tok_bal = await ssc.get_target_tok_bal(acnt0.addr.b58_str)
        price_base1 = await ssc.get_price_base(order_id)
        assert base_tok_bal.data == 500
        assert target_tok_bal.data == 500
        assert price_base1.data == 2

        resp = await ssc.update_order(
            acnt0, order_id, 1, 1, 0, 100, 0, 100, 1, 1
        )  # update price_base to 1.
        await cft.wait_for_block()
        update_tx_id = resp["id"]
        await cft.assert_tx_success(api, update_tx_id)

        price_base2 = await ssc.get_price_base(order_id)
        assert price_base2.data == 1

        return order_id

    async def test_order_deposit_and_withdraw(
        self,
        acnt0: pv.Account,
        new_stable_ctrt: pv.VStableSwapCtrt,
        order_exist: bool,
        exist_order_id: str,
    ) -> None:
        """
        test_order_deposit_and_withdraw tests the method order_deposit and order_withdraw.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_stable_ctrt (pv.VStableSwapCtrt): The fixture that registers a new V Stable Swap contract.
            order_exist (bool): The boolean that indicates whether the order exists.
            exist_order_id (str): The id of the exist order.
        """
        api = acnt0.api
        ssc = new_stable_ctrt

        if order_exist:
            order_id = exist_order_id
        else:
            set_order_tx = await ssc.set_order(
                acnt0, 1, 1, 0, 100, 0, 100, 1, 1, 500, 500
            )
            await cft.wait_for_block()
            order_id = set_order_tx["id"]
        # set_order_tx = await ssc.set_order(acnt0,1,1,0,100,0,100,1,1,500,500)
        # await cft.wait_for_block()
        # order_id = set_order_tx["id"]

        resp = await ssc.order_deposit(acnt0, order_id, 200, 100)
        await cft.wait_for_block()
        deposit_tx_id = resp["id"]
        await cft.assert_tx_success(api, deposit_tx_id)

        base_tok_bal1 = await ssc.get_base_tok_bal(acnt0.addr.b58_str)
        target_tok_bal1 = await ssc.get_target_tok_bal(acnt0.addr.b58_str)
        assert base_tok_bal1.data == 300
        assert target_tok_bal1.data == 400

        resp = await ssc.order_withdraw(acnt0, order_id, 200, 100)
        await cft.wait_for_block()
        withdraw_tx_id = resp["id"]
        await cft.assert_tx_success(api, withdraw_tx_id)

        base_tok_bal1 = await ssc.get_base_tok_bal(acnt0.addr.b58_str)
        target_tok_bal1 = await ssc.get_target_tok_bal(acnt0.addr.b58_str)
        assert base_tok_bal1.data == 500
        assert target_tok_bal1.data == 500

    async def test_swap(
        self,
        acnt0: pv.Account,
        new_stable_ctrt: pv.VStableSwapCtrt,
        order_exist: bool,
        exist_order_id: str,
    ) -> None:
        """
        test_swap tests the method swap_base_to_target and swap_target_to_base.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_stable_ctrt (pv.VStableSwapCtrt): The fixture that registers a new V Stable Swap contract.
            order_exist (bool): The boolean that indicates whether the order exists.
            exist_order_id (str): The id of the exist order.
        """
        api = acnt0.api
        ssc = new_stable_ctrt
        order_id = exist_order_id

        # if(order_exist):
        #     order_id = exist_order_id
        # else:
        set_order_tx = await ssc.set_order(acnt0, 1, 1, 0, 100, 0, 100, 1, 1, 500, 500)
        await cft.wait_for_block()
        order_id = set_order_tx["id"]

        # test swap_base_to_target
        deadline = int(time.time()) + 1500
        swap1 = await ssc.swap_base_to_target(acnt0, order_id, 10, 1, 1, deadline)
        await cft.wait_for_block()
        swap1_tx_id = swap1["id"]
        await cft.assert_tx_success(api, swap1_tx_id)

        base_tok_bal1 = await ssc.get_base_tok_bal(acnt0.addr.b58_str)
        target_tok_bal1 = await ssc.get_target_tok_bal(acnt0.addr.b58_str)
        assert base_tok_bal1.data == 490
        assert target_tok_bal1.data == 509

        # test swap_target_to_base
        swap2 = await ssc.swap_target_to_base(acnt0, order_id, 10, 1, 1, deadline)
        await cft.wait_for_block()
        swap2_tx_id = swap2["id"]
        await cft.assert_tx_success(api, swap2_tx_id)

        base_tok_bal2 = await ssc.get_base_tok_bal(acnt0.addr.b58_str)
        target_tok_bal2 = await ssc.get_target_tok_bal(acnt0.addr.b58_str)
        assert base_tok_bal2.data == 499
        assert target_tok_bal2.data == 499

    async def test_close_order(
        self,
        acnt0: pv.Account,
        new_stable_ctrt: pv.VStableSwapCtrt,
    ) -> None:
        """
        test_swap tests the method swap_base_to_target and swap_target_to_base.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_stable_ctrt (pv.VStableSwapCtrt): The fixture that registers a new V Stable Swap contract.
        """
        api = acnt0.api
        ssc = new_stable_ctrt

        set_order_tx = await ssc.set_order(acnt0, 1, 1, 0, 100, 0, 100, 1, 1, 500, 500)
        await cft.wait_for_block()
        order_id = set_order_tx["id"]

        assert await ssc.get_order_status(order_id)

        resp = await ssc.close_order(acnt0, order_id)
        await cft.wait_for_block()
        close_tx_id = resp["id"]
        await cft.assert_tx_success(api, close_tx_id)

        assert not await ssc.get_order_status(order_id)

    @pytest.mark.whole
    async def test_as_whole(
        self,
        acnt0: pv.Account,
        new_base_ctrt_with_tok: pv.TokenCtrtWithoutSplit,
        new_target_ctrt_with_tok: pv.TokenCtrtWithoutSplit,
    ) -> None:
        """
        test_as_whole tests methods of VStableSwapCtrt as a whole so as to reduce resource consumption.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_base_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new token contract without split and issues base tokens right after it.
            new_target_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new token contract without split and issues target tokens right after it.

        """
        swap_ctrt = await self.test_register(
            acnt0, new_base_ctrt_with_tok, new_target_ctrt_with_tok
        )

        order_id = await self.test_set_and_update_order(acnt0, swap_ctrt)

        await self.test_order_deposit_and_withdraw(acnt0, swap_ctrt, True, order_id)

        await self.test_set_and_update_order(acnt0, swap_ctrt, True, order_id)

        await self.test_close_order(acnt0, swap_ctrt, swap_ctrt)
