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
    CTRT_DEPOSIT_AMOUNT = 50
    ORDER_PERIOD = 45  # in seconds
    DURATION = cft.AVG_BLOCK_DELAY * 2

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

    async def _create_order(
        self,
        vc: pv.VEscrowCtrt,
        payer: pv.Account,
        recipient: pv.Account,
        expire_at: int,
    ) -> Tuple[pv.VEscrowCtrt, str]:
        """
        _create_order creates an order for the given V Escrow contract.

        Args:
            vc (pv.VEscrowCtrt): A V Escrow contract instance.
            payer (pv.Account): The account of the contract payer.
            recipient (pv.Account): The account of the contract recipient.
            expire_at (int): The timestamp of the expiration time of the order.

        Returns:
            Tuple[pv.VEscrowCtrt, str]: The VEscrowCtrt instance and the order_id.
        """
        api = payer.api

        resp = await vc.create(
            by=payer,
            recipient=recipient.addr.data,
            amount=self.ORDER_AMOUNT,
            rcpt_deposit_amount=self.RCPT_DEPOSIT_AMOUNT,
            judge_deposit_amount=self.JUDGE_DEPOSIT_AMOUNT,
            order_fee=self.ORDER_FEE,
            refund_amount=self.REFUND_AMOUNT,
            expire_at=expire_at,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])
        order_id = resp["id"]

        return vc, order_id

    async def _deposit_to_order(
        self,
        vc: pv.VEscrowCtrt,
        order_id: str,
        recipient: pv.Account,
        judge: pv.Account,
    ) -> Tuple[pv.VEscrowCtrt, str]:
        """
        _deposit_to_order ensures every party has deposited into the order.

        Args:
            vc (pv.VEscrowCtrt): A V Escrow contract instance.
            order_id (str): The order ID.
            recipient (pv.Account): The account of the contract recipient.
            judge (pv.Account): The account of the contract judge.

        Returns:
            Tuple[pv.VEscrowCtrt, str]: The VEscrowCtrt instance and the order_id.
        """
        api = recipient.api

        # payer has deposited when creating the order
        # Let recipient & judge deposit
        rcpt_resp, judge_resp = await asyncio.gather(
            vc.recipient_deposit(recipient, order_id),
            vc.judge_deposit(judge, order_id),
        )
        await cft.wait_for_block()

        await asyncio.gather(
            cft.assert_tx_success(api, rcpt_resp["id"]),
            cft.assert_tx_success(api, judge_resp["id"]),
        )

        rcpt_status, judge_status = await asyncio.gather(
            vc.get_order_recipient_deposit_status(order_id),
            vc.get_order_judge_deposit_status(order_id),
        )

        assert rcpt_status is True
        assert judge_status is True

        return vc, order_id

    async def _submit_work(
        self,
        vc: pv.VEscrowCtrt,
        order_id: str,
        recipient: pv.Account,
    ) -> Tuple[pv.VEscrowCtrt, str]:
        """
        _submit_work submits the work of the order.

        Args:
            vc (pv.VEscrowCtrt): A V Escrow contract instance.
            order_id (str): The order ID.
            recipient (pv.Account): The account of the contract recipient.

        Returns:
            Tuple[pv.VEscrowCtrt, str]: The VEscrowCtrt instance and the order_id.
        """
        api = recipient.api

        resp = await vc.submit_work(recipient, order_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        return vc, order_id

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

    @pytest.fixture
    async def new_ctrt(
        self,
        new_sys_ctrt: pv.SysCtrt,
        maker: pv.Account,
        judge: pv.Account,
        payer: pv.Account,
        recipient: pv.Account,
    ) -> pv.VEscrowCtrt:
        """
        new_ctrt is the fixture that
        registers a new V Escrow Contract

        Args:
            new_sys_ctrt (pv.SysCtrt): The system contract instance.
            maker (pv.Account): The account of the contract maker.
            judge (pv.Account): The account of the contract judge.
            payer (pv.Account): The account of the contract payer.
            recipient (pv.Account): The account of the contract recipient.

        Returns:
            pv.VEscrowCtrt: The VEscrowCtrt instance.
        """
        return await self._new_ctrt(
            new_sys_ctrt,
            maker,
            judge,
            payer,
            recipient,
            self.DURATION,
        )

    @pytest.fixture
    async def new_ctrt_order(
        self,
        new_ctrt: pv.VEscrowCtrt,
        payer: pv.Account,
        recipient: pv.Account,
    ) -> Tuple[pv.VEscrowCtrt, str]:
        """
        new_ctrt_order is the fixture that registers
        a new V Escrow Contract where
        - an order is created.

        Args:
            new_ctrt (pv.VEscrowCtrt): The V Escrow contract instance.
            payer (pv.Account): The account of the contract payer.
            recipient (pv.Account): The account of the contract recipient.

        Returns:
            Tuple[pv.VEscrowCtrt, str]: The VEscrowCtrt instance and the order_id
        """
        vc = new_ctrt
        expire_at = int(time.time()) + self.ORDER_PERIOD
        return await self._create_order(vc, payer, recipient, expire_at)

    @pytest.fixture
    async def new_ctrt_order_deposited(
        self,
        new_ctrt_order: Tuple[pv.VEscrowCtrt, str],
        recipient: pv.Account,
        judge: pv.Account,
    ) -> Tuple[pv.VEscrowCtrt, str]:
        """
        new_ctrt_order_deposited is the fixture that registers
        a new V Escrow Contract where
        - an order is created.
        - payer, recipient, & judge have all deposited into it.

        Args:
            new_ctrt_order (Tuple[pv.VEscrowCtrt, str]): The V Escrow contract instance.
            recipient (pv.Account): The account of the contract recipient.
            judge (pv.Account): The account of the contract judge.

        Returns:
            Tuple[pv.VEscrowCtrt, str]: The VEscrowCtrt instance and the order_id
        """
        vc, order_id = new_ctrt_order
        return await self._deposit_to_order(vc, order_id, recipient, judge)

    @pytest.fixture
    async def new_ctrt_quick_expire_order_deposited(
        self,
        new_ctrt: pv.VEscrowCtrt,
        payer: pv.Account,
        recipient: pv.Account,
        judge: pv.Account,
    ) -> Tuple[pv.VEscrowCtrt, str]:
        """
        new_ctrt_quick_expire_order_deposited is the fixture that registers
        a new V Escrow Contract where
        - the payer duration & judge duration are all ten mins
        - an order that is expiring SOON is created

        Args:
            new_ctrt (pv.VEscrowCtrt): The V Escrow contract instance.
            payer (pv.Account): The account of the contract payer.
            recipient (pv.Account): The account of the contract recipient.
            judge (pv.Account): The account of the contract judge.

        Returns:
            Tuple[pv.VEscrowCtrt, str]: The VEscrowCtrt instance and the order_id
        """
        vc = new_ctrt
        five_secs_later = int(time.time()) + 5
        vc, order_id = await self._create_order(vc, payer, recipient, five_secs_later)
        return await self._deposit_to_order(vc, order_id, recipient, judge)

    @pytest.fixture
    async def new_ctrt_work_submitted(
        self,
        new_ctrt_order_deposited: Tuple[pv.VEscrowCtrt, str],
        recipient: pv.Account,
    ) -> Tuple[pv.VEscrowCtrt, str]:
        """
        new_ctrt_work_submitted is the fixture that registers
        a new V Escrow Contract where
        - an order is created.
        - payer, recipient, & judge have all deposited into it.
        - recipient has submitted the work.

        Args:
            new_ctrt_order_deposited (Tuple[pv.VEscrowCtrt, str]): The V Escrow contract instance.
            recipient (pv.Account): The account of the contract recipient.

        Returns:
            Tuple[pv.VEscrowCtrt, str]: The VEscrowCtrt instance and the order_id
        """
        vc, order_id = new_ctrt_order_deposited
        return await self._submit_work(vc, order_id, recipient)

    async def test_register(
        self,
        new_sys_ctrt: pv.SysCtrt,
        new_ctrt: pv.VEscrowCtrt,
        maker: pv.Account,
    ) -> pv.VEscrowCtrt:
        """
        test_register tests the method register.

        Args:
            new_sys_ctrt (pv.SysCtrt): The system contract instance.
            new_ctrt (pv.VEscrowCtrt): The V Escrow contract instance.
            maker (pv.Account): The account of the contract maker.

        Returns:
            pv.VEscrowCtrt: The VEscrowCtrt instance.
        """

        sc = new_sys_ctrt
        vc = new_ctrt

        assert (await vc.maker).data == maker.addr.data
        assert (await vc.judge).data == maker.addr.data

        tok_id = await vc.tok_id
        assert tok_id.data == sc.tok_id

        duration = await vc.duration
        assert duration.unix_ts == self.DURATION

        judge_duration = await vc.judge_duration
        assert judge_duration.unix_ts == self.DURATION

        assert (await vc.unit) == (await sc.unit)

    async def test_supersede(
        self,
        new_ctrt: pv.VEscrowCtrt,
        acnt0: pv.Account,
        acnt1: pv.Account,
    ) -> pv.VEscrowCtrt:
        """
        test_supersede tests the method supersede

        Args:
            new_ctrt (pv.VEscrowCtrt): The V Escrow contract instance.
            acnt0 (pv.Account): The account of nonce 0.
            acnt1 (pv.Account): The account of nonce 1.

        Returns:
            pv.VEscrowCtrt: The VEscrowCtrt instance.
        """

        vc = new_ctrt
        api = acnt0.api

        judge = await vc.judge
        assert judge.data == acnt0.addr.data

        resp = await vc.supersede(acnt0, acnt1.addr.data)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        judge = await vc.judge
        assert judge.data == acnt1.addr.data

    async def test_create(
        self,
        new_ctrt: pv.VEscrowCtrt,
        payer: pv.Account,
        recipient: pv.Account,
        judge: pv.Account,
    ) -> Tuple[pv.VEscrowCtrt, str]:
        """
        test_create tests the method create.

        Args:
            new_ctrt (pv.VEscrowCtrt): The V Escrow contract instance.
            payer (pv.Account): The account of the contract payer.
            recipient (pv.Account): The account of the contract recipient.
            judge (pv.Account): The account of the contract judge.

        Returns:
            Tuple[pv.VEscrowCtrt, str]: The VEscrowCtrt instance and the order_id
        """

        vc = new_ctrt
        api = judge.api
        later = int(time.time()) + self.ORDER_PERIOD

        resp = await vc.create(
            by=payer,
            recipient=recipient.addr.data,
            amount=self.ORDER_AMOUNT,
            rcpt_deposit_amount=self.RCPT_DEPOSIT_AMOUNT,
            judge_deposit_amount=self.JUDGE_DEPOSIT_AMOUNT,
            order_fee=self.ORDER_FEE,
            refund_amount=self.REFUND_AMOUNT,
            expire_at=later,
        )
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        order_id = resp["id"]

        assert (await vc.get_order_payer(order_id)).data == payer.addr.data
        assert (await vc.get_order_recipient(order_id)).data == recipient.addr.data
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
        assert (await vc.get_order_expiration_time(order_id)).unix_ts == later
        assert (await vc.get_order_status(order_id)) is True
        assert (await vc.get_order_recipient_deposit_status(order_id)) is False
        assert (await vc.get_order_judge_deposit_status(order_id)) is False
        assert (await vc.get_order_submit_status(order_id)) is False
        assert (await vc.get_order_judge_status(order_id)) is False
        assert (await vc.get_order_recipient_locked_amount(order_id)).amount == 0
        assert (await vc.get_order_judge_locked_amount(order_id)).amount == 0

        return vc, order_id

    async def test_recipient_deposit(
        self,
        new_ctrt_order: Tuple[pv.VEscrowCtrt, str],
        recipient: pv.Account,
    ) -> None:
        """
        test_recipient_deposit tests the method recipient_deposit.

        Args:
            new_ctrt_order (Tuple[pv.VEscrowCtrt, str]): The V Escrow contract instance.
            recipient (pv.Account): The account of the contract recipient.
        """
        vc, order_id = new_ctrt_order
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

    async def test_judge_deposit(
        self,
        new_ctrt_order: Tuple[pv.VEscrowCtrt, str],
        judge: pv.Account,
    ) -> None:
        """
        test_judge_deposit tests the method judge_deposit.

        Args:
            new_ctrt_order (Tuple[pv.VEscrowCtrt, str]): The V Escrow contract instance.
            judge (pv.Account): The account of the contract judge.
        """
        vc, order_id = new_ctrt_order
        api = judge.api

        assert (await vc.get_order_judge_deposit_status(order_id)) is False
        assert (await vc.get_order_judge_locked_amount(order_id)).amount == 0

        resp = await vc.judge_deposit(judge, order_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await vc.get_order_judge_deposit_status(order_id)) is True
        assert (
            await vc.get_order_judge_locked_amount(order_id)
        ).amount == self.JUDGE_DEPOSIT_AMOUNT

    async def test_payer_cancel(
        self,
        new_ctrt_order: Tuple[pv.VEscrowCtrt, str],
        payer: pv.Account,
    ) -> None:
        """
        test_payer_cancel tests the method payer_cancel.

        Args:
            new_ctrt_order (Tuple[pv.VEscrowCtrt, str]): The V Escrow contract instance.
            payer (pv.Account): The account of the contract payer.
        """

        vc, order_id = new_ctrt_order
        api = payer.api

        assert (await vc.get_order_status(order_id)) is True

        resp = await vc.payer_cancel(payer, order_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await vc.get_order_status(order_id)) is False

    async def test_recipient_cancel(
        self,
        new_ctrt_order: Tuple[pv.VEscrowCtrt, str],
        recipient: pv.Account,
    ) -> None:
        """
        test_recipient_cancel tests the method recipient_cancel.

        Args:
            new_ctrt_order (Tuple[pv.VEscrowCtrt, str]): The V Escrow contract instance.
            recipient (pv.Account): The account of the contract recipient.
        """

        vc, order_id = new_ctrt_order
        api = recipient.api

        assert (await vc.get_order_status(order_id)) is True

        resp = await vc.recipient_cancel(recipient, order_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await vc.get_order_status(order_id)) is False

    async def test_judge_cancel(
        self,
        new_ctrt_order: Tuple[pv.VEscrowCtrt, str],
        judge: pv.Account,
    ) -> None:
        """
        test_judge_cancel tests the method judge_cancel.

        Args:
            new_ctrt_order (Tuple[pv.VEscrowCtrt, str]): The V Escrow contract instance.
            judge (pv.Account): The account of the contract judge.
        """

        vc, order_id = new_ctrt_order
        api = judge.api

        assert (await vc.get_order_status(order_id)) is True

        resp = await vc.judge_cancel(judge, order_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await vc.get_order_status(order_id)) is False

    async def test_submit_work(
        self,
        new_ctrt_order_deposited: Tuple[pv.VEscrowCtrt, str],
        recipient: pv.Account,
    ) -> None:
        """
        test_submit_work tests the method submit_work.

        Args:
            new_ctrt_order_deposited (Tuple[pv.VEscrowCtrt, str]): The V Escrow contract instance.
            recipient (pv.Account): The account of the contract recipient.
        """

        vc, order_id = new_ctrt_order_deposited
        api = recipient.api

        assert (await vc.get_order_submit_status(order_id)) is False

        resp = await vc.submit_work(recipient, order_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await vc.get_order_submit_status(order_id)) is True

    async def test_approve_work(
        self,
        new_ctrt_work_submitted: Tuple[pv.VEscrowCtrt, str],
        payer: pv.Account,
        recipient: pv.Account,
        judge: pv.Account,
    ) -> None:
        """
        test_approve_work tests the method approve_work.

        Args:
            new_ctrt_work_submitted (Tuple[pv.VEscrowCtrt, str]): The V Escrow contract instance.
            payer (pv.Account): The account of the contract payer.
            recipient (pv.Account): The account of the contract recipient.
            judge (pv.Account): The account of the contract judge.
        """
        vc, order_id = new_ctrt_work_submitted
        api = payer.api

        rcpt_bal_old, judge_bal_old = await asyncio.gather(
            vc.get_ctrt_bal(recipient.addr.data), vc.get_ctrt_bal(judge.addr.data)
        )

        assert (await vc.get_order_status(order_id)) is True

        resp = await vc.approve_work(payer, order_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await vc.get_order_status(order_id)) is False

        rcpt_amt, fee, rcpt_dep, judge_dep, rcpt_bal, judge_bal = await asyncio.gather(
            vc.get_order_recipient_amount(order_id),
            vc.get_order_fee(order_id),
            vc.get_order_recipient_deposit(order_id),
            vc.get_order_judge_deposit(order_id),
            vc.get_ctrt_bal(recipient.addr.data),
            vc.get_ctrt_bal(judge.addr.data),
        )

        assert (
            rcpt_bal.amount - rcpt_bal_old.amount == rcpt_amt.amount + rcpt_dep.amount
        )
        assert judge_bal.amount - judge_bal_old.amount == fee.amount + judge_dep.amount

    async def test_apply_to_judge_and_do_judge(
        self,
        new_ctrt_work_submitted: Tuple[pv.VEscrowCtrt, str],
        payer: pv.Account,
        recipient: pv.Account,
        judge: pv.Account,
    ) -> None:
        """
        test_approve_work tests the method
        - apply_to_judge
        - do_judge

        Args:
            new_ctrt_work_submitted (Tuple[pv.VEscrowCtrt, str]): The V Escrow contract instance.
            payer (pv.Account): The account of the contract payer.
            recipient (pv.Account): The account of the contract recipient.
            judge (pv.Account): The account of the contract judge.
        """
        vc, order_id = new_ctrt_work_submitted
        api = payer.api

        payer_bal_old, rcpt_bal_old, judge_bal_old = await asyncio.gather(
            vc.get_ctrt_bal(payer.addr.data),
            vc.get_ctrt_bal(recipient.addr.data),
            vc.get_ctrt_bal(judge.addr.data),
        )
        assert (await vc.get_order_status(order_id)) is True

        resp = await vc.apply_to_judge(payer, order_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        # The judge is dividing the amount that
        # == payer_deposit + recipient_deposit - fee
        # In this case, the amount is 8
        to_payer = 3
        to_rcpt = 5

        resp = await vc.do_judge(judge, order_id, to_payer, to_rcpt)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await vc.get_order_status(order_id)) is False

        fee, judge_dep, payer_bal, rcpt_bal, judge_bal = await asyncio.gather(
            vc.get_order_fee(order_id),
            vc.get_order_judge_deposit(order_id),
            vc.get_ctrt_bal(payer.addr.data),
            vc.get_ctrt_bal(recipient.addr.data),
            vc.get_ctrt_bal(judge.addr.data),
        )

        assert payer_bal.amount - payer_bal_old.amount == to_payer
        assert rcpt_bal.amount - rcpt_bal_old.amount == to_rcpt
        assert judge_bal.amount - judge_bal_old.amount == fee.amount + judge_dep.amount

    async def test_submit_penalty(
        self,
        new_ctrt_quick_expire_order_deposited: Tuple[pv.VEscrowCtrt, str],
        payer: pv.Account,
        judge: pv.Account,
    ) -> None:
        """
        test_submit_penalty tests the method submit_penalty.

        Args:
            new_ctrt_quick_expire_order_deposited (Tuple[pv.VEscrowCtrt, str]): The V Escrow contract instance
            payer (pv.Account): The account of the contract payer.
            judge (pv.Account): The account of the contract judge.
        """
        vc, order_id = new_ctrt_quick_expire_order_deposited
        api = payer.api

        payer_bal_old, judge_bal_old, expire_at = await asyncio.gather(
            vc.get_ctrt_bal(payer.addr.data),
            vc.get_ctrt_bal(judge.addr.data),
            vc.get_order_expiration_time(order_id),
        )
        assert (await vc.get_order_status(order_id)) is True

        # Ensure that the recipient submit work grace period has expired.
        now = int(time.time())
        await asyncio.sleep(expire_at.unix_ts - now + cft.AVG_BLOCK_DELAY)

        resp = await vc.submit_penalty(payer, order_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await vc.get_order_status(order_id)) is False

        rcpt_amt, rcpt_dep, fee, judge_dep, payer_bal, judge_bal = await asyncio.gather(
            vc.get_order_recipient_amount(order_id),
            vc.get_order_recipient_deposit(order_id),
            vc.get_order_fee(order_id),
            vc.get_order_judge_deposit(order_id),
            vc.get_ctrt_bal(payer.addr.data),
            vc.get_ctrt_bal(judge.addr.data),
        )

        assert (
            payer_bal.amount - payer_bal_old.amount == rcpt_amt.amount + rcpt_dep.amount
        )
        assert judge_bal.amount - judge_bal_old.amount == fee.amount + judge_dep.amount

    async def test_payer_refund(
        self,
        new_ctrt_work_submitted: Tuple[pv.VEscrowCtrt, str],
        payer: pv.Account,
        recipient: pv.Account,
    ) -> None:
        """
        test_payer_refund tests the method payer_refund.

        Args:
            new_ctrt_work_submitted (Tuple[pv.VEscrowCtrt, str]): The V Escrow contract instance.
            payer (pv.Account): The account of the contract payer.
            recipient (pv.Account): The account of the contract recipient.
        """
        vc, order_id = new_ctrt_work_submitted
        api = payer.api

        payer_bal_old, rcpt_bal_old, expire_at = await asyncio.gather(
            vc.get_ctrt_bal(payer.addr.data),
            vc.get_ctrt_bal(recipient.addr.data),
            vc.get_order_expiration_time(order_id),
        )
        assert (await vc.get_order_status(order_id)) is True

        resp = await vc.apply_to_judge(payer, order_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        # Wait until the judge duration has exceeded.
        now = int(time.time())
        await asyncio.sleep(expire_at.unix_ts - now + cft.AVG_BLOCK_DELAY)

        resp = await vc.payer_refund(payer, order_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await vc.get_order_status(order_id)) is False

        payer_refund, rcpt_refund, payer_bal, rcpt_bal = await asyncio.gather(
            vc.get_order_refund(order_id),
            vc.get_order_recipient_refund(order_id),
            vc.get_ctrt_bal(payer.addr.data),
            vc.get_ctrt_bal(recipient.addr.data),
        )

        assert payer_bal.amount - payer_bal_old.amount == payer_refund.amount
        assert rcpt_bal.amount - rcpt_bal_old.amount == rcpt_refund.amount

    async def test_recipient_refund(
        self,
        new_ctrt_work_submitted: Tuple[pv.VEscrowCtrt, str],
        payer: pv.Account,
        recipient: pv.Account,
    ) -> None:
        """
        test_recipient_refund tests the method recipient_refund.

        Args:
            new_ctrt_work_submitted (Tuple[pv.VEscrowCtrt, str]): The V Escrow contract instance.
            payer (pv.Account): The account of the contract payer.
            recipient (pv.Account): The account of the contract recipient.
        """
        vc, order_id = new_ctrt_work_submitted
        api = payer.api

        payer_bal_old, rcpt_bal_old, expire_at = await asyncio.gather(
            vc.get_ctrt_bal(payer.addr.data),
            vc.get_ctrt_bal(recipient.addr.data),
            vc.get_order_expiration_time(order_id),
        )
        assert (await vc.get_order_status(order_id)) is True

        resp = await vc.apply_to_judge(payer, order_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        # Wait until the judge duration has exceeded.
        now = int(time.time())
        await asyncio.sleep(expire_at.unix_ts - now + cft.AVG_BLOCK_DELAY)

        resp = await vc.recipient_refund(recipient, order_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await vc.get_order_status(order_id)) is False

        payer_refund, rcpt_refund, payer_bal, rcpt_bal = await asyncio.gather(
            vc.get_order_refund(order_id),
            vc.get_order_recipient_refund(order_id),
            vc.get_ctrt_bal(payer.addr.data),
            vc.get_ctrt_bal(recipient.addr.data),
        )

        assert payer_bal.amount - payer_bal_old.amount == payer_refund.amount
        assert rcpt_bal.amount - rcpt_bal_old.amount == rcpt_refund.amount

    async def test_collect(
        self,
        new_ctrt_work_submitted: Tuple[pv.VEscrowCtrt, str],
        recipient: pv.Account,
        judge: pv.Account,
    ) -> None:
        """
        test_collect tests the method collect.

        Args:
            new_ctrt_work_submitted (Tuple[pv.VEscrowCtrt, str]): The V Escrow contract instance where the payer duration & judge duration are
            recipient (pv.Account): The account of the contract recipient.
            judge (pv.Account): The account of the contract judge.
        """
        vc, order_id = new_ctrt_work_submitted
        api = recipient.api

        rcpt_bal_old, judge_bal_old, expire_at = await asyncio.gather(
            vc.get_ctrt_bal(recipient.addr.data),
            vc.get_ctrt_bal(judge.addr.data),
            vc.get_order_expiration_time(order_id),
        )
        assert (await vc.get_order_status(order_id)) is True

        now = int(time.time())
        await asyncio.sleep(expire_at.unix_ts - now + cft.AVG_BLOCK_DELAY)

        resp = await vc.collect(recipient, order_id)
        await cft.wait_for_block()
        await cft.assert_tx_success(api, resp["id"])

        assert (await vc.get_order_status(order_id)) is False

        rcpt_bal, rcpt_amt, rcpt_dep, judge_bal, fee, judge_dep = await asyncio.gather(
            vc.get_ctrt_bal(recipient.addr.data),
            vc.get_order_recipient_amount(order_id),
            vc.get_order_recipient_deposit(order_id),
            vc.get_ctrt_bal(judge.addr.data),
            vc.get_order_fee(order_id),
            vc.get_order_judge_deposit(order_id),
        )

        assert (
            rcpt_bal.amount - rcpt_bal_old.amount == rcpt_amt.amount + rcpt_dep.amount
        )
        assert judge_bal.amount - judge_bal_old.amount == fee.amount + judge_dep.amount

    @pytest.mark.whole
    async def test_as_whole(
        self,
        new_sys_ctrt: pv.SysCtrt,
        new_ctrt: pv.VEscrowCtrt,
        new_ctrt_quick_expire_order_deposited: Tuple[pv.VEscrowCtrt, str],
        maker: pv.Account,
        judge: pv.Account,
        payer: pv.Account,
        recipient: pv.Account,
    ) -> None:
        """
        test_as_whole tests methods of PayChanCtrt as a whole so as to reduce resource consumption.

        Args:
            new_sys_ctrt (pv.SysCtrt): The system contract instance.
            maker (pv.Account): The account of the contract maker.
            judge (pv.Account): The account of the contract judge.
            payer (pv.Account): The account of the contract payer.
            recipient (pv.Account): The account of the contract recipient.
        """
        vc = new_ctrt
        sc = new_sys_ctrt

        await self.test_register(sc, vc, maker)
        vc_with_order = await self.test_create(vc, payer, recipient, judge)
        await self.test_recipient_deposit(vc_with_order, recipient)
        await self.test_judge_deposit(vc_with_order, judge)
        await self.test_submit_work(vc_with_order, recipient)
        await self.test_approve_work(vc_with_order, payer, recipient, judge)

        # cancel to be tested

        expire_at = int(time.time()) + self.ORDER_PERIOD
        vc_with_order = await self._create_order(vc, payer, recipient, expire_at)
        await self.test_payer_cancel(vc_with_order, payer)

        expire_at = int(time.time()) + self.ORDER_PERIOD
        vc_with_order = await self._create_order(vc, payer, recipient, expire_at)
        await self.test_recipient_cancel(vc_with_order, recipient)

        expire_at = int(time.time()) + self.ORDER_PERIOD
        vc_with_order = await self._create_order(vc, payer, recipient, expire_at)
        await self.test_judge_cancel(vc_with_order, judge)

        expire_at = int(time.time()) + self.ORDER_PERIOD
        vc, order_id = await self._create_order(vc, payer, recipient, expire_at)
        vc, order_id = await self._deposit_to_order(vc, order_id, recipient, judge)
        vc_with_order = await self._submit_work(vc, order_id, recipient)
        await self.test_apply_to_judge_and_do_judge(
            vc_with_order, payer, recipient, judge
        )

        vc_with_order = new_ctrt_quick_expire_order_deposited
        await self.test_submit_penalty(vc_with_order, payer, judge)

        expire_at = int(time.time()) + self.ORDER_PERIOD
        vc, order_id = await self._create_order(vc, payer, recipient, expire_at)
        vc, order_id = await self._deposit_to_order(vc, order_id, recipient, judge)
        vc_with_order = await self._submit_work(vc, order_id, recipient)
        await self.test_payer_refund(vc_with_order, payer, recipient)

        expire_at = int(time.time()) + self.ORDER_PERIOD
        vc, order_id = await self._create_order(vc, payer, recipient, expire_at)
        vc, order_id = await self._deposit_to_order(vc, order_id, recipient, judge)
        vc_with_order = await self._submit_work(vc, order_id, recipient)
        await self.test_recipient_refund(vc_with_order, payer, recipient)

        expire_at = int(time.time()) + self.ORDER_PERIOD
        vc, order_id = await self._create_order(vc, payer, recipient, expire_at)
        vc, order_id = await self._deposit_to_order(vc, order_id, recipient, judge)
        vc_with_order = await self._submit_work(vc, order_id, recipient)
        await self.test_collect(vc_with_order, recipient, judge)

        await self.test_supersede(vc, maker, payer)
