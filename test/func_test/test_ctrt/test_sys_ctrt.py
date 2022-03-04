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

    @pytest.fixture
    async def new_pay_chan_ctrt(
        self,
        acnt0: pv.Account,
        new_ctrt: pv.SysCtrt,
    ) -> pv.PayChanCtrt:
        """
        new_pay_chan_ctrt is the fixture that creates a representative object for the
        Payment Channel contract.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_ctrt (pv.SysCtrt): The system contract.

        Returns:
            pv.PayChanCtrt: The Payment Channel contract instance.
        """
        sc = new_ctrt
        pc = await pv.PayChanCtrt.register(acnt0, sc.tok_id.data)
        await cft.wait_for_block()
        return pc

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

        acnt0_bal_old = (await acnt0.bal).data
        acnt1_bal_old = (await acnt1.bal).data

        resp = await sc.send(acnt0, acnt1.addr.data, amount)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        acnt0_bal = (await acnt0.bal).data
        acnt1_bal = (await acnt1.bal).data

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

        acnt0_bal_old = (await acnt0.bal).data
        acnt1_bal_old = (await acnt1.bal).data

        resp = await sc.transfer(acnt0, acnt0.addr.data, acnt1.addr.data, amount)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        acnt0_bal = (await acnt0.bal).data
        acnt1_bal = (await acnt1.bal).data

        assert (
            acnt0_bal_old - acnt0_bal
            == pv.VSYS.for_amount(amount).data + pv.ExecCtrtFee.DEFAULT
        )
        assert acnt1_bal == acnt1_bal_old + pv.VSYS.for_amount(amount).data

    async def test_deposit_and_withdraw(
        self,
        acnt0: pv.Account,
        new_ctrt: pv.SysCtrt,
        new_pay_chan_ctrt: pv.PayChanCtrt,
    ) -> None:
        """
        test_deposit_and_withdraw tests methods
            - deposit
            - withdraw

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            new_ctrt (pv.SysCtrt): The fixture that creates a representative object for the System contract.
            new_pay_chan_ctrt (pv.PayChanCtrt): The fixture that creates a representative object for the Payment Channel contract.
        """
        api = acnt0.api
        sc = new_ctrt
        pc = new_pay_chan_ctrt
        deposit_amount = 1

        bal_init = (await acnt0.bal).data

        resp = await sc.deposit(acnt0, pc.ctrt_id, deposit_amount)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        bal_after_deposit = (await acnt0.bal).data
        assert (
            bal_after_deposit
            == bal_init
            - pv.VSYS.for_amount(deposit_amount).data
            - pv.ExecCtrtFee.DEFAULT
        )

        resp = await sc.withdraw(acnt0, pc.ctrt_id, deposit_amount)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        bal_after_withdraw = (await acnt0.bal).data
        assert (
            bal_after_withdraw
            == bal_after_deposit
            + pv.VSYS.for_amount(deposit_amount).data
            - pv.ExecCtrtFee.DEFAULT
        )

    @pytest.mark.whole
    async def test_as_whole(
        self,
        new_ctrt: pv.SysCtrt,
        new_pay_chan_ctrt: pv.PayChanCtrt,
        acnt0: pv.Account,
        acnt1: pv.Account,
    ):
        """
        test_as_whole tests methods of SysCtrt as a whole.
        As registering is not required for SysCtrt, the main purpose of having this test
        is to be compatible with test cases of other contracts.

        Args:
            new_ctrt (pv.SysCtrt): The fixture that creates a representative object for the System contract.
            new_pay_chan_ctrt (pv.PayChanCtrt): The fixture that creates a representative object for the Payment Channel contract.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        sc = new_ctrt
        await self.test_send(sc, acnt0, acnt1)
        await self.test_transfer(sc, acnt1, acnt0)

        pc = new_pay_chan_ctrt
        await self.test_deposit_and_withdraw(acnt0, sc, pc)
