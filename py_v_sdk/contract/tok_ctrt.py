"""
tok_ctrt contains Token contract.
"""
from __future__ import annotations

from typing import Dict, Any, TYPE_CHECKING, Union

from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import account as acnt
    from py_v_sdk import chain as ch
from py_v_sdk import data_entry as de
from py_v_sdk import tx_req as tx
from py_v_sdk import model as md

from . import CtrtMeta, Ctrt


class TokenCtrtWithoutSplit(Ctrt):
    """
    TokenCtrtWithoutSplit is the class that encapsulates behaviours of the VSYS TOKEN contract without split v1.
    """

    CTRT_META = CtrtMeta.from_b58_str(
        "3GQnJtxDQc3zFuUwXKbrev1TL7VGxk5XNZ7kUveKK6BsneC1zTSTRjgBTdDrksHtVMv6nwy9Wy6MHRgydAJgEegDmL4yx7tdNjdnU38b8FrCzFhA1aRNxhEC3ez7JCi3a5dgVPr93hS96XmSDnHYvyiCuL6dggahs2hKXjdz4SGgyiUUP4246xnELkjhuCF4KqRncUDcZyWQA8UrfNCNSt9MRKTj89sKsV1hbcGaTcX2qqqSU841HyokLcoQSgmaP3uBBMdgSYVtovPLEFmpXFMoHWXAxQZDaEtZcHPkrhJyG6CdTgkNLUQKWtQdYzjxCc9AsUGMJvWrxWMi6RQpcqYk3aszbEyAh4r4fcszHHAJg64ovDgMNUDnWQWJerm5CjvN76J2MVN6FqQkS9YrM3FoHFTj1weiRbtuTc3mCR4iMcu2eoxcGYRmUHxKiRoZcWnWMX2mzDw31SbvHqqRbF3t44kouJznTyJM6z1ruiyQW6LfFZuV6VxsKLX3KQ46SxNsaJoUpvaXmVj2hULoGKHpwPrTVzVpzKvYQJmz19vXeZiqQ2J3tVcSFH17ahSzwRkXYJ5HP655FHqTr6Vvt8pBt8N5vixJdYtfx7igfKX4aViHgWkreAqBK3trH4VGJ36e28RJP8Xrt6NYG2icsHsoERqHik7GdjPAmXpnffDL6P7NBfyKWtp9g9C289TDGUykS8CNiW9L4sbUabdrqsdkdPRjJHzzrb2gKTf2vB56rZmreTUbJ53KsvpZht5bixZ59VbCNZaHfZyprvzzhyTAudAmhp8Nrks7SV1wTySZdmfLyw7vsNmTEi3hmuPmYqExp4PoLPUwT4TYt2doYUX1ds3CesnRSjFqMhXnLmTgYXsAXvvT2E6PWTY5nPCycQv5pozvQuw1onFtGwY9n5s2VFjxS9W6FkCiqyyZAhCXP5o44wkmD5SVqyqoL5HmgNc8SJL7uMMMDDwecy7Sh9vvt3RXirH7F7bpUv3VsaepVGCHLfDp9GMG59ZiWK9Rmzf66e8Tw4unphu7gFNZuqeBk2YjCBj3i4eXbJvBEgCRB51FATRQY9JUzdMv9Mbkaq4DW69AgdqbES8aHeoax1UDDBi3raM8WpP2cKVEqoeeCGYM2vfN6zBAh7Tu3M4NcNFJmkNtd8Mpc2Md1kxRsusVzHiYxnsZjo"
    )

    def __init__(self, ctrt_id: str, chain: ch.Chain, unit: int) -> None:
        self._ctrt_id = md.CtrtID(ctrt_id)
        self._chain = chain
        self._unit = md.Int(unit)

    @property
    def get_unit(self) -> int:
        """
        get_unit returns the unit in int format.

        Returns:
            int: The unit in integer format.
        """
        return self._unit.data

    class FuncIdx(Ctrt.FuncIdx):
        SUPERSEDE = 0
        ISSUE = 1
        DESTROY = 2
        SEND = 3
        TRANSFER = 4
        DEPOSIT = 5
        WITHDRAW = 6
        TOTAL_SUPPLY = 7
        MAX_SUPPLY = 8
        BALANCE_OF = 9
        GET_ISSUER = 10

    class StateVar(Ctrt.StateVar):
        """
        StateVar is the enum class for state variables of a contract.
        """

        ISSUER = 0
        MAKER = 1

    class DBKey(Ctrt.DBKey):
        """
        DBKey is the class for DB key of a contract used to query data.
        """

        @classmethod
        def for_issuer(cls) -> TokenCtrtWithoutSplit.DBKey:
            b = TokenCtrtWithoutSplit.StateVar.ISSUER.serialize()
            return cls(b)

        @classmethod
        def for_maker(cls) -> TokenCtrtWithoutSplit.DBKey:
            b = TokenCtrtWithoutSplit.StateVar.MAKER.serialize()
            return cls(b)

    @classmethod
    async def register(
        cls,
        by: acnt.Account,
        max: Union[int, float],
        unit: int,
        token_description: str = "",
        ctrt_description: str = "",
        fee: int = md.RegCtrtFee.DEFAULT,
    ) -> TokenCtrtWithoutSplit:
        """
        register registers a token contract without split

        Args:
            by (acnt.Account): The action taker
            max (int): The max amount that can be issued
            unit (int): The granularity of splitting a token
            token_description (str): The description of the token
            ctrt_description (str, optional): The description of the contract. Defaults to "".
            fee (int, optional):  Register fee. Defaults to md.RegCtrtFee.DEFAULT.

        Returns:
            TokenCtrtWithoutSplit: A token contract without split
        """

        data = await by._register_contract(
            tx.RegCtrtTxReq(
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(max, unit),
                    de.Amount(md.Int(unit)),
                    de.String(md.Str(token_description)),
                ),
                ctrt_meta=cls.CTRT_META,
                timestamp=md.VSYSTimestamp.now(),
                description=md.Str(ctrt_description),
                fee=md.RegCtrtFee(fee),
            )
        )
        logger.debug(data)
        print(data)

        return cls(
            data["contractId"],
            chain=by.chain,
            unit=unit,
        )

    @property
    async def issuer(self) -> str:
        """
        issuer queries & returns the issuer of the contract.
        Returns:
            str: The address of the issuer of the contract.
        """

        data = await self.chain.api.ctrt.get_ctrt_data(
            ctrt_id=self.ctrt_id,
            db_key=self.DBKey.for_issuer().b58_str,
        )
        logger.debug(data)
        return data["value"]

    @property
    async def maker(self) -> str:
        """
        maker queries & returns the maker of the contract.
        Returns:
            str: The address of the maker of the contract.
        """

        data = await self.chain.api.ctrt.get_ctrt_data(
            ctrt_id=self.ctrt_id,
            db_key=self.DBKey.for_maker().b58_str,
        )
        logger.debug(data)
        return data["value"]

    @property
    async def tok_id(self) -> str:
        """
        TODO: tok_id can be computed locally.

        tok_id queries & returns the token ID of the contract.

        Returns:
            str: The token ID.
        """
        data = await self.chain.api.ctrt.get_tok_id(self.ctrt_id, 0)
        return data["tokenId"]

    async def get_tok_bal(self, addr: str) -> int:
        """
        get_tok_bal queries & returns the balance of the token of the contract belonging to the user address.

        Args:
            addr (str): The user address.

        Returns:
            int: The balance.
        """
        tok_id = await self.tok_id
        data = await self.chain.api.ctrt.get_tok_bal(addr, tok_id)
        return data["balance"]

    async def supersede(
        self,
        by: acnt.Account,
        new_issuer: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, any]:
        """
        supersede transfers the issuing right of the contract to another account

        Args:
            by (acnt.Account): The action taker
            new_issuer (int): The new issuer of the contract
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str,any]: The response returned by the Node API
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SUPERSEDE,
                data_stack=de.DataStack(de.Addr(md.Addr(new_issuer))),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def issue(
        self,
        by: acnt.Account,
        amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, any]:
        """
        issue issues new Tokens by account who has the issuing right

        Args:
            by (acnt.Account): The action taker
            amount (Union[int, float]): The amount of token will be issued
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str,any]: The response returned by the Node API
        """
        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.ISSUE,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount, self.get_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def send(
        self,
        by: acnt.Account,
        recipient: str,
        amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        send sends tokens to another account

        Args:
            by (acnt.Account): The action taker
            recipient (str): The recipient account
            amount (Union[int, float]): The amount of token to be sent
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        rcpt_md = md.Addr(recipient)
        rcpt_md.must_on(by.chain)

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SEND,
                data_stack=de.DataStack(
                    de.Addr(rcpt_md),
                    de.Amount.for_tok_amount(amount, self.get_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def destroy(
        self,
        by: acnt.Account,
        amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        destroy destroys an amount of tokens by account who has the issuing right

        Args:
            by (acnt.Account): The action taker
            amount (Union[int, float]): The amount of token to be destroyed
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.DESTROY,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount, self.get_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def transfer(
        self,
        by: acnt.Account,
        sender: str,
        recipient: str,
        amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        transfer transfers tokens from sender to recipient

        Args:
            by (acnt.Account): The action taker
            sender (str): The sender account
            recipient (str): The recipient account
            amount (Union[int, float]): The amount to transfer
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        sender_md = md.Addr(sender)
        rcpt_md = md.Addr(recipient)

        sender_md.must_on(by.chain)
        rcpt_md.must_on(by.chain)

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.TRANSFER,
                data_stack=de.DataStack(
                    de.Addr(sender_md),
                    de.Addr(rcpt_md),
                    de.Amount.for_tok_amount(amount, self.get_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def deposit(
        self,
        by: acnt.Account,
        contract: str,
        amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        deposit deposits the tokens into the contract

        Args:
            by (acnt.Account): The action maker.
            contract (str): The contract id to deposit into
            amount (Union[int, float]): The amount to deposit
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        sender_md = md.Addr(by.addr.b58_str)
        sender_md.must_on(by.chain)

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.DEPOSIT,
                data_stack=de.DataStack(
                    de.Addr(sender_md),
                    de.CtrtAcnt(md.CtrtID(contract)),
                    de.Amount.for_tok_amount(amount, self.get_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def withdraw(
        self,
        by: acnt.Account,
        contract: str,
        amount: Union[int, float],
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        withdraw withdraws tokens from another contract

        Args:
            by (acnt.Account): The action maker.
            contract (str): The contract id that you want to withdraw token from
            amount (Union[int, float]): The amount to withdraw
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        rcpt_md = md.Addr(by.addr.b58_str)
        rcpt_md.must_on(by.chain)

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.WITHDRAW,
                data_stack=de.DataStack(
                    de.CtrtAcnt(md.CtrtID(contract)),
                    de.Addr(rcpt_md),
                    de.Amount.for_tok_amount(amount, self.get_unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data


class TokenCtrtWithSplit(TokenCtrtWithoutSplit):

    CTRT_META = CtrtMeta.from_b58_str(
        "3dPGAWbTw4srh5hmMiRUhHtcxmXXLUooKGAfnmz11j5NruyJpBzZpgvADMdZS7Mevy5MAHqFbfHYdfqaAe1JEpLWt1pJWLHZBV62zUhLGmVLXUP5UDvSs24jsBRHqZMC71ciE1uYtgydKxCoFJ3rAgsYqp7GDeTU2PXS5ygDmL6WXmbAYPS8jE4sfNUbJVwpvL1cTw4nnjnJvmLET8VmQybxFt415RemV3MFPeYZay5i5gMmyZa63bjzK1uMZAVWA9TpF5YQ1NTZjPaRPvQGYVY4kY9L4LFJvUG2bib1QaNh7wUAQnTzJfRYJoy1aegFGFZFnBGp9GugH4fHAY69vGmZQnhDw3jU45G9odFyXo3T5Ww4R5szegbjCUKdUGpXf9vY2cKEMJ7i8eCkFVG1dDFZeVov1KMjkVNV8rDBDYfcp3oSGNWQQvGSUT5iGUvDRN8phy1UpR3A9uMVebvjLnVzPx9RyqQ8HaXLM8vPhLuWLoh5hk1Zi1n9nwz55XvKDYjP6eeB55yK5vpg8xjaYDnw9bjYV7ZmS7LAsHvXfnwi8y2W6vk2hGvs4rtR1vNRZSQMPGRRSuwCRJL1yngH6uHWwm2ajWxc684jApuoLdyjZomfCtdpabSyU3kp9Lrn8zT8BVY332sJPQU6gTQi8ke9s9dBxCae4cfSQM6HhuBmFc5KKWHCVG4bm4KZRYbMtidw8ZZnjaAMtcGq7k3Se6GXaTxdS3GcuttB3VB7njypyzuqAcfCdYb9ht8Y1WuTCZ1aLsXsL6eydfk2WLJVrqYpbTk6AchV5gMAEopvc3qXvzrDCedjtNsDmA56Lh6PxrrKr8aV8Wzz8aMaQ88YsVBpE8J4cDkxzo31AojhzEGVBKLmpb3bjmsaw9VkpB6yL8ngYs8eJMSPdM289TSMaEmG4eHt1jezpHTKxkuB9cwqcvhGNLWuv8KXQkik5pRMXV67Qs2FvjpzeJ81z2hnVh1wCtsa6M6qAG1gsqLHa1AVMRzsowafC99uDexwWMBS2RqsZWZBXJcUiNVULjApSnoBREYfHYEpjJ152hnTYZCAwpZMWEkVdBQpZ3zk8gbfLxB4fWMfKgJJucbKPGp1K56u7P8MHQu9aNb9dEof2mwX8rTHjk8jSQ7kXVX4Mf1JqMRWWftkV3GmU1nqYhxRGu4FjDNAomwTr5epHpcMF6P5oiXcLWh5BFQVmGYKz129oizAyUJBsZdxr2WZEGDieLxUg8cve25g28oTuCVENST4z1ZsFAN9wTa1"
    )

    class FuncIdx(Ctrt.FuncIdx):
        SUPERSEDE = 0
        ISSUE = 1
        DESTROY = 2
        SPLIT = 3
        SEND = 4
        TRANSFER = 5
        DEPOSIT = 6
        WITHDRAW = 7
        TOTAL_SUPPLY = 8
        MAX_SUPPLY = 9
        BALANCE_OF = 10
        GET_ISSUER = 11

    async def split(
        self,
        by: acnt.Account,
        new_unit: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        split updates the unit

        Args:
            by (acnt.Account): The action taker
            new_unit (int): The new unit to update
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): Execution fee of this tx. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SPLIT,
                data_stack=de.DataStack(
                    de.INT32(md.Int(new_unit)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data
