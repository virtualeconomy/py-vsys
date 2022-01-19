from __future__ import annotations
import enum
from typing import Dict, Any, TYPE_CHECKING

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import api


class ChainID(enum.Enum):
    MAIN_NET = "M"
    TEST_NET = "T"


class Chain:
    def __init__(self, node_api: api.NodeAPI, chain_id: ChainID = ChainID.TEST_NET):
        self._api = node_api
        self._chain_id = chain_id

    @property
    def api(self) -> api.NodeAPI:
        return self._api

    @property
    def chain_id(self) -> ChainID:
        return self._chain_id

    @property
    def height(self) -> int:
        return self.api.blocks.get_height()["height"]

    @property
    def last_block(self) -> Dict[str, Any]:
        return self.api.blocks.get_last_block()
