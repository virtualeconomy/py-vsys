"""
test_api contains functional tests for py_v_sdk/api.py
"""
import aiohttp
import pytest

import py_v_sdk as pv


class TestAPIGrp:
    """
    TestAPIGrp tests pv.APIGrp
    """

    class MockAPIGrp(pv.APIGrp):
        """
        MockAPIGrp is the test subclass of pv.APIGrp
        """

        PREFIX = "TEST"

    @pytest.mark.asyncio
    async def test_make_url(self, host: str):
        """
        test_make_url tests pv.APIGrp._make_url
        """
        sess = aiohttp.ClientSession(base_url=host)
        obj = self.MockAPIGrp(sess)
        edpt = "EDPT"
        assert obj._make_url(edpt) == self.MockAPIGrp.PREFIX + edpt

    @pytest.mark.asyncio
    async def test_get(self, host: str):
        """
        test_get tests pv.APIGrp._get
        """
        self.MockAPIGrp.PREFIX = "/blocks"

        sess = aiohttp.ClientSession(base_url=host)
        edpt = "/height"

        resp = await self.MockAPIGrp(sess)._get(edpt)
        assert resp["height"] > 0

    @pytest.mark.asyncio
    async def test_post(self, host: str):
        """
        test_post tests pv.APIGrp._post
        """
        self.MockAPIGrp.PREFIX = "/utils"

        sess = aiohttp.ClientSession(base_url=host)
        edpt = "/hash/fast"

        raw = "hello"
        resp = await self.MockAPIGrp(sess)._post(edpt, raw)
        assert resp["hash"] == "4PNCZERNLKAqwSYHhZpb7B4GE34eiYDPXGgeNKWNNaBp"
