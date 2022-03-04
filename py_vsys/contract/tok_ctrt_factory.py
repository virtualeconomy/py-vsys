"""
tok_ctrt_factory contains factory methods to create a token contract(NFT included) instance.
"""
from __future__ import annotations
import enum
from typing import TYPE_CHECKING, Type

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import chain as ch

from py_v_sdk import model as md

from py_v_sdk.contract import nft_ctrt, tok_ctrt, sys_ctrt
from . import BaseTokCtrt


class TokCtrtType(enum.Enum):
    """
    TokCtrtType is the enum class for token contract(NFT included) types.
    The string value of each enum item is the contract type returned from the node.
    """

    NFT = "NonFungibleContract"
    NFT_V2_BLACKLIST = "NFTContractWithBlacklist"
    NFT_V2_WHITELIST = "NFTContractWithWhitelist"

    TOK_NO_SPLIT = "TokenContract"
    TOK_WITH_SPLIT = "TokenContractWithSplit"
    TOK_V2_WHITELIST = "TokenContractWithWhitelist"
    TOK_V2_BLACKLIST = "TokenContractWithBlacklist"


class TokCtrtMap:
    """
    TokCtrtMap is the map between the TokCtrtType & corresponding token contract classes.
    """

    MAP = {
        TokCtrtType.NFT: nft_ctrt.NFTCtrt,
        TokCtrtType.NFT_V2_BLACKLIST: nft_ctrt.NFTCtrtV2Blacklist,
        TokCtrtType.NFT_V2_WHITELIST: nft_ctrt.NFTCtrtV2Whitelist,
        TokCtrtType.TOK_NO_SPLIT: tok_ctrt.TokCtrtWithoutSplit,
        TokCtrtType.TOK_WITH_SPLIT: tok_ctrt.TokCtrtWithSplit,
        TokCtrtType.TOK_V2_WHITELIST: tok_ctrt.TokCtrtWithoutSplitV2Whitelist,
        TokCtrtType.TOK_V2_BLACKLIST: tok_ctrt.TokCtrtWithoutSplitV2Blacklist,
    }

    @classmethod
    def get_tok_ctrt_cls(cls, tok_ctrt_type: TokCtrtType) -> Type[BaseTokCtrt]:
        return cls.MAP[tok_ctrt_type]


async def from_tok_id(tok_id: md.TokenID, chain: ch.Chain) -> BaseTokCtrt:
    """
    from_tok_id creates a token contract instance based on the given token ID

    Args:
        tok_id (md.TokenID): The token ID.
        chain (ch.Chain): The chain object.

    Returns:
        BaseTokCtrt: The token contract instance.
    """
    if tok_id.is_mainnet_vsys_tok:
        return sys_ctrt.SysCtrt.for_mainnet(chain)
    if tok_id.is_testnet_vsys_tok:
        return sys_ctrt.SysCtrt.for_testnet(chain)

    tok_info = await chain.api.ctrt.get_tok_info(tok_id.data)
    ctrt_id = tok_info["contractId"]

    ctrt_info = await chain.api.ctrt.get_ctrt_info(ctrt_id)

    type = TokCtrtType(ctrt_info["type"])

    cls = TokCtrtMap.get_tok_ctrt_cls(type)
    return cls(ctrt_id, chain)
