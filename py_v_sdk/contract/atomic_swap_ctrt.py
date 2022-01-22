"""
atomic_swap_ctrt contains Atomic Swap contract.
"""
from __future__ import annotations
import imp
from typing import TYPE_CHECKING, Dict, Any

from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import account as acnt

from py_v_sdk import data_entry as de
from py_v_sdk import tx_req as tx
from py_v_sdk import model as md
from . import CtrtMeta, Ctrt

from py_v_sdk.utils.crypto.hashes import sha256_hash
import base58

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
    def register(
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
        data = by.register_contract(
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
    def maker(self) -> str:
        """
        maker queries & returns the maker of the contract.

        Returns:
            str: The address of the maker of the contract.
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
        token_id queries & returns the token_id of the contract.

        Returns:
            str: The token_id of the contract.
        """
        data = self.chain.api.ctrt.get_ctrt_data(
            ctrt_id=self.ctrt_id,
            db_key=self.DBKey.for_token_id().b58_str,
        )
        logger.debug(data)
        return data["value"]


    def lock(
        self,
        by: acnt.Account,
        amount: int,
        recipient: str,
        puzzle: str,
        expire_time: int,
        attachment: str= "",
        fee: int = md.ExecCtrtFee.DEFAULT
        ) -> Dict[str, Any]:
        """ transfer tokens from sender to recipient

        Args:
            by (acnt.Account): The action taker
            sender (str): The sender account
            recipient (str): The recipient account
            amount (int): The amount to transfer
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """
        
        puzzle_bytes =  base58.b58encode(sha256_hash(puzzle))
        puzzle_str = "".join(map(chr,puzzle))

        data=by.execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.LOCK,
                data_stack=de.DataStack(
                    de.Amount(md.Int(amount)),
                    de.Addr(md.Addr(recipient)),
                    de.B58Str(md.B58Str(puzzle_str)),
                    de.expire_time(md.VSYSTimestamp(expire_time))
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    def solve(
    self,
    by: acnt.Account,
    tx_id: str,
    key: str,
    attachment: str= "",
    fee: int = md.ExecCtrtFee.DEFAULT
    ) -> Dict[str, Any]:
        """ transfer tokens from sender to recipient

        Args:
            by (acnt.Account): The action taker
            sender (str): The sender account
            recipient (str): The recipient account
            amount (int): The amount to transfer
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """
    
        data=by.execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.LOCK,
                data_stack=de.DataStack(
                    de.Bytes(md.Bytes(tx_id.encode('latin-1'))),
                    de.Bytes(md.Bytes(key.encode('latin-1'))),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    def exp_withdraw(
        self,
        by: acnt.Account,
        tx_id: str,
        attachment: str= "",
        fee: int = md.ExecCtrtFee.DEFAULT
        ) -> Dict[str, Any]:
            """ transfer tokens from sender to recipient

            Args:
                by (acnt.Account): The action taker
                sender (str): The sender account
                recipient (str): The recipient account
                amount (int): The amount to transfer
                attachment (str, optional): The attachment of this action. Defaults to "".
                fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

            Returns:
                Dict[str, Any]: The response returned by the Node API
            """
        
            data=by.execute_contract(
                tx.ExecCtrtFuncTxReq(
                    ctrt_id=self._ctrt_id,
                    func_id=self.FuncIdx.LOCK,
                    data_stack=de.DataStack(
                        de.Bytes(md.Bytes(tx_id.encode('latin-1'))),
                    ),
                    timestamp=md.VSYSTimestamp.now(),
                    attachment=md.Str(attachment),
                    fee=md.ExecCtrtFee(fee),
                )
            )
            logger.debug(data)
            return data

    