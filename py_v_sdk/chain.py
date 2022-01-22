"""
chain contains chain-related resources.
"""
from __future__ import annotations
import enum
from typing import Dict, Any, TYPE_CHECKING

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import api


class ChainID(enum.Enum):
    """
    ChainID is the enum class for chain ID.
    """

    MAIN_NET = "M"
    TEST_NET = "T"


class Chain:
    """
    Chain is the class for the narrowly-defined chain.
    It contains handy methods for querying chain-related data(e.g. height, last block, etc).
    """

    def __init__(self, node_api: api.NodeAPI, chain_id: ChainID = ChainID.TEST_NET):
        """
        Args:
            node_api (api.NodeAPI): The NodeAPI object the chain uses.
            chain_id (ChainID, optional): The chain's ID. Defaults to ChainID.TEST_NET.
        """
        self._api = node_api
        self._chain_id = chain_id

    @property
    def api(self) -> api.NodeAPI:
        """
        api returns the NodeAPI object that the chain uses.

        Returns:
            api.NodeAPI: The NodeAPI object that the chain uses.
        """
        return self._api

    @property
    def chain_id(self) -> ChainID:
        """
        chain_id returns the ID of the chain.

        Returns:
            ChainID: ID of the chain.
        """
        return self._chain_id

    @property
    async def height(self) -> int:
        """
        height queries & returns the height of the chain.

        Returns:
            int: The height of the chain.
        """
        return await self.api.blocks.get_height()["height"]

    @property
    async def last_block(self) -> Dict[str, Any]:
        """
        last_block queries & returns the last_block of the chain.

        Returns:
            Dict[str, Any]: The last block data of the chain.
        """
        return await self.api.blocks.get_last()
