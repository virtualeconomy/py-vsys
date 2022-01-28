"""
atomic_swap_ctrt contains Atomic Swap contract.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import account as acnt

from py_v_sdk import data_entry as de
from py_v_sdk import tx_req as tx
from py_v_sdk import model as md
from . import CtrtMeta, Ctrt


class AtomicSwapCtrt(Ctrt):
    """
    AtomicSwapCtrt is the class for VSYS Atomic Swap contract.
    """

    CTRT_META = CtrtMeta.from_b58_str(
        "4CrYZXauEHTHvUcNbU2qxvYSgdxPkSBum4PAUfytuZu7Nn56L59op72uKJUBMnF8dk8dLb5k63M9236s8S2yH4FTeWFP4zjfpkx9HGwjAuh6n6WJyxWE1S5HHH2cQLy4xk5B4iMpQKyHQwrQDn3zWwQQPsrfnwaHX1F3V2zKHKx15QYATS784BGfz9NeY72Ntdz2Cgsf6MLQE1YKdgdRfpryCwadqs5xchALCPYLNg6ECSxzPDa4XdS8ywTWzRpiajTGZA1z9YoQZiUMYBwM8S2G4ttZJkgrWTqpXuxberLv3CWZm7kp8bwvg577p8kJ7zAugTgaBU9vzSRFzi3fWtGEP1TPuMCjLSQfskepjoLXbPHyVMmvLZGbjx2AwCyGikdXBdLJWhheL6rnveiXJQfV6zfgF9zeMTpg9GE5SRstGHFetCZwfe3qCPV6vUWrobmWusQ9rDkj5uUXVpjwmBseynCnKNS1CZKDnBDy6mWBDPHNCtuDdYCamqaSEh1nx9ykk4vVJggzPJR8awFMHh5iKPRL9LGhuqbqs4rDPVsg7BCrdaszTGEBEHjfqF51K8PF9kUnPQJvGkf58MrLj2SAArizmZYcnpGMwdfYqGxrjz7xaJGZVAqvFbWFDk3x18ozp58PwFM1fdAn1dn15fKCsiQoqZBtVTxSd4GRJ2tFvBzgUJjig6hqhHqCqobCbpes8LoTdtDCHE5Co3YBnrYN19vbESu2W6LMpwrPPgd1YUeHx8AxR9evasFYrCjmnvBkEyefu5n66yTPYNXfjAk646dHmWYJiUPp1oWDXMjfDJ4xif4BXhRwBtfwgHoDhU2dMV6E7cPVppXxeVL2UsFCbqsafpNcDmhsrGEDAWmxJ3V8KymyuNugM1CHTEiwcTb7GXd4dD3UznDVoJEVrmBveETvCuGVNfGZ4zGZnURyoJHzMkDKPWFQhqgVYLoRuLg4MtquRAaSEKixtXiSJZFKZvQTzMbJC2ie3bnyQoX3x2C9pPpzp3uFKc1eGpgafgi8KoyiqiCMJvfzi8v8DiyTZ9QPENAtwToUpf6vsn1C4HhDzGb9otfigtVuh9JuzsZkJbd4r2rU8sUcKWZcaLF1uX4EdZiEfiW3aV5cm1L7oEJX2w4rQbNiFZWGUpS31WS6mYtWkSTnQupp7rggs8sQxcdWK8WamLgonF4mhXkY12Y2U9AXDJifMKr7mzxiFxZumPWxGn8A1PtTp34wcuhykNMesekwDgWGRCWca9w3YDkeinoD2QmV5ivF2GfHTKhCVH5pkGmBZczeVMA2ZTWb5DTM5qQA9vRy43aJipwmYH73ssbdF7N96678x4hsdcFXXJooRbDtuEY9UkhFPtFMjzD7D5uvXzN4qTPFSyoumwH3ag6cmZMxxQdHNJAm7vitgDpRy3HM174KpjE7uUQXtVvMKEYeAWus24vwW6M4i7APsVg6FeJTgGJJHAHFJFJ4YrZ1fmzgGFnugfp9g4hMuo9G76dzzkZetLhweJCggXBRVpNeRzQ9xmtuDN3wmiyQ1bLSx2ZtNcmWqzbSDsUnCezXtbF4CURyp2djUKo2DRza78CHpmUgHHVai8JrAxPwS6gB8mBg"
    )

    class FuncIdx(Ctrt.FuncIdx):
        """
        FuncIdx is the enum class for function indexes of a contract.
        """

        LOCK = 0
        SOLVE_PUZZLE = 1
        EXPIRE_WITHDRAW = 2

    class StateVar(Ctrt.StateVar):
        """
        StateVar is the enum class for state variables of a contract.
        """

        MAKER = 0
        TOKEN_ID = 1

    class DBKey(Ctrt.DBKey):
        """
        DBKey is the class for DB key of a contract used to query data.
        """

        @classmethod
        def for_maker(cls) -> AtomicSwapCtrt.DBKey:
            """
            for_maker returns the AtomicSwapCtrt.DBKey object for querying the maker.

            Returns:
                AtomicSwapCtrt.DBKey: The AtomicSwapCtrt.DBKey object.
            """
            b = AtomicSwapCtrt.StateVar.MAKER.serialize()
            return cls(b)

        @classmethod
        def for_token_id(cls) -> AtomicSwapCtrt.DBKey:
            """
            for_token_id returns the AtomicSwapCtrt.DBKey object for querying the token_id.

            Returns:
                AtomicSwapCtrt.DBKey: The AtomicSwapCtrt.DBKey object.
            """
            b = AtomicSwapCtrt.StateVar.TOKEN_ID.serialize()
            return cls(b)

        @classmethod
        def for_token_balance(cls, addr: str) -> AtomicSwapCtrt.DBKey:
            """
            for_token_balance [summary]

            Args:
                addr (str): [description]

            Returns:
                AtomicSwapCtrt.DBKey: [description]
            """
            b = AtomicSwapCtrt.StateMap(
                idx=0,
                data_entry=de.Addr(md.Addr(addr)),
            ).serialize()
            return cls(b)

    @classmethod
    async def register(
        cls,
        by: acnt.Account,
        tok_id: str,
        description: str = "",
        fee: int = md.RegCtrtFee.DEFAULT,
    ) -> AtomicSwapCtrt:
        """
        register registers an Atomic Swap Contract

        Args:
            by (acnt.Account): The action taker.
            tok_id (str): The id of the token to atomic swap.
            description (str): The description of the action.
            fee (int, optional): The fee to pay for this action. Defaults to md.RegCtrtFee.DEFAULT.

        Returns:
            AtomicSwapCtrt: The AtomicSwapCtrt object of the registered Atomic Swap contract.
        """
        data = await by._register_contract(
            tx.RegCtrtTxReq(
                data_stack=de.DataStack(
                    de.TokenID(md.TokenID(tok_id)),
                ),
                ctrt_meta=cls.CTRT_META,
                timestamp=md.VSYSTimestamp.now(),
                description=md.Str(description),
                fee=md.RegCtrtFee(fee),
            )
        )
        logger.debug(data)

        return cls(
            data["contractId"],
            chain=by.chain,
        )

    @property
    async def maker(self) -> str:
        """
        maker queries & returns the maker of the contract.

        Returns:
            str: The address of the maker of the contract.
        """
        return await self._query_db_key(self.DBKey.for_maker())

    @property
    async def token_id(self) -> str:
        """
        token_id queries & returns the token_id of the contract.

        Returns:
            str: The token_id of the contract.
        """
        return await self._query_db_key(self.DBKey.for_token_id())

    async def get_token_balance(self, addr: str) -> int:
        """
        token_balance queries & returns the balance of the token deposited into the contract.

        Args:
            addr (str): The account address that deposits the token.

        Returns:
            int: The balance of the token.
        """
        return await self._query_db_key(self.DBKey.for_token_balance(addr))
