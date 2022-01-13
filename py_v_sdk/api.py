import abc
import json
from typing import Any, Dict, Optional

import requests


class NodeAPI:
    def __init__(
        self, host: str, api_key: Optional[str] = None, timeout: Optional[int] = None
    ):
        self._host = host

        self._sess = requests.Session()
        self._sess.headers.update({"Content-Type": "application/json"})
        if api_key:
            self._sess.headers.update({"api_key": api_key})
        if timeout:
            self._sess.timeout = timeout

        self._blocks = Blocks(self._host, self._sess)
        self._node = Node(self._host, self._sess)
        self._ctrt = Contract(self._host, self._sess)
        self._addr = Addresses(self._host, self._sess)

    @property
    def host(self) -> str:
        return self.host

    @property
    def blocks(self) -> "Blocks":
        return self._blocks

    @property
    def node(self) -> "Node":
        return self._node

    @property
    def ctrt(self) -> "Contract":
        return self._ctrt

    @property
    def addr(self) -> "Addresses":
        return self._addr


class APIGrp(abc.ABC):
    PREFIX = ""

    def __init__(self, host: str, sess: requests.Session):
        self._host = host
        self._sess = sess

    def _make_url(self, edpt: str) -> str:
        return self._host + self.PREFIX + edpt

    def get(self, edpt: str) -> Dict[str, Any]:
        url = self._make_url(edpt)
        return self._sess.get(url).json()

    def post(self, edpt: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = self._make_url(edpt)
        return self._sess.post(url, json.dumps(payload)).json()


class Blocks(APIGrp):
    PREFIX = "/blocks"

    def get_height(self) -> Dict[str, Any]:
        return self.get("/height")

    def get_last_block(self) -> Dict[str, Any]:
        return self.get("/last")


class Node(APIGrp):
    PREFIX = "/node"

    def get_status(self) -> Dict[str, Any]:
        return self.get("/status")

    def get_version(self) -> Dict[str, Any]:
        return self.get("/version")


class Contract(APIGrp):
    PREFIX = "/contract"

    def broadcast_register(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.post("/broadcast/register", payload)

    def broadcast_execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.post("/broadcast/execute", payload)

    def get_contract_data(self, ctrt_id: str, db_key: str) -> Dict[str, Any]:
        return self.get(f"/data/{ctrt_id}/{db_key}")


class Addresses(APIGrp):
    PREFIX = "/addresses"

    def get_addr(self, pub_key: str) -> Dict[str, Any]:
        """
        get_addr gets the address from the public key

        Args:
            pub_key (str): The public key in base58 format string

        Returns:
            Dict[str, Any]: The response
        """
        return self.get(f"/publicKey/{pub_key}")

    def get_balance(self, addr: str) -> Dict[str, Any]:
        """
        get_balance gets the balance of the given address

        Args:
            addr (str): The account address in base58 format string

        Returns:
            Dict[str, Any]: The response
        """
        return self.get(f"/balance/{addr}")
