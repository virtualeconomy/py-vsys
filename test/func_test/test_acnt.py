"""
test_acnt contains functional tests for Account.
"""
import py_v_sdk as pv
from . import conftest as cft


class TestAccount:
    """
    TestAccount is the collection of functional tests of Account.
    """

    async def test_pay(self, acnt0: pv.Account, acnt1: pv.Account):
        api = acnt0.api

        acnt0_bal_old = await acnt0.balance
        acnt1_bal_old = await acnt1.balance

        amount = pv.VSYS.for_amount(5)
        resp = await acnt0.pay(acnt1.addr.b58_str, amount.amount)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        acnt0_bal = await acnt0.balance
        acnt1_bal = await acnt1.balance

        assert acnt0_bal == acnt0_bal_old - amount.data - pv.PaymentFee.DEFAULT
        assert acnt1_bal == acnt1_bal_old + amount.data
