import pytest

HOST = "http://veldidina.vos.systems:9928"
API_KEY = ""


@pytest.fixture
def host() -> str:
    return HOST


@pytest.fixture
def api_key() -> str:
    return API_KEY
