"""
test_ctrt contains functional tests for smart contracts.
"""
import asyncio
import time

import pytest

import py_v_sdk as pv
from . import conftest as cft


async def get_tok_id(api: pv.NodeAPI, ctrt_id: str, tok_idx: int) -> str:
    """
    get_tok_id gets the token ID for the given token index of the contract.

    Args:
        api (pv.NodeAPI): The NodeAPI object.
        ctrt_id (str): The contract ID.
        tok_idx (int): The token index.

    Returns:
        str: The token ID.
    """
    resp = await api.ctrt.get_tok_id(ctrt_id, tok_idx)
    return resp["tokenId"]


async def get_tok_bal(api: pv.NodeAPI, addr: str, tok_id: str) -> int:
    """
    get_tok_bal gets the token balance of the given token ID.

    Args:
        api (pv.NodeAPI): The NodeAPI object.
        addr (str): The account address.
        tok_id (str): The token ID.

    Returns:
        int: The balance.
    """
    resp = await api.ctrt.get_tok_bal(addr, tok_id)
    return resp["balance"]


class TestNFTCtrt:
    """
    TestNFTCtrt is the collection of functional tests of NFT contract.
    """

    @pytest.fixture
    async def new_ctrt(self, acnt0: pv.Account) -> pv.NFTCtrt:
        """
        new_ctrt is the fixture that registers a new NFT contract.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.NFTCtrt: The NFTCtrt instance.
        """
        nc = await pv.NFTCtrt.register(acnt0)
        await cft.wait_for_block()
        return nc

    @pytest.fixture
    async def new_ctrt_with_tok(
        self, new_ctrt: pv.NFTCtrt, acnt0: pv.Account
    ) -> pv.NFTCtrt:
        """
        new_ctrt_with_tok is the fixture that registers a new NFT contract and issues an NFT token right after it.

        Args:
            new_ctrt (pv.NFTCtrt): The fixture that registers a new NFT contract.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.NFTCtrt: The NFTCtrt instance.
        """
        nc = new_ctrt
        await nc.issue(acnt0)
        await cft.wait_for_block()
        return nc

    @pytest.fixture
    async def new_atomic_swap_ctrt(
        self,
        new_ctrt_with_tok: pv.NFTCtrt,
        acnt0: pv.Account,
    ) -> pv.AtomicSwapCtrt:
        """
        new_atomic_swap_ctrt is the fixture that registers a new atomic swap contract.

        Args:
            new_ctrt_with_tok (pv.NFTCtrt): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.AtomicSwapCtrt: The AtomicSwapCtrt instance.
        """
        nc = new_ctrt_with_tok
        api = nc.chain.api

        tok_id = await get_tok_id(api, nc.ctrt_id, 0)
        ac = await pv.AtomicSwapCtrt.register(acnt0, tok_id)

        await cft.wait_for_block()
        assert (await ac.maker) == acnt0.addr.b58_str
        assert (await ac.token_id) == tok_id

        return ac

    async def test_register(self, acnt0: pv.Account) -> pv.NFTCtrt:
        """
        test_register tests the method register.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.NFTCtrt: The registered NFTCtrt.
        """
        nc = await pv.NFTCtrt.register(acnt0)
        await cft.wait_for_block()
        assert (await nc.issuer) == acnt0.addr.b58_str
        assert (await nc.maker) == acnt0.addr.b58_str

        return nc

    async def test_issue(self, new_ctrt: pv.NFTCtrt, acnt0: pv.Account):
        """
        test_issue tests the method issue.

        Args:
            new_ctrt (pv.NFTCtrt): The fixture that registers a new NFT contract.
            acnt0 (pv.Account): The account of nonce 0.
        """
        nc = new_ctrt
        api = nc.chain.api

        resp = await nc.issue(acnt0)
        await cft.wait_for_block()

        await cft.assert_tx_success(api, resp["id"])

        tok_id = await get_tok_id(api, nc.ctrt_id, 0)
        tok_bal = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal == 1

    async def test_send(
        self, new_ctrt_with_tok: pv.NFTCtrt, acnt0: pv.Account, acnt1: pv.Account
    ):
        """
        test_send tests the method send

        Args:
            new_ctrt_with_tok (pv.NFTCtrt): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        nc = new_ctrt_with_tok
        api = nc.chain.api

        tok_id = await get_tok_id(api, nc.ctrt_id, 0)

        tok_bal_acnt0 = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal_acnt0 == 1

        tok_bal_acnt1 = await get_tok_bal(api, acnt1.addr.b58_str, tok_id)
        assert tok_bal_acnt1 == 0

        resp = await nc.send(acnt0, acnt1.addr.b58_str, 0)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        tok_bal_acnt0 = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal_acnt0 == 0

        tok_bal_acnt1 = await get_tok_bal(api, acnt1.addr.b58_str, tok_id)
        assert tok_bal_acnt1 == 1

    async def test_transfer(
        self, new_ctrt_with_tok: pv.NFTCtrt, acnt0: pv.Account, acnt1: pv.Account
    ):
        """
        test_transfer tests the method transfer.

        Args:
            new_ctrt_with_tok (pv.NFTCtrt): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        nc = new_ctrt_with_tok
        api = nc.chain.api

        tok_id = await get_tok_id(api, nc.ctrt_id, 0)

        tok_bal_acnt0 = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal_acnt0 == 1

        tok_bal_acnt1 = await get_tok_bal(api, acnt1.addr.b58_str, tok_id)
        assert tok_bal_acnt1 == 0

        resp = await nc.transfer(acnt0, acnt0.addr.b58_str, acnt1.addr.b58_str, 0)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        tok_bal_acnt0 = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal_acnt0 == 0

        tok_bal_acnt1 = await get_tok_bal(api, acnt1.addr.b58_str, tok_id)
        assert tok_bal_acnt1 == 1

    async def test_deposit_withdraw(
        self,
        new_ctrt_with_tok: pv.NFTCtrt,
        new_atomic_swap_ctrt: pv.AtomicSwapCtrt,
        acnt0: pv.Account,
    ):
        """
        test_deposit_withdraw tests the method deposit & withdraw.

        Args:
            new_ctrt_with_tok (pv.NFTCtrt): The fixture that registers a new NFT contract and issues an NFT token right after it.
            new_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract.
            acnt0 (pv.Account): The account of nonce 0.
        """
        nc = new_ctrt_with_tok
        api = nc.chain.api

        tok_id = await get_tok_id(api, nc.ctrt_id, 0)
        ac = new_atomic_swap_ctrt

        tok_bal = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal == 1

        resp = await nc.deposit(acnt0, ac.ctrt_id, 0)
        await cft.wait_for_block()
        tx_info = await api.tx.get_info(resp["id"])
        assert tx_info["status"] == "Success"

        tok_bal = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal == 0

        deposited_tok_bal = await ac.get_tok_bal(acnt0.addr.b58_str)
        assert deposited_tok_bal == 1

        await nc.withdraw(acnt0, ac.ctrt_id, 0)
        await cft.wait_for_block()

        tok_bal = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal == 1

        deposited_tok_bal = await ac.get_tok_bal(acnt0.addr.b58_str)
        assert deposited_tok_bal == 0

    async def test_supersede(
        self, new_ctrt: pv.NFTCtrt, acnt0: pv.Account, acnt1: pv.Account
    ):
        """
        test_supersede tests the method supersede.

        Args:
            new_ctrt (pv.NFTCtrt): The fixture that registers a new NFT contract.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        nc = new_ctrt
        api = nc.chain.api

        assert (await nc.issuer) == acnt0.addr.b58_str

        resp = await nc.supersede(acnt0, acnt1.addr.b58_str)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await nc.issuer) == acnt1.addr.b58_str

    @pytest.mark.whole
    async def test_as_whole(
        self,
        new_ctrt_with_tok: pv.NFTCtrt,
        new_atomic_swap_ctrt: pv.AtomicSwapCtrt,
        acnt0: pv.Account,
        acnt1: pv.Account,
    ):

        """
        test_as_whole tests methods of NFTCtrt as a whole so as to reduce resource consumption.

        Args:
            new_ctrt_with_tok (pv.NFTCtrt): The fixture that registers a new NFT contract and issues an NFT token right after it.
            new_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        nc = await self.test_register(acnt0)
        await self.test_issue(nc, acnt0)

        nc = new_ctrt_with_tok
        ac = new_atomic_swap_ctrt

        await self.test_send(nc, acnt0, acnt1)
        await self.test_transfer(nc, acnt1, acnt0)
        await self.test_deposit_withdraw(nc, ac, acnt0)
        await self.test_supersede(nc, acnt0, acnt1)


class TestNFTCtrtV2Whitelist(TestNFTCtrt):
    """
    TestNFTCtrtV2Whitelist is the collection of functional tests of NFT contract V2 with whitelist.
    """

    @pytest.fixture
    async def new_ctrt(
        self, acnt0: pv.Account, acnt1: pv.Account
    ) -> pv.NFTCtrtV2Whitelist:
        """
        new_ctrt is the fixture that registers a new NFT contract V2 with whitelist.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.

        Returns:
            pv.NFTCtrtV2Whitelist: The NFTCtrtV2Whitelist instance.
        """
        nc = await pv.NFTCtrtV2Whitelist.register(acnt0)
        await cft.wait_for_block()

        await nc.update_list_user(acnt0, acnt0.addr.b58_str, True)
        await nc.update_list_user(acnt0, acnt1.addr.b58_str, True)
        return nc

    @pytest.fixture
    async def new_atomic_swap_ctrt(
        self,
        new_ctrt_with_tok: pv.NFTCtrtV2Whitelist,
        acnt0: pv.Account,
    ) -> pv.AtomicSwapCtrt:
        """
        new_atomic_swap_ctrt is the fixture that registers a new atomic swap contract.

        Args:
            new_ctrt_with_tok (pv.NFTCtrtV2Whitelist): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.AtomicSwapCtrt: The AtomicSwapCtrt instance.
        """
        nc = new_ctrt_with_tok
        api = nc.chain.api

        tok_id = await get_tok_id(api, nc.ctrt_id, 0)
        ac = await pv.AtomicSwapCtrt.register(acnt0, tok_id)

        await cft.wait_for_block()
        assert (await ac.maker) == acnt0.addr.b58_str
        assert (await ac.token_id) == tok_id

        resp = await nc.update_list_ctrt(acnt0, ac.ctrt_id, True)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        return ac

    @pytest.fixture
    def arbitrary_ctrt_id(self) -> str:
        """
        arbitrary_ctrt_id is the fixture that returns an arbitrary contract ID

        Returns:
            str: The contract ID.
        """
        return "CF5Zkj2Ycx72WrBnjrcNHvJRVwsbNX1tjgT"

    async def test_supersede(
        self, new_ctrt: pv.NFTCtrtV2Whitelist, acnt0: pv.Account, acnt1: pv.Account
    ):
        """
        test_supersede tests the method supersede.

        Args:
            new_ctrt (pv.NFTCtrtV2Whitelist): The fixture that registers a new NFT contract V2 with whitelist.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """

        nc = new_ctrt
        api = nc.chain.api

        assert (await nc.issuer) == acnt0.addr.b58_str
        assert (await nc.regulator) == acnt0.addr.b58_str

        resp = await nc.supersede(acnt0, acnt1.addr.b58_str, acnt1.addr.b58_str)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await nc.issuer) == acnt1.addr.b58_str
        assert (await nc.regulator) == acnt1.addr.b58_str

    async def test_update_list_user(
        self, new_ctrt: pv.NFTCtrtV2Whitelist, acnt0: pv.Account, acnt1: pv.Account
    ):
        """
        test_update_list_user tests the method update_list_user.

        Args:
            new_ctrt (pv.NFTCtrtV2Whitelist): The fixture that registers a new NFT contract V2 with whitelist.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """

        nc = new_ctrt
        api = nc.chain.api

        in_list = await nc.is_user_in_list(acnt1.addr.b58_str)
        assert in_list == False

        resp = await nc.update_list_user(
            by=acnt0,
            addr=acnt1.addr.b58_str,
            val=True,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        in_list = await nc.is_user_in_list(acnt1.addr.b58_str)
        assert in_list == True

        resp = await nc.update_list_user(
            by=acnt0,
            addr=acnt1.addr.b58_str,
            val=False,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        in_list = await nc.is_user_in_list(acnt1.addr.b58_str)
        assert in_list == False

    async def test_update_list_ctrt(
        self, new_ctrt: pv.NFTCtrtV2Whitelist, acnt0: pv.Account, arbitrary_ctrt_id: str
    ):
        """
        test_update_list_ctrt tests the method update_list_ctrt.

        Args:
            new_ctrt (pv.NFTCtrtV2Whitelist): The fixture that registers a new NFT contract V2 with whitelist.
            acnt0 (pv.Account): The account of nonce 0.
            arbitrary_ctrt_id (str): An arbitrary contract ID
        """
        nc = new_ctrt
        api = nc.chain.api
        target_ctrt_id = arbitrary_ctrt_id

        in_list = await nc.is_ctrt_in_list(target_ctrt_id)
        assert in_list == False

        resp = await nc.update_list_ctrt(
            by=acnt0,
            addr=target_ctrt_id,
            val=True,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        in_list = await nc.is_ctrt_in_list(target_ctrt_id)
        assert in_list == True

        resp = await nc.update_list_ctrt(
            by=acnt0,
            addr=target_ctrt_id,
            val=False,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        in_list = await nc.is_ctrt_in_list(target_ctrt_id)
        assert in_list == False

    async def test_register(self, acnt0: pv.Account) -> pv.NFTCtrtV2Whitelist:
        """
        test_register tests the method register.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.NFTCtrtV2Whitelist: The registered NFTCtrtV2Whitelist
        """
        nc: pv.NFTCtrtV2Whitelist = await pv.NFTCtrtV2Whitelist.register(acnt0)
        await cft.wait_for_block()
        assert (await nc.issuer) == acnt0.addr.b58_str
        assert (await nc.maker) == acnt0.addr.b58_str
        assert (await nc.regulator) == acnt0.addr.b58_str

        return nc

    @pytest.mark.whole
    async def test_as_whole(
        self,
        new_ctrt_with_tok: pv.NFTCtrtV2Whitelist,
        new_atomic_swap_ctrt: pv.AtomicSwapCtrt,
        acnt0: pv.Account,
        acnt1: pv.Account,
        arbitrary_ctrt_id: str,
    ):
        """
        test_as_whole tests method of NFTCtrtV2Whitelist as a whole so as to reduce resource consumption.

        Args:
            new_ctrt_with_tok (pv.NFTCtrtV2Whitelist): The fixture that registers a new NFT contract and issues an NFT token right after it.
            new_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
            arbitrary_ctrt_id (str): An arbitrary contract ID
        """
        nc = await self.test_register(acnt0)
        await self.test_update_list_user(nc, acnt0, acnt1)
        await self.test_update_list_ctrt(nc, acnt0, arbitrary_ctrt_id)

        await self.test_issue(nc, acnt0)

        nc = new_ctrt_with_tok
        ac = new_atomic_swap_ctrt

        await self.test_send(nc, acnt0, acnt1)
        await self.test_transfer(nc, acnt1, acnt0)

        await self.test_deposit_withdraw(nc, ac, acnt0)
        await self.test_supersede(nc, acnt0, acnt1)


class TestNFTCtrtV2Blacklist(TestNFTCtrtV2Whitelist):
    """
    TestNFTCtrtV2Blacklist is the collection of functional tests of NFT contract V2 with blacklist.
    """

    @pytest.fixture
    async def new_ctrt(self, acnt0: pv.Account) -> pv.NFTCtrtV2Blacklist:
        """
        new_ctrt is the fixture that registers a new NFT contract V2 with blacklist.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.

        Returns:
            pv.NFTCtrtV2Blacklist: The NFTCtrtV2Blacklist instance.
        """
        nc = await pv.NFTCtrtV2Blacklist.register(acnt0)
        await cft.wait_for_block()

        return nc

    @pytest.fixture
    async def new_atomic_swap_ctrt(
        self,
        new_ctrt_with_tok: pv.NFTCtrtV2Blacklist,
        acnt0: pv.Account,
    ) -> pv.AtomicSwapCtrt:
        """
        new_atomic_swap_ctrt is the fixture that registers a new atomic swap contract.

        Args:
            new_ctrt_with_tok (pv.NFTCtrtV2Blacklist): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.AtomicSwapCtrt: The AtomicSwapCtrt instance.
        """
        nc = new_ctrt_with_tok
        api = nc.chain.api

        tok_id = await get_tok_id(api, nc.ctrt_id, 0)
        ac = await pv.AtomicSwapCtrt.register(acnt0, tok_id)

        await cft.wait_for_block()
        assert (await ac.maker) == acnt0.addr.b58_str
        assert (await ac.token_id) == tok_id

        return ac


class TestVSwapCtrt:
    """
    TestVSwapCtrt is the collection of functional tests of V Swap contract.
    """

    TOK_MAX = 1_000_000_000
    HALF_TOK_MAX = TOK_MAX // 2
    TOK_UNIT = 1_000
    MIN_LIQ = 10
    INIT_AMOUNT = 10_000

    async def new_tok_ctrt(self, acnt0: pv.Account) -> pv.TokenCtrtWithoutSplit:
        """
        new_tok_ctrt is the fixture that registers a new token contract without split
        to be used in a V Swap contract.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.TokenCtrtWithoutSplit: The TokenCtrtWithoutSplit instance.
        """
        api = acnt0.api

        tc = await pv.TokenCtrtWithoutSplit.register(
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
            tca.send(acnt0, acnt1.addr.b58_str, self.HALF_TOK_MAX),
            tcb.send(acnt0, acnt1.addr.b58_str, self.HALF_TOK_MAX),
        )

        await cft.wait_for_block()

        tok_a_id, tok_b_id, liq_tok_id = await asyncio.gather(
            tca.tok_id,
            tcb.tok_id,
            tcl.tok_id,
        )

        vc = await pv.VSwapCtrt.register(
            by=acnt0,
            tok_a_id=tok_a_id,
            tok_b_id=tok_b_id,
            liq_tok_id=liq_tok_id,
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

        assert (await vc.maker) == acnt0.addr.b58_str

        resp = await vc.supersede(acnt0, acnt1.addr.b58_str)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await vc.maker) == acnt1.addr.b58_str

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

        assert tok_a_reserved == tok_a_reserved_old + DELTA * self.TOK_UNIT
        assert tok_b_reserved == tok_b_reserved_old + DELTA * self.TOK_UNIT
        assert liq_tok_left == liq_tok_left_old - DELTA * self.TOK_UNIT

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

        assert liq_tok_left == liq_tok_left_old + DELTA * self.TOK_UNIT

        tok_a_redeemed = tok_a_reserved_old - tok_a_reserved
        tok_b_redeemed = tok_b_reserved_old - tok_b_reserved

        assert tok_a_redeemed >= DELTA * self.TOK_UNIT
        assert tok_b_redeemed >= DELTA * self.TOK_UNIT

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
            vc.get_tok_a_bal(acnt1.addr.b58_str),
            vc.get_tok_b_bal(acnt1.addr.b58_str),
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
            vc.get_tok_a_bal(acnt1.addr.b58_str),
            vc.get_tok_b_bal(acnt1.addr.b58_str),
        )

        assert bal_a == bal_a_old + amount_a * self.TOK_UNIT
        assert bal_b_old - bal_b <= amount_b_max * self.TOK_UNIT

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
            vc.get_tok_a_bal(acnt1.addr.b58_str),
            vc.get_tok_b_bal(acnt1.addr.b58_str),
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
            vc.get_tok_a_bal(acnt1.addr.b58_str),
            vc.get_tok_b_bal(acnt1.addr.b58_str),
        )

        assert bal_a - bal_a_old >= amount_a_min
        assert bal_b == bal_b_old - amount_b * self.TOK_UNIT

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
            vc.get_tok_a_bal(acnt1.addr.b58_str),
            vc.get_tok_b_bal(acnt1.addr.b58_str),
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
            vc.get_tok_a_bal(acnt1.addr.b58_str),
            vc.get_tok_b_bal(acnt1.addr.b58_str),
        )

        assert bal_a_old - bal_a <= amount_a_max * self.TOK_UNIT
        assert bal_b == bal_b_old + amount_b * self.TOK_UNIT

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
            vc.get_tok_a_bal(acnt1.addr.b58_str),
            vc.get_tok_b_bal(acnt1.addr.b58_str),
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
            vc.get_tok_a_bal(acnt1.addr.b58_str),
            vc.get_tok_b_bal(acnt1.addr.b58_str),
        )

        assert bal_a == bal_a_old - amount_a * self.TOK_UNIT
        assert bal_b - bal_b_old >= amount_b_min

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
            new_ctrt (pv.NFTCtrt): The fixture that registers a new TokenWithoutSplit contract.
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
            new_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.AtomicSwapCtrt: The AtomicSwapCtrt instance.
        """
        tc = new_ctrt_with_tok
        api = tc.chain.api

        tok_id = await get_tok_id(api, tc.ctrt_id, 0)
        ac = await pv.AtomicSwapCtrt.register(acnt0, tok_id)

        await cft.wait_for_block()
        assert (await ac.maker) == acnt0.addr.b58_str
        assert (await ac.token_id) == tok_id

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
        assert (await tc.issuer) == acnt0.addr.b58_str
        assert (await tc.maker) == acnt0.addr.b58_str

        return tc

    async def test_issue(self, new_ctrt: pv.TokenCtrtWithoutSplit, acnt0: pv.Account):
        """
        test_issue tests the method issue.

        Args:
            new_ctrt (pv.TokenCtrtWithoutSplit): [description]
            acnt0 (pv.Account): The account of nonce 0.
        """
        tc = new_ctrt
        api = tc.chain.api

        resp = await tc.issue(acnt0, 50)
        await cft.wait_for_block()

        await cft.assert_tx_success(api, resp["id"])

        tok_id = await get_tok_id(api, tc.ctrt_id, 0)
        tok_bal = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
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
            new_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        tc = new_ctrt_with_tok
        api = tc.chain.api

        tok_id = await get_tok_id(api, tc.ctrt_id, 0)

        tok_bal_acnt0 = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal_acnt0 == 50

        tok_bal_acnt1 = await get_tok_bal(api, acnt1.addr.b58_str, tok_id)
        assert tok_bal_acnt1 == 0

        resp = await tc.transfer(acnt0, acnt0.addr.b58_str, acnt1.addr.b58_str, 50)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        tok_bal_acnt0 = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal_acnt0 == 0

        tok_bal_acnt1 = await get_tok_bal(api, acnt1.addr.b58_str, tok_id)
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
            new_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        tc = new_ctrt_with_tok
        api = tc.chain.api

        tok_id = await get_tok_id(api, tc.ctrt_id, 0)

        tok_bal_acnt0 = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal_acnt0 == 50

        tok_bal_acnt1 = await get_tok_bal(api, acnt1.addr.b58_str, tok_id)
        assert tok_bal_acnt1 == 0

        resp = await tc.transfer(acnt0, acnt0.addr.b58_str, acnt1.addr.b58_str, 50)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        tok_bal_acnt0 = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal_acnt0 == 0

        tok_bal_acnt1 = await get_tok_bal(api, acnt1.addr.b58_str, tok_id)
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
            new_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new NFT contract and issues an NFT token right after it.
            new_atomic_swap_ctrt (pv.AtomicSwapCtrt): The fixture that registers a new atomic swap contract.
            acnt0 (pv.Account): The account of nonce 0.
        """
        tc = new_ctrt_with_tok
        api = tc.chain.api

        tok_id = await get_tok_id(api, tc.ctrt_id, 0)
        ac = new_atomic_swap_ctrt
        await cft.wait_for_block()
        assert (await ac.maker) == acnt0.addr.b58_str
        assert (await ac.token_id) == tok_id

        tok_bal = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal == 50

        resp = await tc.deposit(acnt0, ac.ctrt_id, 10)
        await cft.wait_for_block()
        tx_info = await api.tx.get_info(resp["id"])
        assert tx_info["status"] == "Success"

        tok_bal = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal == 40

        deposited_tok_bal = await ac.get_tok_bal(acnt0.addr.b58_str)
        assert deposited_tok_bal == 10

        # withdraw
        await tc.withdraw(acnt0, ac.ctrt_id, 10)
        await cft.wait_for_block()

        tok_bal = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal == 50

        deposited_tok_bal = await ac.get_tok_bal(acnt0.addr.b58_str)
        assert deposited_tok_bal == 0

    async def test_destroy(
        self, new_ctrt_with_tok: pv.TokenCtrtWithoutSplit, acnt0: pv.Account
    ):
        """
        test_destroy tests the method destroy.
        Args:
            new_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new NFT contract and issues an NFT token right after it.
        """
        tc = new_ctrt_with_tok
        api = tc.chain.api

        tok_id = await get_tok_id(api, tc.ctrt_id, 0)

        tok_bal = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal == 50

        resp = await tc.destroy(acnt0, 10)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        tok_bal_acnt0 = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
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

        assert (await tc.issuer) == acnt0.addr.b58_str

        resp = await tc.supersede(acnt0, acnt1.addr.b58_str)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await tc.issuer) == acnt1.addr.b58_str

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
            new_ctrt_with_tok (pv.TokenCtrtWithoutSplit): The fixture that registers a new NFT contract and issues an NFT token right after it.
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
        tc_ctrt_id = tc.ctrt_id

        tok_id_dict = await api.ctrt.get_tok_id(tc_ctrt_id, 0)
        tok_id = tok_id_dict["tokenId"]

        resp = await tc.split(acnt0, 12)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        new_unit = await api.ctrt.get_tok_info(tok_id)

        assert 12 == new_unit["unity"]
