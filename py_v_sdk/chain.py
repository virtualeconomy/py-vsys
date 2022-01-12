import enum
from typing import Dict, Any

from py_v_sdk import api


class ChainID(enum.Enum):
    MAIN_NET = "M"
    TEST_NET = "T"


class Chain:
    def __init__(self, api: api.NodeAPI, chain_id: ChainID = ChainID.TEST_NET):
        self._api = api
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
