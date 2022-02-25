import asyncio
import time
from typing import Tuple

import pytest

import py_v_sdk as pv
from test.func_test import conftest as cft


class TestVEscrowCtrt:
    """
    TestVEscrowCtrt is the collection of functional tests of V Escrow Contract.
    """

    ORDER_AMOUNT = 10
    RCPT_DEPOSIT_AMOUNT = 2
    JUDGE_DEPOSIT_AMOUNT = 3
    ORDER_FEE = 4
    REFUND_AMOUNT = 5
    CTRT_DEPOSIT_AMOUNT = 30

    @pytest.fixture
    def maker(self, acnt0: pv.Account) -> pv.Account:
        """
        maker is the fixture that returns the maker account used in the tests.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.Account: The account.
        """
        return acnt0

    @pytest.fixture
    def judge(self, acnt0: pv.Account) -> pv.Account:
        """
        judge is the fixture that returns the judge account used in the tests.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.Account: The account.
        """
        return acnt0

    @pytest.fixture
    def payer(self, acnt1: pv.Account) -> pv.Account:
        """
        payer is the fixture that returns the payer account used in the tests.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.Account: The account.
        """
        return acnt1

    @pytest.fixture
    def recipient(self, acnt2: pv.Account) -> pv.Account:
        """
        recipient is the fixture that returns the recipient account used in the tests.

        Args:
            acnt0 (pv.Account): The account of nonce 0.

        Returns:
            pv.Account: The account.
        """
        return acnt2

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
        maker: pv.Account,
        judge: pv.Account,
        payer: pv.Account,
        recipient: pv.Account,
        duration: int,
    ) -> pv.VEscrowCtrt:
        """
        _new_ctrt registers a new V Escrow Contract where the payer duration & judge duration
        are all the given duration.

        Args:
            new_sys_ctrt (pv.SysCtrt): The system contract instance.
            maker (pv.Account): The account of the contract maker.
            judge (pv.Account): The account of the contract judge.
            payer (pv.Account): The account of the contract payer.
            recipient (pv.Account): The account of the contract recipient.
            duration (int): The duration in seconds.

        Returns:
            pv.VEscrowCtrt: The VEscrowCtrt instance.
        """
        sc = new_sys_ctrt
        api = maker.api

        vc = await pv.VEscrowCtrt.register(
            by=maker,
            tok_id=sc.tok_id,
            duration=duration,
            judge_duration=duration,
        )
        await cft.wait_for_block()

        judge_resp, payer_resp, rcpt_resp = await asyncio.gather(
            sc.deposit(judge, vc.ctrt_id, self.CTRT_DEPOSIT_AMOUNT),
            sc.deposit(payer, vc.ctrt_id, self.CTRT_DEPOSIT_AMOUNT),
            sc.deposit(recipient, vc.ctrt_id, self.CTRT_DEPOSIT_AMOUNT),
        )
        await cft.wait_for_block()

        await asyncio.gather(
            cft.assert_tx_success(api, judge_resp["id"]),
            cft.assert_tx_success(api, payer_resp["id"]),
            cft.assert_tx_success(api, rcpt_resp["id"]),
        )
        return vc

    @pytest.fixture
    async def new_ctrt_with_ten_mins_duration(
        self,
        new_sys_ctrt: pv.SysCtrt,
        maker: pv.Account,
        judge: pv.Account,
        payer: pv.Account,
        recipient: pv.Account,
    ) -> pv.VEscrowCtrt:
        """
        new_ctrt_with_ten_mins_duration is the fixture that registers
        a new V Escrow Contract where the payer duration & judge duration
        are all 10 mins

        Args:
            new_sys_ctrt (pv.SysCtrt): The system contract instance.
            maker (pv.Account): The account of the contract maker.
            judge (pv.Account): The account of the contract judge.
            payer (pv.Account): The account of the contract payer.
            recipient (pv.Account): The account of the contract recipient.

        Returns:
            pv.VEscrowCtrt: The VEscrowCtrt instance.
        """
        ten_mins = 10 * 60
        return await self._new_ctrt(
            new_sys_ctrt,
            maker,
            judge,
            payer,
            recipient,
            ten_mins,
        )

    @pytest.fixture
    async def new_ctrt_with_five_secs_duration(
        self,
        new_sys_ctrt: pv.SysCtrt,
        maker: pv.Account,
        judge: pv.Account,
        payer: pv.Account,
        recipient: pv.Account,
    ) -> pv.VEscrowCtrt:
        """
        new_ctrt_with_ten_mins_duration is the fixture that registers
        a new V Escrow Contract where the payer duration & judge duration
        are all 5 secs.

        Args:
            new_sys_ctrt (pv.SysCtrt): The system contract instance.
            maker (pv.Account): The account of the contract maker.
            judge (pv.Account): The account of the contract judge.
            payer (pv.Account): The account of the contract payer.
            recipient (pv.Account): The account of the contract recipient.

        Returns:
            pv.VEscrowCtrt: The VEscrowCtrt instance.
        """
        five_secs = 5
        return await self._new_ctrt(
            new_sys_ctrt,
            maker,
            judge,
            payer,
            recipient,
            five_secs,
        )

    @pytest.fixture
    async def new_ctrt_ten_mins_duration_order(
        self,
        new_ctrt_with_ten_mins_duration: pv.VEscrowCtrt,
        payer: pv.Account,
        recipient: pv.Account,
    ) -> Tuple[pv.VEscrowCtrt, str]:
        """
        new_ctrt_ten_mins_duration_order is the fixture that registers
        a new V Escrow Contract where the payer duration & judge duration
        are all 10 mins with an order created.

        Args:
            new_ctrt_with_ten_mins_duration (pv.VEscrowCtrt): The V Escrow contract instance.
            payer (pv.Account): The account of the contract payer.
            recipient (pv.Account): The account of the contract recipient.

        Returns:
            pv.VEscrowCtrt: The VEscrowCtrt instance.
        """
        vc = new_ctrt_with_ten_mins_duration
        api = payer.api
        a_day_later = int(time.time()) + 60 * 60 * 24

        resp = await vc.create(
            by=payer,
            recipient=recipient.addr.b58_str,
            amount=self.ORDER_AMOUNT,
            rcpt_deposit_amount=self.RCPT_DEPOSIT_AMOUNT,
            judge_deposit_amount=self.JUDGE_DEPOSIT_AMOUNT,
            order_fee=self.ORDER_FEE,
            refund_amount=self.REFUND_AMOUNT,
            expire_at=a_day_later,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])
        order_id = resp["id"]

        return vc, order_id

    async def test_register(
        self,
        new_sys_ctrt: pv.SysCtrt,
        new_ctrt_with_ten_mins_duration: pv.VEscrowCtrt,
        maker: pv.Account,
    ) -> pv.VEscrowCtrt:
        """
        test_register tests the method register.

        Args:
            new_sys_ctrt (pv.SysCtrt): The system contract instance.
            new_ctrt_with_ten_mins_duration (pv.VEscrowCtrt): The V Escrow contract instance.
            maker (pv.Account): The account of the contract maker.

        Returns:
            pv.VEscrowCtrt: The VEscrowCtrt instance.
        """

        sc = new_sys_ctrt
        vc = new_ctrt_with_ten_mins_duration

        assert (await vc.maker).data == maker.addr.b58_str
        assert (await vc.judge).data == maker.addr.b58_str

        tok_id = await vc.tok_id
        assert tok_id.data == sc.tok_id

        ten_mins = 10 * 60
        duration = await vc.duration
        assert duration.unix_ts == ten_mins

        judge_duration = await vc.judge_duration
        assert judge_duration.unix_ts == ten_mins

        assert (await vc.unit) == (await sc.unit)

    async def test_supersede(
        self,
        new_ctrt_with_ten_mins_duration: pv.VEscrowCtrt,
        acnt0: pv.Account,
        acnt1: pv.Account,
    ) -> pv.VEscrowCtrt:
        """
        test_supersede tests the method supersede

        Args:
            new_ctrt_with_ten_mins_duration (pv.VEscrowCtrt): The V Escrow contract instance.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.

        Returns:
            pv.VEscrowCtrt: The VEscrowCtrt instance.
        """

        vc = new_ctrt_with_ten_mins_duration
        api = acnt0.api

        judge = await vc.judge
        assert judge.data == acnt0.addr.b58_str

        resp = await vc.supersede(acnt0, acnt1.addr.b58_str)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        judge = await vc.judge
        assert judge.data == acnt1.addr.b58_str

    async def test_create(
        self,
        new_ctrt_with_ten_mins_duration: pv.VEscrowCtrt,
        judge: pv.Account,
        payer: pv.Account,
        recipient: pv.Account,
    ) -> None:
        """
        test_create tests the method create.

        Args:
            new_ctrt_with_ten_mins_duration (pv.VEscrowCtrt): The V Escrow contract instance.
            maker (pv.Account): The account of the contract maker.
            payer (pv.Account): The account of the contract payer.
            recipient (pv.Account): The account of the contract recipient.
        """

        vc = new_ctrt_with_ten_mins_duration
        api = judge.api
        a_day_later = int(time.time()) + 60 * 60 * 24

        resp = await vc.create(
            by=payer,
            recipient=recipient.addr.b58_str,
            amount=self.ORDER_AMOUNT,
            rcpt_deposit_amount=self.RCPT_DEPOSIT_AMOUNT,
            judge_deposit_amount=self.JUDGE_DEPOSIT_AMOUNT,
            order_fee=self.ORDER_FEE,
            refund_amount=self.REFUND_AMOUNT,
            expire_at=a_day_later,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        order_id = resp["id"]

        assert (await vc.get_order_payer(order_id)).data == payer.addr.b58_str
        assert (await vc.get_order_recipient(order_id)).data == recipient.addr.b58_str
        assert (await vc.get_order_amount(order_id)).amount == self.ORDER_AMOUNT
        assert (
            await vc.get_order_recipient_deposit(order_id)
        ).amount == self.RCPT_DEPOSIT_AMOUNT
        assert (
            await vc.get_order_judge_deposit(order_id)
        ).amount == self.JUDGE_DEPOSIT_AMOUNT
        assert (await vc.get_order_fee(order_id)).amount == self.ORDER_FEE
        assert (
            await vc.get_order_recipient_amount(order_id)
        ).amount == self.ORDER_AMOUNT - self.ORDER_FEE
        assert (await vc.get_order_refund(order_id)).amount == self.REFUND_AMOUNT

        total_in_order = (
            self.ORDER_AMOUNT + self.RCPT_DEPOSIT_AMOUNT + self.JUDGE_DEPOSIT_AMOUNT
        )
        assert (
            await vc.get_order_recipient_refund(order_id)
        ).amount == total_in_order - self.REFUND_AMOUNT
        assert (await vc.get_order_expiration_time(order_id)).unix_ts == a_day_later
        assert (await vc.get_order_status(order_id)) is True
        assert (await vc.get_order_recipient_deposit_status(order_id)) is False
        assert (await vc.get_order_judge_deposit_status(order_id)) is False
        assert (await vc.get_order_submit_status(order_id)) is False
        assert (await vc.get_order_judge_status(order_id)) is False
        assert (await vc.get_order_recipient_locked_amount(order_id)).amount == 0
        assert (await vc.get_order_judge_locked_amount(order_id)).amount == 0

    async def test_recipient_deposit(
        self,
        new_ctrt_ten_mins_duration_order: Tuple[pv.VEscrowCtrt, str],
        recipient: pv.Account,
    ) -> None:
        """
        test_recipient_deposit tests the method recipient_deposit.

        Args:
            new_ctrt_ten_mins_duration_order (Tuple[pv.VEscrowCtrt, str]): The V Escrow contract instance
                where the payer duration & judge duration are all 10 mins and an order has been created.
            recipient (pv.Account): The account of the contract recipient.
        """
        vc, order_id = new_ctrt_ten_mins_duration_order
        api = recipient.api

        assert (await vc.get_order_recipient_deposit_status(order_id)) is False
        assert (await vc.get_order_recipient_locked_amount(order_id)).amount == 0

        resp = await vc.recipient_deposit(recipient, order_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await vc.get_order_recipient_deposit_status(order_id)) is True
        assert (
            await vc.get_order_recipient_locked_amount(order_id)
        ).amount == self.RCPT_DEPOSIT_AMOUNT
