from __future__ import annotations
from typing import TYPE_CHECKING

from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import account as acnt

from py_v_sdk import data_entry as de
from py_v_sdk import tx_req as tx
from . import CtrtMeta, Ctrt


class AtomicSwapCtrt(Ctrt):
    """
    AtomicSwapCtrt is the class that encapsulates behaviours of the VSYS Atomic Swap Contract
    """

    CTRT_META = CtrtMeta.from_b58_str(
        "4CrYZXauEHTHvUcNbU2qxvYSgdxPkSBum4PAUfytuZu7Nn56L59op72uKJUBMnF8dk8dLb5k63M9236s8S2yH4FTeWFP4zjfpkx9HGwjAuh6n6WJyxWE1S5HHH2cQLy4xk5B4iMpQKyHQwrQDn3zWwQQPsrfnwaHX1F3V2zKHKx15QYATS784BGfz9NeY72Ntdz2Cgsf6MLQE1YKdgdRfpryCwadqs5xchALCPYLNg6ECSxzPDa4XdS8ywTWzRpiajTGZA1z9YoQZiUMYBwM8S2G4ttZJkgrWTqpXuxberLv3CWZm7kp8bwvg577p8kJ7zAugTgaBU9vzSRFzi3fWtGEP1TPuMCjLSQfskepjoLXbPHyVMmvLZGbjx2AwCyGikdXBdLJWhheL6rnveiXJQfV6zfgF9zeMTpg9GE5SRstGHFetCZwfe3qCPV6vUWrobmWusQ9rDkj5uUXVpjwmBseynCnKNS1CZKDnBDy6mWBDPHNCtuDdYCamqaSEh1nx9ykk4vVJggzPJR8awFMHh5iKPRL9LGhuqbqs4rDPVsg7BCrdaszTGEBEHjfqF51K8PF9kUnPQJvGkf58MrLj2SAArizmZYcnpGMwdfYqGxrjz7xaJGZVAqvFbWFDk3x18ozp58PwFM1fdAn1dn15fKCsiQoqZBtVTxSd4GRJ2tFvBzgUJjig6hqhHqCqobCbpes8LoTdtDCHE5Co3YBnrYN19vbESu2W6LMpwrPPgd1YUeHx8AxR9evasFYrCjmnvBkEyefu5n66yTPYNXfjAk646dHmWYJiUPp1oWDXMjfDJ4xif4BXhRwBtfwgHoDhU2dMV6E7cPVppXxeVL2UsFCbqsafpNcDmhsrGEDAWmxJ3V8KymyuNugM1CHTEiwcTb7GXd4dD3UznDVoJEVrmBveETvCuGVNfGZ4zGZnURyoJHzMkDKPWFQhqgVYLoRuLg4MtquRAaSEKixtXiSJZFKZvQTzMbJC2ie3bnyQoX3x2C9pPpzp3uFKc1eGpgafgi8KoyiqiCMJvfzi8v8DiyTZ9QPENAtwToUpf6vsn1C4HhDzGb9otfigtVuh9JuzsZkJbd4r2rU8sUcKWZcaLF1uX4EdZiEfiW3aV5cm1L7oEJX2w4rQbNiFZWGUpS31WS6mYtWkSTnQupp7rggs8sQxcdWK8WamLgonF4mhXkY12Y2U9AXDJifMKr7mzxiFxZumPWxGn8A1PtTp34wcuhykNMesekwDgWGRCWca9w3YDkeinoD2QmV5ivF2GfHTKhCVH5pkGmBZczeVMA2ZTWb5DTM5qQA9vRy43aJipwmYH73ssbdF7N96678x4hsdcFXXJooRbDtuEY9UkhFPtFMjzD7D5uvXzN4qTPFSyoumwH3ag6cmZMxxQdHNJAm7vitgDpRy3HM174KpjE7uUQXtVvMKEYeAWus24vwW6M4i7APsVg6FeJTgGJJHAHFJFJ4YrZ1fmzgGFnugfp9g4hMuo9G76dzzkZetLhweJCggXBRVpNeRzQ9xmtuDN3wmiyQ1bLSx2ZtNcmWqzbSDsUnCezXtbF4CURyp2djUKo2DRza78CHpmUgHHVai8JrAxPwS6gB8mBg"
    )

    class FuncIdx(Ctrt.FuncIdx):
        LOCK = 0
        SOLVE_PUZZLE = 1
        EXPIRE_WITHDRAW = 2

    class StateVar(Ctrt.StateVar):
        MAKER = 0
        TOKEN_ID = 1

    class DBKey(Ctrt.DBKey):
        @classmethod
        def for_maker(cls) -> AtomicSwapCtrt.DBKey:
            b = AtomicSwapCtrt.StateVar.MAKER.serialize()
            return cls(b)

        @classmethod
        def for_token_id(cls) -> AtomicSwapCtrt.DBKey:
            b = AtomicSwapCtrt.StateVar.TOKEN_ID.serialize()
            return cls(b)

    @classmethod
    def register(
        cls, by: acnt.Account, tok_id: str, description: str = ""
    ) -> AtomicSwapCtrt:
        """
        register registers an Atomic Swap Contract

        Args:
            by (acnt.Account): The action taker
            tok_id (str): The id of the token to atomic swap
            description (str): The description of the action

        Returns:
            AtomicSwapCtrt: The representative instance of the registered Atomic Swap Contract
        """
        data = by.register_contract(
            tx.RegCtrtTxReq(
                data_stack=de.DataStack(
                    de.TokenID(tok_id),
                ),
                ctrt_meta=cls.CTRT_META,
                timestamp=de.Timestamp.now(),
                description=description,
            )
        )
        logger.debug(data)

        return cls(
            data["contractId"],
            chain=by.chain,
        )

    @property
    def maker(self) -> str:
        """
        The address of the maker of this contract
        """
        data = self.chain.api.ctrt.get_ctrt_data(
            ctrt_id=self.ctrt_id,
            db_key=self.DBKey.for_maker().b58_str,
        )
        logger.debug(data)
        return data["value"]

    @property
    def token_id(self) -> str:
        """
        The id of the token registered with this contract
        """
        data = self.chain.api.ctrt.get_ctrt_data(
            ctrt_id=self.ctrt_id,
            db_key=self.DBKey.for_token_id().b58_str,
        )
        logger.debug(data)
        return data["value"]
