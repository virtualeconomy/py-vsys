import asyncio
from typing import Optional

import pytest

import py_v_sdk as pv

HOST = ""
API_KEY = ""
SEED = ""
SUPERNODE_ADDR = ""


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
    return pv.Chain(api)


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


async def wait_for_block() -> None:
    """
    wait_for_block waits for the transaction to be packed into a block.
    """
    await asyncio.sleep(6)


async def assert_tx_success(api: pv.NodeAPI, tx_id: str) -> None:
    """
    assert_tx_success asserts the status of the transaction of the given
    ID is success.

    Args:
        api (pv.NodeAPI): The NodeAPI object.
        tx_id (str): The transaction ID.
    """
    resp = await api.tx.get_info(tx_id)
    assert resp["status"] == "Success"
