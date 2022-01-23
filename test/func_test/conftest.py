import pytest

import py_v_sdk as pv

HOST = ""
API_KEY = ""
SEED = ""


@pytest.fixture
def host() -> str:
    return HOST


@pytest.fixture
def api_key() -> str | None:
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
def seed() -> str:
    return SEED
