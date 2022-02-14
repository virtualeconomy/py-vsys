import pytest

import py_v_sdk as pv
from test.func_test import conftest as cft


class TestSysCtrt:
    """
    TestSysCtrt is the collection of functional tests of System contract.
    """

    @pytest.fixture
    def new_ctrt(self, acnt0: pv.Account) -> pv.SysCtrt:
        """
        new_ctrt is the fixture that creates a representative object for the System contract.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.SysCtrt: The System contract instance.
        """
        return pv.SysCtrt.for_testnet(acnt0.chain)

    async def test_send(
        self,
        new_ctrt: pv.SysCtrt,
        acnt0: pv.Account,
        acnt1: pv.Account,
    ):
        """
        test_send tests the method send.

        Args:
            new_ctrt (pv.SysCtrt): The fixture that creates a representative object for the System contract.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        sc = new_ctrt
        api = acnt0.api
        amount = 1

        acnt0_bal_old = await acnt0.balance
        acnt1_bal_old = await acnt1.balance

        resp = await sc.send(acnt0, acnt1.addr.b58_str, amount)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        acnt0_bal = await acnt0.balance
        acnt1_bal = await acnt1.balance

        assert (
            acnt0_bal_old - acnt0_bal
            == pv.VSYS.for_amount(amount).data + pv.ExecCtrtFee.DEFAULT
        )
        assert acnt1_bal == acnt1_bal_old + pv.VSYS.for_amount(amount).data

    async def test_transfer(
        self,
        new_ctrt: pv.SysCtrt,
        acnt0: pv.Account,
        acnt1: pv.Account,
    ):
        """
        test_transfer tests the method transfer.

        Args:
            new_ctrt (pv.SysCtrt): The fixture that creates a representative object for the System contract.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        sc = new_ctrt
        api = acnt0.api
        amount = 1

        acnt0_bal_old = await acnt0.balance
        acnt1_bal_old = await acnt1.balance

        resp = await sc.transfer(acnt0, acnt0.addr.b58_str, acnt1.addr.b58_str, amount)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        acnt0_bal = await acnt0.balance
        acnt1_bal = await acnt1.balance

        assert (
            acnt0_bal_old - acnt0_bal
            == pv.VSYS.for_amount(amount).data + pv.ExecCtrtFee.DEFAULT
        )
        assert acnt1_bal == acnt1_bal_old + pv.VSYS.for_amount(amount).data

    @pytest.mark.whole
    async def test_as_whole(
        self,
        new_ctrt: pv.SysCtrt,
        acnt0: pv.Account,
        acnt1: pv.Account,
    ):
        """
        test_as_whole tests methods of SysCtrt as a whole.
        As registering is not required for SysCtrt, the main purpose of having this test
        is to be compatible with test cases of other contracts.

        Args:
            new_ctrt (pv.SysCtrt): The fixture that creates a representative object for the System contract.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        sc = new_ctrt
        await self.test_send(sc, acnt0, acnt1)
        await self.test_transfer(sc, acnt1, acnt0)
