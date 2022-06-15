"""
chain contains chain-related resources.
"""
from __future__ import annotations
import enum
from typing import Dict, Any, TYPE_CHECKING, List

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_vsys import api


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

    def __init__(self, node_api: api.NodeAPI, chain_id: ChainID):
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
        resp = await self.api.blocks.get_height()
        return resp["height"]

    @property
    async def last_block(self) -> Dict[str, Any]:
        """
        last_block queries & returns the last_block of the chain.

        Returns:
            Dict[str, Any]: The last block data of the chain.
        """
        return await self.api.blocks.get_last()

    async def get_block_at(self, height: int) -> Dict[str, Any]:
        """
        get_block_at gets the block at the given height.

        Args:
            height (int): The height of the block.

        Returns:
            Dict[str, Any]: The block.
        """
        return await self.api.blocks.get_block_at(height)

    async def get_blocks_within(
        self, start_height: int, end_height: int
    ) -> List[Dict[str, Any]]:
        """
        get_blocks_within gets blocks fall in the given range.

        NOTE that the max length of the range is 100.

        Args:
            start_height (int): The start height.
            end_height (int): The end height.

        Returns:
            List[Dict[str, Any]]: The blocks.
        """
        return await self.api.blocks.get_blocks_within(start_height, end_height)
