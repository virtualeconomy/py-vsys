"""
api contains NodeAPI-related resources.
"""
from __future__ import annotations
import abc
import json
from typing import Any, Dict, Optional

import requests


class NodeAPI:
    """
    NodeAPI is the wrapper class for RESTful APIs exposed by a node in the VSYS chain network.
    """

    def __init__(
        self, host: str, api_key: Optional[str] = None, timeout: Optional[int] = None
    ):
        """
        Args:
            host (str): The host of the node(with the port). E.g. http://veldidina.vos.systems:9928
            api_key (Optional[str], optional): The API key to that node. Defaults to None.
            timeout (Optional[int], optional): The timeout value. Defaults to None.
        """
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
        """
        host returns the host of the NodeAPI.

        Returns:
            str: The host of the NodeAPI.
        """
        return self._host

    @property
    def blocks(self) -> Blocks:
        """
        blocks returns the API group "blocks" of the NodeAPI.

        Returns:
            Blocks: The API group "blocks".
        """
        return self._blocks

    @property
    def node(self) -> Node:
        """
        node returns the API group "node" of the NodeAPI.

        Returns:
            Node: The API group "node".
        """
        return self._node

    @property
    def ctrt(self) -> Contract:
        """
        ctrt returns the API group "contract" of the NodeAPI.

        Returns:
            Contract: The API group "contract".
        """
        return self._ctrt

    @property
    def addr(self) -> Addresses:
        """
        addr returns the API group "addresses" of the NodeAPI.

        Returns:
            Addresses: The API group "addresses".
        """
        return self._addr


class APIGrp(abc.ABC):
    """
    APIGrp is the class for a group of APIs that share the same prefix.
    """

    PREFIX = ""

    def __init__(self, host: str, sess: requests.Session):
        """
        Args:
            host (str): The host of the node(with the port). E.g. http://veldidina.vos.systems:9928
            sess (requests.Session): The HTTP request session.
        """
        self._host = host
        self._sess = sess

    def _make_url(self, edpt: str) -> str:
        """
        _make_url makes the full url based on the given endpoint name.

        Args:
            edpt (str): The endpoint name.

        Returns:
            str: The full url.
        """
        return self._host + self.PREFIX + edpt

    def get(self, edpt: str) -> Dict[str, Any]:
        """
        get calls the given endpoint with HTTP GET.

        Args:
            edpt (str): The endpoint name.

        Returns:
            Dict[str, Any]: The response.
        """
        url = self._make_url(edpt)
        return self._sess.get(url).json()

    def post(self, edpt: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        post calls the given endpoint with HTTP POST with the given payload.

        Args:
            edpt (str): The endpoint name.
            payload (Dict[str, Any]): The payload.

        Returns:
            Dict[str, Any]: The response.
        """
        url = self._make_url(edpt)
        return self._sess.post(url, json.dumps(payload)).json()


class Blocks(APIGrp):
    """
    Blocks is the API group "blocks"
    """

    PREFIX = "/blocks"

    def get_height(self) -> Dict[str, Any]:
        """
        get_height gets the height of the last block.

        Returns:
            Dict[str, Any]: The response.
        """
        return self.get("/height")

    def get_last_block(self) -> Dict[str, Any]:
        """
        get_last_block gets the last block of the chain.

        Returns:
            Dict[str, Any]: The response.
        """
        return self.get("/last")


class Node(APIGrp):
    """
    Node is the API group "node".
    """

    PREFIX = "/node"

    def get_status(self) -> Dict[str, Any]:
        """
        get_status gets the status of the node.

        Returns:
            Dict[str, Any]: The response.
        """
        return self.get("/status")

    def get_version(self) -> Dict[str, Any]:
        """
        get_version gets the version of the node.

        Returns:
            Dict[str, Any]: The response.
        """
        return self.get("/version")


class Contract(APIGrp):
    """
    Contract is the API group "contract"
    """

    PREFIX = "/contract"

    def broadcast_register(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        broadcast_register broadcasts the register contract request.

        Args:
            payload (Dict[str, Any]): The payload to broadcast.

        Returns:
            Dict[str, Any]: The response.
        """
        return self.post("/broadcast/register", payload)

    def broadcast_execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        broadcast_execute broadcasts the execute contract request.

        Args:
            payload (Dict[str, Any]): The payload to broadcast.

        Returns:
            Dict[str, Any]: The response.
        """
        return self.post("/broadcast/execute", payload)

    def get_ctrt_data(self, ctrt_id: str, db_key: str) -> Dict[str, Any]:
        """
        get_ctrt_data gets the data of a contract with the given DB key.

        Args:
            ctrt_id (str): The contract ID.
            db_key (str): The DB key.

        Returns:
            Dict[str, Any]: The response.
        """
        return self.get(f"/data/{ctrt_id}/{db_key}")


class Addresses(APIGrp):
    """
    Addresses is the API group "addresses".
    """

    PREFIX = "/addresses"

    def get_addr(self, pub_key: str) -> Dict[str, Any]:
        """
        get_addr gets the address from the public key.

        Args:
            pub_key (str): The public key in base58 string format.

        Returns:
            Dict[str, Any]: The response.
        """
        return self.get(f"/publicKey/{pub_key}")

    def get_balance(self, addr: str) -> Dict[str, Any]:
        """
        get_balance gets the balance of the given address.

        Args:
            addr (str): The account address in base58 string format.

        Returns:
            Dict[str, Any]: The response.
        """
        return self.get(f"/balance/{addr}")
