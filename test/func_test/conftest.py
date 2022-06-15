import asyncio
import os
from typing import Optional

import pytest

import py_vsys as pv

HOST = os.getenv("PY_SDK_HOST")
API_KEY = os.getenv("PY_SDK_API_KEY", "")
SEED = os.getenv("PY_SDK_SEED")
SUPERNODE_ADDR = os.getenv("PY_SDK_SUPERNODE_ADDR")
AVG_BLOCK_DELAY = int(os.getenv("PY_SDK_AVG_BLOCK_DELAY", "6"))  # in seconds


@pytest.fixture
def host() -> str:
    return HOST


@pytest.fixture
def api_key() -> Optional[str]:
    return API_KEY or None


@pytest.fixture
async def api(host: str, api_key: str) -> pv.NodeAPI:
    a = await pv.NodeAPI.new(host, api_key)
    yield a
    await a.sess.close()


@pytest.fixture
def chain(api: pv.NodeAPI) -> pv.Chain:
    return pv.Chain(api, pv.ChainID.TEST_NET)


@pytest.fixture
def seed() -> pv.Seed:
    return pv.Seed(SEED)


@pytest.fixture
def wallet(seed: pv.Seed) -> pv.Wallet:
    return pv.Wallet(seed)


@pytest.fixture
def acnt0(chain: pv.Chain, wallet: pv.Wallet) -> pv.Account:
    """
    acnt0 is the fixture that returns the account of nonce 0.

    Args:
        chain (pv.Chain): The Chain object.
        wallet (pv.Wallet): The wallet object.

    Returns:
        pv.Account: The account.
    """
    return wallet.get_account(chain, 0)


@pytest.fixture
def acnt1(chain: pv.Chain, wallet: pv.Wallet) -> pv.Account:
    """
    acnt1 is the fixture that returns the account of nonce 1.

    Args:
        chain (pv.Chain): The Chain object.
        wallet (pv.Wallet): The wallet object.

    Returns:
        pv.Account: The account.
    """
    return wallet.get_account(chain, 1)


@pytest.fixture
def acnt2(chain: pv.Chain, wallet: pv.Wallet) -> pv.Account:
    """
    acnt2 is the fixture that returns the account of nonce 2.

    Args:
        chain (pv.Chain): The Chain object.
        wallet (pv.Wallet): The wallet object.

    Returns:
        pv.Account: The account.
    """
    return wallet.get_account(chain, 2)


async def wait_for_block() -> None:
    """
    wait_for_block waits for the transaction to be packed into a block.
    """
    await asyncio.sleep(AVG_BLOCK_DELAY)


async def assert_tx_status(api: pv.NodeAPI, tx_id: str, status: str) -> None:
    """
    assert_tx_status asserts the status of the transaction of the given
    ID matches the given status.

    Args:
        api (pv.NodeAPI): The NodeAPI object.
        tx_id (str): The transaction ID.
    """
    resp = await api.tx.get_info(tx_id)
    assert resp["status"] == status


async def assert_tx_success(api: pv.NodeAPI, tx_id: str) -> None:
    """
    assert_tx_success asserts the status of the transaction of the given
    ID is success.

    Args:
        api (pv.NodeAPI): The NodeAPI object.
        tx_id (str): The transaction ID.
    """
    await assert_tx_status(api, tx_id, "Success")


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
