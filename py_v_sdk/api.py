"""
api contains NodeAPI-related resources.
"""
from __future__ import annotations
import abc
import json
from typing import Any, Dict, Optional

import aiohttp


class NodeAPI:
    """
    NodeAPI is the wrapper class for RESTful APIs exposed by a node in the VSYS chain network.
    """

    def __init__(self, sess: aiohttp.ClientSession):
        self._sess = sess
        self._blocks = Blocks(sess)
        self._node = Node(sess)
        self._tx = Transactions(sess)
        self._utils = Utils(sess)
        self._ctrt = Contract(sess)
        self._addr = Addresses(sess)
        self._vsys = VSYS(sess)

    @classmethod
    async def new(
        cls, host: str, api_key: Optional[str] = None, timeout: Optional[float] = None
    ) -> NodeAPI:
        """
        Args:
            host (str): The host of the node(with the port). E.g. http://veldidina.vos.systems:9928
            api_key (Optional[str], optional): The API key to that node. Defaults to None.
            timeout (Optional[float], optional): The timeout value in seconds. Defaults to None.
        """
        headers: Dict[str, str] = {"Content-type": "application/json"}

        if api_key:
            headers["api_key"] = api_key

        sess = aiohttp.ClientSession(
            base_url=host,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=timeout),
        )
        return cls(sess)

    @property
    def sess(self) -> aiohttp.ClientSession:
        return self._sess

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
    def tx(self) -> Transactions:
        """
        tx returns the API group "tx" of the NodeAPI.

        Returns:
            Transactions: The API group "transactions".
        """
        return self._tx

    @property
    def utils(self) -> Utils:
        """
        utils return the API group "utils" of the NodeAPI.

        Returns:
            Utils: The API group "utils".
        """
        return self._utils

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

    @property
    def vsys(self) -> VSYS:
        """
        vsys returns the API group "vsys" of the NodeAPI.

        Returns:
            VSYS: The API group "vsys".
        """
        return self._vsys


class APIGrp(abc.ABC):
    """
    APIGrp is the class for a group of APIs that share the same prefix.
    """

    PREFIX = ""

    def __init__(self, sess: aiohttp.ClientSession):
        """
        Args:
            sess (aiohttp.ClientSession): The HTTP request session.
        """
        self._sess = sess

    def _make_url(self, edpt: str) -> str:
        """
        _make_url makes the full url based on the given endpoint name.

        Args:
            edpt (str): The endpoint name.

        Returns:
            str: The full url.
        """
        return self.PREFIX + edpt

    async def _get(self, edpt: str) -> Dict[str, Any]:
        """
        get calls the given endpoint with HTTP GET.

        Args:
            edpt (str): The endpoint name.

        Returns:
            Dict[str, Any]: The response.
        """
        url = self._make_url(edpt)

        async with self._sess.get(url) as resp:
            return await resp.json()

    async def _post(self, edpt: str, data: str) -> Dict[str, Any]:
        """
        post calls the given endpoint with HTTP POST with the given data.

        Args:
            edpt (str): The endpoint name.
            data (str): The payload. Either a JSON string or a plain text string.

        Returns:
            Dict[str, Any]: The response.
        """
        url = self._make_url(edpt)

        async with self._sess.post(url, data=data) as resp:
            return await resp.json()


class Blocks(APIGrp):
    """
    Blocks is the API group "blocks"
    """

    PREFIX = "/blocks"

    async def get_height(self) -> Dict[str, Any]:
        """
        get_height gets the height of the last block.

        Returns:
            Dict[str, Any]: The response.
        """
        return await self._get("/height")

    async def get_last(self) -> Dict[str, Any]:
        """
        get_last gets the last block of the chain.

        Returns:
            Dict[str, Any]: The response.
        """
        return await self._get("/last")


class Utils(APIGrp):

    PREFIX = "/utils"

    async def hash_fast(self, data: str) -> Dict[str, Any]:
        return await self._post("/hash/fast", data)


class Node(APIGrp):
    """
    Node is the API group "node".
    """

    PREFIX = "/node"

    async def get_status(self) -> Dict[str, Any]:
        """
        get_status gets the status of the node.

        Returns:
            Dict[str, Any]: The response.
        """
        return await self._get("/status")

    async def get_version(self) -> Dict[str, Any]:
        """
        get_version gets the version of the node.

        Returns:
            Dict[str, Any]: The response.
        """
        return await self._get("/version")


class Transactions(APIGrp):
    """
    Transactions is the API group "transactions".
    """

    PREFIX = "/transactions"

    async def get_info(self, tx_id: str) -> Dict[str, Any]:
        """
        get_info gets the information about a transaction.

        Args:
            tx_id (str): The transaction ID.

        Returns:
            Dict[str, Any]: The response.
        """
        return await self._get(f"/info/{tx_id}")


class Contract(APIGrp):
    """
    Contract is the API group "contract"
    """

    PREFIX = "/contract"

    async def get_tok_id(self, ctrt_id: str, tok_idx: int) -> Dict[str, Any]:
        """
        get_tok_id gets the token ID of the given contract with the given token index.

        Args:
            ctrt_id (str): The contract ID.
            tok_idx (int): The token index.

        Returns:
            Dict[str, Any]: The response.
        """
        return await self._get(f"/contractId/{ctrt_id}/tokenIndex/{tok_idx}")

    async def broadcast_register(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        broadcast_register broadcasts the register contract request.

        Args:
            data (Dict[str, Any]): The payload for the API call.

        Returns:
            Dict[str, Any]: The response.
        """
        return await self._post("/broadcast/register", json.dumps(data))

    async def broadcast_execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        broadcast_execute broadcasts the execute contract request.

        Args:
            data (Dict[str, Any]): The payload for the API call.

        Returns:
            Dict[str, Any]: The response.
        """
        return await self._post("/broadcast/execute", json.dumps(data))

    async def get_ctrt_data(self, ctrt_id: str, db_key: str) -> Dict[str, Any]:
        """
        get_ctrt_data gets the data of a contract with the given DB key.

        Args:
            ctrt_id (str): The contract ID.
            db_key (str): The DB key.

        Returns:
            Dict[str, Any]: The response.
        """
        return await self._get(f"/data/{ctrt_id}/{db_key}")

    async def get_tok_balance(self, addr: str, tok_id: str) -> Dict[str, Any]:
        """
        get_tok_balance gets the balance of the token for the account address.

        Args:
            addr (str): The account address.
            tok_id (str): The token ID.

        Returns:
            Dict[str, Any]: The response.
        """
        return await self._get(f"/balance/{addr}/{tok_id}")


class Addresses(APIGrp):
    """
    Addresses is the API group "addresses".
    """

    PREFIX = "/addresses"

    async def get_addr(self, pub_key: str) -> Dict[str, Any]:
        """
        get_addr gets the address from the public key.

        Args:
            pub_key (str): The public key in base58 string format.

        Returns:
            Dict[str, Any]: The response.
        """
        return await self._get(f"/publicKey/{pub_key}")

    async def get_balance(self, addr: str) -> Dict[str, Any]:
        """
        get_balance gets the balance of the given address.

        Args:
            addr (str): The account address in base58 string format.

        Returns:
            Dict[str, Any]: The response.
        """
        return await self._get(f"/balance/{addr}")


class VSYS(APIGrp):
    """
    VSYS is the API group "vsys"
    """

    PREFIX = "/vsys"

    async def broadcast_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        broadcast_payment broadcasts the request for payment of VSYS coins.

        Args:
            data (Dict[str, Any]): The payload for the API call.

        Returns:
            Dict[str, Any]: The response.
        """
        return await self._post("/broadcast/payment", json.dumps(data))

    async def payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        payment makes the payment of VSYS coins for one of the built-in account of the node (API Key required).

        Args:
            data (Dict[str, Any]): The payload for the API call.

        Returns:
            Dict[str, Any]: The response.
        """
        return await self._post("/payment", json.dumps(data))
