import pytest

import py_v_sdk as pv
from test.func_test import conftest as cft


class TestVEscrowCtrt:
    """
    TestVEscrowCtrt is the collection of functional tests of V Escrow Contract.
    """

    TOK_MAX = 100
    TOK_UNIT = 1
    INIT_LOAD = TOK_MAX // 2

    @pytest.fixture
    async def new_sys_ctrt(self, chain: pv.Chain) -> pv.SysCtrt:
        """
        new_sys_ctrt is the fixture that returns a system contract instance.

        Args:
            chain (pv.Chain): The chain object.

        Returns:
            pv.SysCtrt: The system contract instance.
        """
        return pv.SysCtrt.for_testnet(chain)

    async def _new_ctrt(
        self,
        new_sys_ctrt: pv.SysCtrt,
        acnt0: pv.Account,
        duration: int,
    ) -> pv.VEscrowCtrt:
        """
        _new_ctrt registers a new V Escrow Contract where the payer duration & judge duration
        are all the given duration.

        Args:
            new_sys_ctrt (pv.SysCtrt): The system contract instance.
            acnt0 (pv.Account): The account of nonce 0.
            duration (int): The duration in seconds.

        Returns:
            pv.VEscrowCtrt: The VEscrowCtrt instance.
        """
        sc = new_sys_ctrt

        vc = await pv.VEscrowCtrt.register(
            by=acnt0,
            tok_id=sc.tok_id,
            duration=duration,
            judge_duration=duration,
        )
        await cft.wait_for_block()
        return vc

    @pytest.fixture
    async def new_ctrt_with_ten_mins_duration(
        self,
        new_sys_ctrt: pv.SysCtrt,
        acnt0: pv.Account,
    ) -> pv.VEscrowCtrt:
        """
        new_ctrt_with_ten_mins_duration is the fixture that registers
        a new V Escrow Contract where the payer duration & judge duration
        are all 10 mins

        Args:
            new_sys_ctrt (pv.SysCtrt): The system contract instance.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.VEscrowCtrt: The VEscrowCtrt instance.
        """
        ten_mins = 10 * 60
        return await self._new_ctrt(
            new_sys_ctrt,
            acnt0,
            ten_mins,
        )

    @pytest.fixture
    async def new_ctrt_with_five_secs_duration(
        self,
        new_sys_ctrt: pv.SysCtrt,
        acnt0: pv.Account,
    ) -> pv.VEscrowCtrt:
        """
        new_ctrt_with_ten_mins_duration is the fixture that registers
        a new V Escrow Contract where the payer duration & judge duration
        are all 5 secs.

        Args:
            new_sys_ctrt (pv.SysCtrt): The system contract instance.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.VEscrowCtrt: The VEscrowCtrt instance.
        """
        five_secs = 5
        return await self._new_ctrt(
            new_sys_ctrt,
            acnt0,
            five_secs,
        )

    async def test_register(
        self,
        new_sys_ctrt: pv.SysCtrt,
        new_ctrt_with_ten_mins_duration: pv.VEscrowCtrt,
        acnt0: pv.Account,
    ) -> pv.VEscrowCtrt:
        """
        test_register tests the method register.

        Args:
            new_sys_ctrt (pv.SysCtrt): The system contract instance.
            new_ctrt_with_ten_mins_duration (pv.VEscrowCtrt): The V Escrow contract instance.
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.VEscrowCtrt: The VEscrowCtrt instance.
        """

        sc = new_sys_ctrt
        vc = new_ctrt_with_ten_mins_duration

        maker = await vc.maker
        assert maker.data == acnt0.addr.b58_str

        judge = await vc.judge
        assert judge.data == acnt0.addr.b58_str

        tok_id = await vc.tok_id
        assert tok_id.data == sc.tok_id

        ten_mins = 10 * 60
        duration = await vc.duration
        assert duration.unix_ts == ten_mins

        judge_duration = await vc.judge_duration
        assert judge_duration.unix_ts == ten_mins

        assert (await vc.unit) == (await sc.unit)

