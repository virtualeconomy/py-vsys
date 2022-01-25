"""
account contains account-related resources
"""
from __future__ import annotations
from typing import Any, Dict, TYPE_CHECKING

from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import chain as ch
    from py_v_sdk import api

from py_v_sdk import model as md
from py_v_sdk import tx_req as tx
from py_v_sdk.utils.crypto import hashes as hs
from py_v_sdk.utils.crypto import curve_25519 as curve


class Account:
    """
    Account is a class for an account on the chain.
    """

    ADDR_VER = 5

    def __init__(self, chain: ch.Chain, seed: str, nonce: int = 0) -> None:
        """
        Args:
            chain (ch.Chain): The chain that the account is on.
            seed (str): The seed string of the account.
            nonce (int, optional): The nonce of the account. Defaults to 0.
        """
        self._chain = chain
        self._seed = md.Str(seed)
        self._nonce = md.Nonce(nonce)
        self._acnt_seed_hash = self.get_acnt_seed_hash(seed, nonce)
        self._key_pair = self.get_key_pair(self._acnt_seed_hash.data)
        self._addr = self.get_addr(
            self.key_pair.pub.bytes, self.ADDR_VER, self.chain.chain_id
        )

    @property
    def chain(self) -> ch.Chain:
        """
        chain returns the chain that the account is on.

        Returns:
            ch.Chain: The chain that the account is on.
        """
        return self._chain

    @property
    def api(self) -> api.NodeAPI:
        """
        api returns the NodeAPI object that the account's chain uses.

        Returns:
            api.NodeAPI: The NodeAPI object that the account's chain uses.
        """
        return self._chain.api

    @property
    def seed(self) -> str:
        """
        seed returns the account's seed string.

        Returns:
            str: The account's seed string.
        """
        return self._seed.data

    @property
    def nonce(self) -> int:
        """
        nonce returns the account's nonce.

        Returns:
            int: The account's nonce.
        """
        return self._nonce.data

    @property
    def acnt_seed_hash(self) -> md.Bytes:
        """
        acnt_seed_hash returns the account's account seed hash.

        Returns:
            md.Bytes: The account's account seed hash.
        """
        return self._acnt_seed_hash

    @property
    def key_pair(self) -> md.KeyPair:
        """
        key_pair returns the account's key pair.

        Returns:
            md.KeyPair: The account's key pair.
        """
        return self._key_pair

    @property
    def addr(self) -> md.Bytes:
        """
        addr returns the account's address.

        Returns:
            md.Bytes: The account's address.
        """
        return self._addr

    @property
    async def balance(self) -> int:
        """
        balance returns the account's balance.

        Returns:
            int: The account's balance.
        """
        resp = await self.api.addr.get_balance(self.addr.b58_str)
        return resp["balance"]

    @property
    async def effective_balance(self) -> int:
        """
        effective_balance returns the account's effective balance(i.e. The balance that can be spent).

        Returns:
            int: The account's effective balance.
        """
        resp = await self.api.addr.get_effective_balance(self.addr.b58_str)
        return resp["balance"]

    async def _pay(self, req: tx.PaymentTxReq) -> Dict[str, Any]:
        """
        _pay sends a payment transaction request on behalf of the account.

        Args:
            req (tx.PaymentTxReq): The payment transaction request.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """
        return await self.api.vsys.broadcast_payment(
            req.to_broadcast_payment_payload(self.key_pair)
        )

    async def pay(
        self,
        recipient: str,
        amount: int | float,
        attachment: str = "",
        fee: int = md.PaymentFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        pay pays the VSYS coins from the action taker to the recipient.

        Args:
            recipient (str): The account address of the recipient.
            amount (int | float): The amount of VSYS coins to send.
            attachment (str, optional): The attachment of the action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.PaymentFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """
        rcpt_md = md.Addr(recipient)
        rcpt_md.must_on(self.chain)

        data = await self._pay(
            tx.PaymentTxReq(
                recipient=rcpt_md,
                amount=md.VSYS.for_amount(amount),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.PaymentFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def _lease(self, req: tx.LeaseTxReq) -> Dict[str, Any]:
        """
        _lease sends a leasing transaction request on behalf of the account.

        Args:
            req (tx.LeaseTxReq): The leasing transaction request.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """
        return await self.api.leasing.broadcast_lease(
            req.to_broadcast_leasing_payload(self.key_pair)
        )

    async def lease(
        self,
        recipient: str,
        amount: int | float,
        fee: int = md.LeasingFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        lease leases the VSYS coins from the action taker to the recipient(a supernode).

        Args:
            recipient (str): The account address of the recipient.
            amount (int | float): The amount of VSYS coins to send.
            fee (int, optional): The fee to pay for this action. Defaults to md.LeasingFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """
        rcpt_md = md.Addr(recipient)
        rcpt_md.must_on(self.chain)

        data = await self._lease(
            tx.LeaseTxReq(
                recipient=rcpt_md,
                amount=md.VSYS.for_amount(amount),
                timestamp=md.VSYSTimestamp.now(),
                fee=md.LeasingFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def _cancel_lease(self, req: tx.LeaseCancelTxReq) -> Dict[str, Any]:
        """
        _cancel_lease sends a leasing cancel transaction request on behalf of the account.

        Args:
            req (tx.LeaseCancelTxReq): The leasing cancel transaction request.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """
        return await self.api.leasing.broadcast_cancel(
            req.to_broadcast_cancel_payload(self.key_pair)
        )

    async def cancel_lease(
        self,
        leasing_tx_id: str,
        fee: int = md.LeasingCancelFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        cancel_lease cancels the leasing.

        Args:
            leasing_tx_id (str): The transaction ID of the leasing.
            fee (int, optional): The fee to pay for this action. Defaults to md.LeasingCancelFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """

        data = await self._cancel_lease(
            tx.LeaseCancelTxReq(
                leasing_tx_id=md.TXID(leasing_tx_id),
                timestamp=md.VSYSTimestamp.now(),
                fee=md.LeasingCancelFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def _register_contract(self, req: tx.RegCtrtTxReq) -> Dict[str, Any]:
        """
        _register_contract sends a register contract transaction on behalf of the account.

        Args:
            req (tx.RegCtrtTxReq): The register contract transaction request.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """
        return await self.api.ctrt.broadcast_register(
            req.to_broadcast_register_payload(self.key_pair)
        )

    async def _execute_contract(self, req: tx.ExecCtrtFuncTxReq) -> Dict[str, Any]:
        """
        _execute_contract sends an execute contract transaction on behalf of the account.

        Args:
            req (tx.ExecCtrtFuncTxReq): The execute contract transaction request.

        Returns:
            Dict[str, Any]: The response returned by the Node API.
        """
        return await self.api.ctrt.broadcast_execute(
            req.to_broadcast_execute_payload(self.key_pair)
        )

    @staticmethod
    def get_key_pair(acnt_seed_hash: bytes) -> md.KeyPair:
        """
        get_key_pair generates a key pair based on the given account seed hash.

        Args:
            acnt_seed_hash (bytes): The account seed hash.

        Returns:
            md.KeyPair: The generated key pair.
        """
        pri_key = curve.gen_pri_key(acnt_seed_hash)
        pub_key = curve.gen_pub_key(pri_key)

        return md.KeyPair(
            pub=md.PubKey.from_bytes(pub_key),
            pri=md.PriKey.from_bytes(pri_key),
        )

    @staticmethod
    def get_addr(pub_key: bytes, addr_ver: int, chain_id: ch.ChainID) -> md.Bytes:
        """
        get_addr generates the address based on the given data.

        Args:
            pub_key (bytes): The public key.
            addr_ver (int): The address version.
            chain_id (ch.ChainID): The chain ID.

        Returns:
            md.Bytes: The generated address.
        """

        def ke_bla_hash(b: bytes) -> bytes:
            return hs.keccak256_hash(hs.blake2b_hash(b))

        raw_addr: str = (
            chr(addr_ver) + chain_id.value + ke_bla_hash(pub_key).decode("latin-1")[:20]
        )

        checksum: str = ke_bla_hash(raw_addr.encode("latin-1")).decode("latin-1")[:4]

        b = bytes((raw_addr + checksum).encode("latin-1"))
        return md.Bytes(b)

    @staticmethod
    def get_acnt_seed_hash(seed: str, nonce: int) -> md.Bytes:
        """
        get_acnt_seed_hash generates account seed hash based on the given seed & nonce.

        Args:
            seed (str): The account seed.
            nonce (int): The account nonce.

        Returns:
            md.Bytes: The generated account seed hash.
        """
        b = hs.sha256_hash(
            hs.keccak256_hash(hs.blake2b_hash(f"{nonce}{seed}".encode("latin-1")))
        )
        return md.Bytes(b)
