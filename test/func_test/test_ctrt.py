"""
test_ctrt contains functional tests for smart contracts.
"""
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
    resp = await api.ctrt.get_tok_balance(addr, tok_id)
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

    async def test_register(self, acnt0: pv.Account):
        """
        test_register tests the method register.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
        """
        nc = await pv.NFTCtrt.register(acnt0)
        await cft.wait_for_block()
        assert (await nc.issuer) == acnt0.addr.b58_str
        assert (await nc.maker) == acnt0.addr.b58_str

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

    async def test_deposit(self, new_ctrt_with_tok: pv.NFTCtrt, acnt0: pv.Account):
        """
        test_deposit tests the method deposit.

        Args:
            new_ctrt_with_tok (pv.NFTCtrt): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.
        """
        nc = new_ctrt_with_tok
        api = nc.chain.api

        tok_id = await get_tok_id(api, nc.ctrt_id, 0)
        ac = await pv.AtomicSwapCtrt.register(acnt0, tok_id)
        await cft.wait_for_block()
        assert (await ac.maker) == acnt0.addr.b58_str
        assert (await ac.token_id) == tok_id

        tok_bal = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal == 1

        resp = await nc.deposit(acnt0, ac.ctrt_id, 0)
        await cft.wait_for_block()
        tx_info = await api.tx.get_info(resp["id"])
        assert tx_info["status"] == "Success"

        tok_bal = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal == 0

        deposited_tok_bal = await ac.get_token_balance(acnt0.addr.b58_str)
        assert deposited_tok_bal == 1

    async def test_withdraw(self, new_ctrt_with_tok: pv.NFTCtrt, acnt0: pv.Account):
        """
        test_withdraw tests the method withdraw.

        Args:
            new_ctrt_with_tok (pv.NFTCtrt): The fixture that registers a new NFT contract and issues an NFT token right after it.
            acnt0 (pv.Account): The account of nonce 0.
        """
        nc = new_ctrt_with_tok
        api = nc.chain.api

        tok_id = await get_tok_id(api, nc.ctrt_id, 0)
        ac = await pv.AtomicSwapCtrt.register(acnt0, tok_id)
        await cft.wait_for_block()
        assert (await ac.maker) == acnt0.addr.b58_str
        assert (await ac.token_id) == tok_id

        await nc.deposit(acnt0, ac.ctrt_id, 0)
        await cft.wait_for_block()

        tok_bal = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal == 0

        deposited_tok_bal = await ac.get_token_balance(acnt0.addr.b58_str)
        assert deposited_tok_bal == 1

        await nc.withdraw(acnt0, ac.ctrt_id, 0)
        await cft.wait_for_block()

        tok_bal = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal == 1

        deposited_tok_bal = await ac.get_token_balance(acnt0.addr.b58_str)
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
    async def test_as_whole(self, acnt0: pv.Account, acnt1: pv.Account):
        """
        test_as_whole tests methods of NFTCtrt as a whole so as to reduce resource consumption.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        api = acnt0.api

        # test register
        nc = await pv.NFTCtrt.register(acnt0)
        await cft.wait_for_block()
        assert (await nc.issuer) == acnt0.addr.b58_str
        assert (await nc.maker) == acnt0.addr.b58_str

        # test issue
        resp = await nc.issue(acnt0)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])
        tok_id = await get_tok_id(api, nc.ctrt_id, 0)
        tok_bal = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal == 1

        # test send
        resp = await nc.send(acnt0, acnt1.addr.b58_str, 0)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])
        tok_bal_acnt0 = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal_acnt0 == 0
        tok_bal_acnt1 = await get_tok_bal(api, acnt1.addr.b58_str, tok_id)
        assert tok_bal_acnt1 == 1

        # test transfer
        resp = await nc.transfer(acnt1, acnt1.addr.b58_str, acnt0.addr.b58_str, 0)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])
        tok_bal_acnt0 = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal_acnt0 == 1
        tok_bal_acnt1 = await get_tok_bal(api, acnt1.addr.b58_str, tok_id)
        assert tok_bal_acnt1 == 0

        # create atomic swap contract instance for testing deposit & withdraw
        ac = await pv.AtomicSwapCtrt.register(acnt0, tok_id)
        await cft.wait_for_block()
        assert (await ac.maker) == acnt0.addr.b58_str
        assert (await ac.token_id) == tok_id

        # test deposit
        tok_bal_acnt0 = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal_acnt0 == 1
        await nc.deposit(acnt0, ac.ctrt_id, 0)
        await cft.wait_for_block()
        tok_bal_acnt0 = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal_acnt0 == 0
        deposited_tok_bal = await ac.get_token_balance(acnt0.addr.b58_str)
        assert deposited_tok_bal == 1

        # test withdraw
        resp = await nc.withdraw(acnt0, ac.ctrt_id, 0)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])
        tok_bal_acnt0 = await get_tok_bal(api, acnt0.addr.b58_str, tok_id)
        assert tok_bal_acnt0 == 1
        deposited_tok_bal = await ac.get_token_balance(acnt0.addr.b58_str)
        assert deposited_tok_bal == 0

        # test supersede
        assert (await nc.issuer) == acnt0.addr.b58_str
        resp = await nc.supersede(acnt0, acnt1.addr.b58_str)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])
        assert (await nc.issuer) == acnt1.addr.b58_str
