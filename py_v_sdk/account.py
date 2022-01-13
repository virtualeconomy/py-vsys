from typing import Any, Dict

from py_v_sdk import tx_req as tx
from py_v_sdk import chain as ch
from py_v_sdk import api
from py_v_sdk import model as md
from py_v_sdk.utils import bytes as bu
from py_v_sdk.utils.crypto import hashes as hs
from py_v_sdk.utils.crypto import curve_25519 as curve


class Account:

    ADDR_VER = 5

    def __init__(self, chain: ch.Chain, seed: str, nonce: int = 0):
        self._chain = chain
        self._seed = seed
        self._nonce = nonce
        self._acnt_seed_hash = self.get_acnt_seed_hash(seed, nonce)
        self._key_pair = self.get_key_pair(self._acnt_seed_hash)
        self._addr = self.get_addr(
            self.key_pair.pub, self.ADDR_VER, self.chain.chain_id
        )

    @property
    def chain(self) -> ch.Chain:
        return self._chain

    @property
    def api(self) -> api.NodeAPI:
        return self._chain.api

    @property
    def seed(self) -> str:
        return self._seed

    @property
    def nonce(self) -> int:
        return self._nonce

    @property
    def acnt_seed_hash(self) -> md.Bytes:
        return self._acnt_seed_hash

    @property
    def key_pair(self) -> md.KeyPair:
        return self._key_pair

    @property
    def addr(self) -> md.Bytes:
        return self._addr

    @staticmethod
    def get_acnt_seed_hash(seed: str, nonce: int) -> md.Bytes:
        return md.Bytes(
            hs.sha256_hash(
                hs.keccak256_hash(hs.blake2b_hash(bu.str_to_bytes(f"{nonce}{seed}")))
            )
        )

    @staticmethod
    def get_key_pair(acnt_seed_hash: md.Bytes) -> md.KeyPair:
        pri_key = curve.gen_pri_key(acnt_seed_hash.bytes)
        pub_key = curve.gen_pub_key(pri_key)

        return curve.KeyPair(
            pub=md.Bytes(pub_key),
            pri=md.Bytes(pri_key),
        )

    @staticmethod
    def get_addr(pub_key: md.Bytes, addr_ver: int, chain_id: ch.ChainID) -> md.Bytes:
        def hash(b: bytes) -> bytes:
            return hs.keccak256_hash(hs.blake2b_hash(b))

        raw_addr: str = (
            chr(addr_ver) + chain_id.value + bu.bytes_to_str(hash(pub_key.bytes))[:20]
        )

        addr_hash: str = bu.bytes_to_str(hash(bu.str_to_bytes(raw_addr)))[:4]

        return md.Bytes(bu.str_to_bytes(raw_addr + addr_hash))

    @property
    def balance(self) -> int:
        return self.api.addr.get_balance(self.addr.b58_str)["balance"]

    def register_contract(self, req: tx.RegCtrtTxReq) -> Dict[str, Any]:
        return self.api.ctrt.broadcast_register(
            req.to_broadcast_register_payload(self.key_pair)
        )

    def execute_contract(self, req: tx.ExecCtrtFuncTxReq) -> Dict[str, Any]:
        return self.api.ctrt.broadcast_execute(
            req.to_broadcast_execute_payload(self.key_pair)
        )
