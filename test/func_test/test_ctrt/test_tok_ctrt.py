import pytest

import py_v_sdk as pv
from test.func_test import conftest as cft


class TestTokCtrtWithoutSplit:
    """
    TestTokCtrtWithoutSplit is the collection of functional tests of Token contract without split.
    """

    @pytest.fixture
    async def new_ctrt(self, acnt0: pv.Account) -> pv.TokenCtrtWithoutSplit:
        """
        new_ctrt is the fixture that registers a new token contract.

        Args:
            acnt0 (pv.Account): the account of nonce 0.

        Returns:
            pv.TokenCtrtWithoutSplit: the TokenCtrtWithoutSplit instance.
        """
        tc = await pv.TokenCtrtWithoutSplit.register(acnt0, 50, 1)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_ctrt_with_tok(
        self, new_ctrt: pv.TokenCtrtWithoutSplit, acnt0: pv.Account
    ) -> pv.TokenCtrtWithoutSplit:
        """
        new_ctrt_with_tok is the fixture that registers a new TokenWithoutSplit contract and issues tokens right after it.

        Args:
            new_ctrt (pv.TokenCtrtWithoutSplit): The fixture that registers a new TokenWithoutSplit contract.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokenCtrtWithoutSplit: The TokenCtrtWithoutSplit instance.
        """
        tc = new_ctrt
        await tc.issue(acnt0, 50)
        await cft.wait_for_block()
        return tc

    @pytest.fixture
    async def new_atomic_swap_ctrt(
        self,
        new_ctrt_with_tok: pv.TokenCtrtWithoutSplit,
        acnt0: pv.Account,
    ) -> pv.AtomicSwapCtrt:
        """
        new_atomic_swap_ctrt is the fixture that registers a new atomic swap contract.

        Args:
            new_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new token contract and issues tokens right after it.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.AtomicSwapCtrt: The AtomicSwapCtrt instance.
        """
        tc = new_ctrt_with_tok

        ac = await pv.AtomicSwapCtrt.register(acnt0, tc.tok_id.data)

        await cft.wait_for_block()
        assert (await ac.maker) == acnt0.addr.data
        assert (await ac.token_id) == tc.tok_id.data

        return ac

    async def test_register(self, acnt0: pv.Account) -> pv.TokenCtrtWithoutSplit:
        """
        test_register tests the method register.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokenCtrtWithoutSplit: The TokenCtrtWithoutSplit instance.
        """
        tc = await pv.TokenCtrtWithoutSplit.register(acnt0, 50, 1)
        await cft.wait_for_block()
        assert (await tc.issuer).data == acnt0.addr.data
        assert (await tc.maker).data == acnt0.addr.data

        return tc

    async def test_issue(self, new_ctrt: pv.TokenCtrtWithoutSplit, acnt0: pv.Account):
        """
        test_issue tests the method issue.

        Args:
            new_ctrt (pv.TokenCtrtWithoutSplit): The fixture that registers a new token contract without split.
            acnt0 (pv.Account): The account of nonce 0.
        """
        tc = new_ctrt
        api = tc.chain.api

        resp = await tc.issue(acnt0, 50)
        await cft.wait_for_block()

        await cft.assert_tx_success(api, resp["id"])

        tok_bal = await cft.get_tok_bal(api, acnt0.addr.data, tc.tok_id.data)
        assert tok_bal == 50

    async def test_send(
        self,
        new_ctrt_with_tok: pv.TokenCtrtWithoutSplit,
        acnt0: pv.Account,
        acnt1: pv.Account,
    ):
        """
        test_send tests the method send

        Args:
            new_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new token contract and issues tokens right after it.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        tc = new_ctrt_with_tok
        api = tc.chain.api

        tok_bal_acnt0 = await cft.get_tok_bal(api, acnt0.addr.data, tc.tok_id.data)
        assert tok_bal_acnt0 == 50

        tok_bal_acnt1 = await cft.get_tok_bal(api, acnt1.addr.data, tc.tok_id.data)
        assert tok_bal_acnt1 == 0

        resp = await tc.send(acnt0, acnt1.addr.data, 50)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        tok_bal_acnt0 = await cft.get_tok_bal(api, acnt0.addr.data, tc.tok_id.data)
        assert tok_bal_acnt0 == 0

        tok_bal_acnt1 = await cft.get_tok_bal(api, acnt1.addr.data, tc.tok_id.data)
        assert tok_bal_acnt1 == 50

    async def test_transfer(
        self,
        new_ctrt_with_tok: pv.TokenCtrtWithoutSplit,
        acnt0: pv.Account,
        acnt1: pv.Account,
    ):
        """
        test_transfer tests the method transfer.

        Args:
            new_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new token contract and issues tokens right after it.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        tc = new_ctrt_with_tok
        api = tc.chain.api

        tok_bal_acnt0 = await cft.get_tok_bal(api, acnt0.addr.data, tc.tok_id.data)
        assert tok_bal_acnt0 == 50

        tok_bal_acnt1 = await cft.get_tok_bal(api, acnt1.addr.data, tc.tok_id.data)
        assert tok_bal_acnt1 == 0

        resp = await tc.transfer(acnt0, acnt0.addr.data, acnt1.addr.data, 50)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        tok_bal_acnt0 = await cft.get_tok_bal(api, acnt0.addr.data, tc.tok_id.data)
        assert tok_bal_acnt0 == 0

        tok_bal_acnt1 = await cft.get_tok_bal(api, acnt1.addr.data, tc.tok_id.data)
        assert tok_bal_acnt1 == 50

    async def test_deposit_and_withdraw(
        self,
        new_ctrt_with_tok: pv.TokenCtrtWithoutSplit,
        new_atomic_swap_ctrt: pv.AtomicSwapCtrt,
        acnt0: pv.Account,
    ):
        """
        test_deposit_and_withdraw tests the method deposit & withdraw.

        Args:
            new_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new token contract and issues tokens right after it.
            new_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract.
            acnt0 (pv.Account): The account of nonce 0.
        """
        tc = new_ctrt_with_tok
        api = tc.chain.api

        ac = new_atomic_swap_ctrt
        await cft.wait_for_block()
        assert (await ac.maker) == acnt0.addr.data
        assert (await ac.token_id) == tc.tok_id.data

        tok_bal = await cft.get_tok_bal(api, acnt0.addr.data, tc.tok_id.data)
        assert tok_bal == 50

        resp = await tc.deposit(acnt0, ac.ctrt_id, 10)
        await cft.wait_for_block()
        tx_info = await api.tx.get_info(resp["id"])
        assert tx_info["status"] == "Success"

        tok_bal = await cft.get_tok_bal(api, acnt0.addr.data, tc.tok_id.data)
        assert tok_bal == 40

        deposited_tok_bal = await ac.get_swap_balance(acnt0.addr.data)
        assert deposited_tok_bal.amount == 10

        # withdraw
        await tc.withdraw(acnt0, ac.ctrt_id, 10)
        await cft.wait_for_block()

        tok_bal = await cft.get_tok_bal(api, acnt0.addr.data, tc.tok_id.data)
        assert tok_bal == 50

        deposited_tok_bal = await ac.get_swap_balance(acnt0.addr.data)
        assert deposited_tok_bal.amount == 0

    async def test_destroy(
        self, new_ctrt_with_tok: pv.TokenCtrtWithoutSplit, acnt0: pv.Account
    ):
        """
        test_destroy tests the method destroy.
        Args:
            new_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new token contract and issues tokens right after it.
        """
        tc = new_ctrt_with_tok
        api = tc.chain.api

        tok_bal = await cft.get_tok_bal(api, acnt0.addr.data, tc.tok_id.data)
        assert tok_bal == 50

        resp = await tc.destroy(acnt0, 10)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        tok_bal_acnt0 = await cft.get_tok_bal(api, acnt0.addr.data, tc.tok_id.data)
        assert tok_bal_acnt0 == 40

    async def test_supersede(
        self, new_ctrt: pv.TokenCtrtWithoutSplit, acnt0: pv.Account, acnt1: pv.Account
    ):
        """
        test_supersede tests the method supersede.

        Args:
            new_ctrt (pv.TokenCtrtWithoutSplit): The fixture that registers a new token contract.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        tc = new_ctrt
        api = tc.chain.api

        assert (await tc.issuer).data == acnt0.addr.data

        resp = await tc.supersede(acnt0, acnt1.addr.data)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await tc.issuer).data == acnt1.addr.data

    @pytest.mark.whole
    async def test_as_whole(
        self,
        new_ctrt_with_tok: pv.TokenCtrtWithoutSplit,
        new_atomic_swap_ctrt: pv.AtomicSwapCtrt,
        acnt0: pv.Account,
        acnt1: pv.Account,
    ):
        """
        test_as_whole tests methods of TokenWithSplitCtrt as a whole so as to reduce resource consumption.

        Args:
            new_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new token contract and issues tokens right after it.
            new_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        tc = await self.test_register(acnt0)
        await self.test_issue(tc, acnt0)

        tc = new_ctrt_with_tok
        ac = new_atomic_swap_ctrt

        await self.test_send(tc, acnt0, acnt1)
        await self.test_transfer(tc, acnt1, acnt0)
        await self.test_deposit_and_withdraw(tc, ac, acnt0)
        await self.test_destroy(tc, acnt0)
        await self.test_supersede(tc, acnt0, acnt1)


class TestTokWithSplit(TestTokCtrtWithoutSplit):
    """
    TestTokCtrtWithSplit is the collection of functional tests of Token contract with split.
    """

    @pytest.fixture
    async def new_ctrt(self, acnt0: pv.Account) -> pv.TokenCtrtWithSplit:
        """
        new_ctrt is the fixture that registers a new token contract with split.

        Args:
            acnt0 (pv.Account): the account of nonce 0.

        Returns:
            pv.TokenCtrtWithoutSplit: the TokenCtrtWithSplit instance.
        """
        tc = await pv.TokenCtrtWithSplit.register(acnt0, 50, 1)
        await cft.wait_for_block()
        return tc

    async def test_split(self, new_ctrt: pv.TokenCtrtWithSplit, acnt0: pv.Account):
        """
        test_split tests the method split.

        Args:
            new_ctrt (pv.TokenCtrtWithSplit): The fixture that registers a new token contract.
            acnt0 (pv.Account): The account of nonce 0.
        """
        tc = new_ctrt
        api = tc.chain.api

        resp = await tc.split(acnt0, 12)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        new_unit = await api.ctrt.get_tok_info(tc.tok_id.data)
        assert 12 == new_unit["unity"]


class TestTokWithoutSplitV2WhiteList(TestTokCtrtWithoutSplit):
    """
    TestTokWithoutSplitV2WhiteList is the collection of functional tests of Token contract with white list.
    """

    @pytest.fixture
    async def new_ctrt(
        self, acnt0: pv.Account, acnt1: pv.Account
    ) -> pv.TokenCtrtWithoutSplitV2WhiteList:
        """
        new_ctrt is the fixture that registers a new token contract with white list.

        Args:
            acnt0 (pv.Account): the account of nonce 0.

        Returns:
            pv.TokenCtrtWithoutSplitV2WhiteList: the TokenCtrtWithoutSplitV2WhiteList instance.
        """
        tc = await pv.TokenCtrtWithoutSplitV2WhiteList.register(acnt0, 50, 1)
        await cft.wait_for_block()

        await tc.update_list_user(acnt0, acnt0.addr.data, True)
        await tc.update_list_user(acnt0, acnt1.addr.data, True)
        return tc

    @pytest.fixture
    def arbitrary_ctrt_id(self) -> str:
        """
        arbitrary_ctrt_id is the fixture that returns an arbitrary contract ID

        Returns:
            str: The contract ID.
        """
        return "CEzFs69VesVBHTefZVVCAddcbMzMQAjchCX"

    @pytest.fixture
    async def new_atomic_swap_ctrt(
        self,
        new_ctrt_with_tok: pv.TokenCtrtWithoutSplitV2WhiteList,
        acnt0: pv.Account,
    ) -> pv.AtomicSwapCtrt:
        """
        new_atomic_swap_ctrt is the fixture that registers a new atomic swap contract.

        Args:
            new_ctrt_with_tok (pv.TokenCtrtWithoutSplitV2WhiteList): The fixture that registers a new token contract and issues a token right after it.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.AtomicSwapCtrt: The AtomicSwapCtrt instance.
        """
        tc = new_ctrt_with_tok
        api = tc.chain.api

        ac = await pv.AtomicSwapCtrt.register(acnt0, tc.tok_id.data)

        await cft.wait_for_block()
        assert (await ac.maker) == acnt0.addr.data
        assert (await ac.token_id) == tc.tok_id.data

        resp = await tc.update_list_ctrt(acnt0, ac.ctrt_id, True)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        return ac

    async def test_supersede(
        self,
        new_ctrt: pv.TokenCtrtWithoutSplitV2WhiteList,
        acnt0: pv.Account,
        acnt1: pv.Account,
    ):
        """
        test_supersede tests the method supersede.

        Args:
            new_ctrt (pv.TokenCtrtWithoutSplitV2WhiteList): The fixture that registers a new token contract V2 with whitelist.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """

        tc = new_ctrt
        api = tc.chain.api

        assert (await tc.issuer).data == acnt0.addr.data
        assert (await tc.regulator).data == acnt0.addr.data

        resp = await tc.supersede(acnt0, acnt1.addr.data, acnt1.addr.data)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await tc.issuer).data == acnt1.addr.data
        assert (await tc.regulator).data == acnt1.addr.data

    async def test_update_list_user(
        self,
        new_ctrt: pv.TokenCtrtWithoutSplitV2WhiteList,
        acnt0: pv.Account,
        acnt1: pv.Account,
    ):
        """
        test_update_list_user tests the method update_list_user.

        Args:
            new_ctrt (pv.TokenCtrtWithoutSplitV2WhiteList): The fixture that registers a new token contract V2 with whitelist.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """

        tc = new_ctrt
        api = tc.chain.api

        in_list = await tc.is_user_in_list(acnt1.addr.data)
        assert in_list == False

        resp = await tc.update_list_user(
            by=acnt0,
            addr=acnt1.addr.data,
            val=True,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        in_list = await tc.is_user_in_list(acnt1.addr.data)
        assert in_list == True

        resp = await tc.update_list_user(
            by=acnt0,
            addr=acnt1.addr.data,
            val=False,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        in_list = await tc.is_user_in_list(acnt1.addr.data)
        assert in_list == False

    async def test_update_list_ctrt(
        self,
        new_ctrt: pv.TokenCtrtWithoutSplitV2WhiteList,
        acnt0: pv.Account,
        arbitrary_ctrt_id: str,
    ):
        """
        test_update_list_ctrt tests the method update_list_ctrt.

        Args:
            new_ctrt (pv.TokenCtrtWithoutSplitV2WhiteList): The fixture that registers a new token contract V2 with whitelist.
            acnt0 (pv.Account): The account of nonce 0.
            arbitrary_ctrt_id (str): An arbitrary contract ID
        """
        tc = new_ctrt
        api = tc.chain.api
        target_ctrt_id = arbitrary_ctrt_id

        in_list = await tc.is_ctrt_in_list(target_ctrt_id)
        assert in_list == False

        resp = await tc.update_list_ctrt(
            by=acnt0,
            addr=target_ctrt_id,
            val=True,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        in_list = await tc.is_ctrt_in_list(target_ctrt_id)
        assert in_list == True

        resp = await tc.update_list_ctrt(
            by=acnt0,
            addr=target_ctrt_id,
            val=False,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        in_list = await tc.is_ctrt_in_list(target_ctrt_id)
        assert in_list == False

    async def test_register(
        self, acnt0: pv.Account
    ) -> pv.TokenCtrtWithoutSplitV2WhiteList:
        """
        test_register tests the method register.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokenCtrtWithoutSplitV2WhiteList: The registered TokenCtrtWithoutSplitV2WhiteList
        """
        tc = await pv.TokenCtrtWithoutSplitV2WhiteList.register(acnt0, 50, 1)
        await cft.wait_for_block()
        assert (await tc.issuer).data == acnt0.addr.data
        assert (await tc.maker).data == acnt0.addr.data
        assert (await tc.regulator).data == acnt0.addr.data

        return tc


class TestTokWithoutSplitV2BlackList(TestTokWithoutSplitV2WhiteList):
    """
    TestTokWithoutSplitV2BlackList is the collection of functional tests of token contract V2 with blacklist.
    """

    @pytest.fixture
    async def new_ctrt(self, acnt0: pv.Account) -> pv.TokenCtrtWithoutSplitV2BlackList:
        """
        new_ctrt is the fixture that registers a new token contract V2 with blacklist.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.

        Returns:
            pv.TokenCtrtWithoutSplitV2BlackList: The TokenCtrtWithoutSplitV2BlackList instance.
        """
        tc = await pv.TokenCtrtWithoutSplitV2BlackList.register(acnt0, 50, 1)
        await cft.wait_for_block()

        return tc

    @pytest.fixture
    async def new_atomic_swap_ctrt(
        self,
        new_ctrt_with_tok: pv.TokenCtrtWithoutSplitV2BlackList,
        acnt0: pv.Account,
    ) -> pv.AtomicSwapCtrt:
        """
        new_atomic_swap_ctrt is the fixture that registers a new atomic swap contract.

        Args:
            new_ctrt_with_tok (pv.TokenCtrtWithoutSplitV2BlackList): The fixture that registers a new token contract and issues tokens right after it.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.AtomicSwapCtrt: The AtomicSwapCtrt instance.
        """
        tc = new_ctrt_with_tok

        ac = await pv.AtomicSwapCtrt.register(acnt0, tc.tok_id.data)

        await cft.wait_for_block()
        assert (await ac.maker) == acnt0.addr.data
        assert (await ac.token_id) == tc.tok_id.data

        return ac
