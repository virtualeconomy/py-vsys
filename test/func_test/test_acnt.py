"""
test_acnt contains functional tests for Account.
"""

import uuid
import pytest

import py_vsys as pv
from . import conftest as cft


class TestAccount:
    """
    TestAccount is the collection of functional tests of Account.
    """

    pri_key = "EV5stVcWZ1kEQhrS7qcfYQdHpMHM5jwkyRxi9n9kXteZ";
    pub_key = "4EyuJtDzQH15qAfnTPgqa8QB4ZU1dzqihdCs13UYEiV4";
    addr = "ATuQXbkZV4dCKsoFtXSCH5eKw92dMXQdUYU";

    @pytest.fixture
    def supernode_addr(self) -> str:
        """
        supernode_addr returns the address of a supernode.

        Returns:
            str: The address.
        """
        return cft.SUPERNODE_ADDR

    def test_pri_str_cons(self, chain: pv.Chain):
        """
        test_pri_str_cons tests method from_pri_key_str.

        Args:
            chain (pv.Chain): The chain.
        """

        acnt = pv.Account.from_pri_key_str(chain, self.pri_key)

        assert acnt.key_pair.pri.data == self.pri_key
        assert acnt.key_pair.pub.data == self.pub_key
        assert acnt.addr.data == self.addr

    def test_pri_pub_cons(self, chain: pv.Chain):
        """
        test_pri_pub_cons tests class Account constructor.

        Args:
            chain (pv.Chain): The chain.
        """

        acnt = pv.Account(chain, pv.PriKey(self.pri_key), pv.PubKey(self.pub_key))

        assert acnt.key_pair.pri.data == self.pri_key
        assert acnt.key_pair.pub.data == self.pub_key
        assert acnt.addr.data == self.addr

    def test_key_match(self, chain: pv.Chain):
        """
        test_key_match tests the class KeyPair method validate.

        Args:
            chain (pv.Chain): The chain.
        """
        wrong_pub_key = "4EyuJtDzQH15qAfnTPgqa8QB4ZU1dzqihdCs13U12345"

        try:
            acnt = pv.Account(chain, pv.PriKey(self.pri_key), pv.PubKey(wrong_pub_key))
            assert False
        except ValueError as e:
            print(e.args)
            if e.args[0] == "Public key & private key do not match.":
                assert True
            else:
                assert False

    async def test_pay(self, acnt0: pv.Account, acnt1: pv.Account) -> None:
        """
        test_pay tests the method pay.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.
        """
        api = acnt0.api

        acnt0_bal_old = (await acnt0.bal).data
        acnt1_bal_old = (await acnt1.bal).data

        amount = pv.VSYS.for_amount(5)
        resp = await acnt0.pay(acnt1.addr.data, amount.amount)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        acnt0_bal = (await acnt0.bal).data
        acnt1_bal = (await acnt1.bal).data

        assert acnt0_bal == acnt0_bal_old - amount.data - pv.PaymentFee.DEFAULT
        assert acnt1_bal == acnt1_bal_old + amount.data

    async def test_lease_and_cancel_lease(
        self, acnt0: pv.Account, supernode_addr: str
    ) -> None:
        """
        test_lease_and_cancel_lease tests methods
            - lease
            - cancel_lease

        Args:
            acnt0 (pv.Account): The account of nonce 0.
            supernode_addr (str): The supernode address.
        """
        api = acnt0.api

        eff_bal_init = (await acnt0.eff_bal).data

        amount = pv.VSYS.for_amount(5)
        resp = await acnt0.lease(supernode_addr, amount.amount)
        await cft.wait_for_block()

        leasing_tx_id = resp["id"]
        await cft.assert_tx_success(api, leasing_tx_id)

        eff_bal_lease = (await acnt0.eff_bal).data
        assert eff_bal_lease == eff_bal_init - amount.data - pv.LeasingFee.DEFAULT

        resp = await acnt0.cancel_lease(leasing_tx_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        eff_bal_cancel = (await acnt0.eff_bal).data
        assert (
            eff_bal_cancel == eff_bal_lease + amount.data - pv.LeasingCancelFee.DEFAULT
        )

    async def test_db_put(self, acnt0: pv.Account) -> None:
        """
        test_db_put tests the method db_put.

        Args:
            acnt0 (pv.Account): The account of nonce 0.
        """
        api = acnt0.api

        db_key = "func_test"
        data = str(uuid.uuid4())

        resp = await acnt0.db_put(db_key, data)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        resp = await api.db.get(acnt0.addr.data, db_key)
        assert resp["data"] == data
