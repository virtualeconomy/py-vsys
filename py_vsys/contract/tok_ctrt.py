"""
tok_ctrt contains Token contract.
"""
from __future__ import annotations

from typing import Dict, Any, TYPE_CHECKING, Union, Optional

from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_vsys import account as acnt
    from py_vsys import chain as ch

from py_vsys import data_entry as de
from py_vsys import tx_req as tx
from py_vsys import model as md

from . import CtrtMeta, Ctrt, BaseTokCtrt


class TokCtrtWithoutSplit(BaseTokCtrt):
    """
    TokCtrtWithoutSplit is the class that encapsulates behaviours of the VSYS TOKEN contract without split v1.
    """

    CTRT_META = CtrtMeta.from_b58_str(
        "3GQnJtxDQc3zFuUwXKbrev1TL7VGxk5XNZ7kUveKK6BsneC1zTSTRjgBTdDrksHtVMv6nwy9Wy6MHRgydAJgEegDmL4yx7tdNjdnU38b8FrCzFhA1aRNxhEC3ez7JCi3a5dgVPr93hS96XmSDnHYvyiCuL6dggahs2hKXjdz4SGgyiUUP4246xnELkjhuCF4KqRncUDcZyWQA8UrfNCNSt9MRKTj89sKsV1hbcGaTcX2qqqSU841HyokLcoQSgmaP3uBBMdgSYVtovPLEFmpXFMoHWXAxQZDaEtZcHPkrhJyG6CdTgkNLUQKWtQdYzjxCc9AsUGMJvWrxWMi6RQpcqYk3aszbEyAh4r4fcszHHAJg64ovDgMNUDnWQWJerm5CjvN76J2MVN6FqQkS9YrM3FoHFTj1weiRbtuTc3mCR4iMcu2eoxcGYRmUHxKiRoZcWnWMX2mzDw31SbvHqqRbF3t44kouJznTyJM6z1ruiyQW6LfFZuV6VxsKLX3KQ46SxNsaJoUpvaXmVj2hULoGKHpwPrTVzVpzKvYQJmz19vXeZiqQ2J3tVcSFH17ahSzwRkXYJ5HP655FHqTr6Vvt8pBt8N5vixJdYtfx7igfKX4aViHgWkreAqBK3trH4VGJ36e28RJP8Xrt6NYG2icsHsoERqHik7GdjPAmXpnffDL6P7NBfyKWtp9g9C289TDGUykS8CNiW9L4sbUabdrqsdkdPRjJHzzrb2gKTf2vB56rZmreTUbJ53KsvpZht5bixZ59VbCNZaHfZyprvzzhyTAudAmhp8Nrks7SV1wTySZdmfLyw7vsNmTEi3hmuPmYqExp4PoLPUwT4TYt2doYUX1ds3CesnRSjFqMhXnLmTgYXsAXvvT2E6PWTY5nPCycQv5pozvQuw1onFtGwY9n5s2VFjxS9W6FkCiqyyZAhCXP5o44wkmD5SVqyqoL5HmgNc8SJL7uMMMDDwecy7Sh9vvt3RXirH7F7bpUv3VsaepVGCHLfDp9GMG59ZiWK9Rmzf66e8Tw4unphu7gFNZuqeBk2YjCBj3i4eXbJvBEgCRB51FATRQY9JUzdMv9Mbkaq4DW69AgdqbES8aHeoax1UDDBi3raM8WpP2cKVEqoeeCGYM2vfN6zBAh7Tu3M4NcNFJmkNtd8Mpc2Md1kxRsusVzHiYxnsZjo"
    )

    def __init__(self, ctrt_id: str, chain: ch.Chain) -> None:
        """
        Args:
            ctrt_id (str): The contract ID.
            chain (ch.Chain): The Chain object.
        """
        self._ctrt_id = md.CtrtID(ctrt_id)
        self._chain = chain
        self._unit = 0
        self._tok_id: Optional[md.TokenID] = None

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
        def for_issuer(cls) -> TokCtrtWithoutSplit.DBKey:
            b = TokCtrtWithoutSplit.StateVar.ISSUER.serialize()
            return cls(b)

        @classmethod
        def for_maker(cls) -> TokCtrtWithoutSplit.DBKey:
            b = TokCtrtWithoutSplit.StateVar.MAKER.serialize()
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
    ) -> TokCtrtWithoutSplit:
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
            TokCtrtWithoutSplit: A token contract without split
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

        tc = cls(
            data["contractId"],
            chain=by.chain,
        )
        tc._unit = unit
        return tc

    @property
    async def issuer(self) -> md.Addr:
        """
        issuer queries & returns the issuer of the contract.

        Returns:
            md.Addr: The address of the issuer of the contract.
        """

        raw_val = await self._query_db_key(self.DBKey.for_issuer())
        return md.Addr(raw_val)

    @property
    async def maker(self) -> md.Addr:
        """
        maker queries & returns the maker of the contract.

        Returns:
            str: The address of the maker of the contract.
        """

        raw_val = await self._query_db_key(self.DBKey.for_maker())
        return md.Addr(raw_val)

    @property
    def tok_id(self) -> md.TokenID:
        """
        tok_id returns the token ID of the contract.

        Returns:
            md.TokenID: The token ID.
        """
        if not self._tok_id:
            self._tok_id = self.get_tok_id(self.ctrt_id, md.TokenIdx(0))
        return self._tok_id

    @property
    async def unit(self) -> int:
        """
        unit returns the unit in integer format.

        Returns:
            int: The unit in integer format.
        """
        if self._unit <= 0:
            info = await self._chain.api.ctrt.get_tok_info(self.tok_id.data)
            self._unit = info["unity"]
        return self._unit

    async def get_tok_bal(self, addr: str) -> md.Token:
        """
        get_tok_bal queries & returns the balance of the token of the contract belonging to the user address.

        Args:
            addr (str): The user address.

        Returns:
            md.Token: The balance.
        """
        resp = await self.chain.api.ctrt.get_tok_bal(addr, self.tok_id.data)
        raw_val = resp["balance"]
        return md.Token(raw_val, await self.unit)

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
        unit = await self.unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.ISSUE,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount, unit),
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

        unit = await self.unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SEND,
                data_stack=de.DataStack(
                    de.Addr(rcpt_md),
                    de.Amount.for_tok_amount(amount, unit),
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
        unit = await self.unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.DESTROY,
                data_stack=de.DataStack(
                    de.Amount.for_tok_amount(amount, unit),
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

        unit = await self.unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.TRANSFER,
                data_stack=de.DataStack(
                    de.Addr(sender_md),
                    de.Addr(rcpt_md),
                    de.Amount.for_tok_amount(amount, unit),
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

        sender_md = md.Addr(by.addr.data)
        sender_md.must_on(by.chain)

        unit = await self.unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.DEPOSIT,
                data_stack=de.DataStack(
                    de.Addr(sender_md),
                    de.CtrtAcnt(md.CtrtID(contract)),
                    de.Amount.for_tok_amount(amount, unit),
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

        rcpt_md = md.Addr(by.addr.data)
        rcpt_md.must_on(by.chain)

        unit = await self.unit

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.WITHDRAW,
                data_stack=de.DataStack(
                    de.CtrtAcnt(md.CtrtID(contract)),
                    de.Addr(rcpt_md),
                    de.Amount.for_tok_amount(amount, unit),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data


class TokCtrtWithSplit(TokCtrtWithoutSplit):

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

    @classmethod
    async def register(
        cls,
        by: acnt.Account,
        max: Union[int, float],
        unit: int,
        token_description: str = "",
        ctrt_description: str = "",
        fee: int = md.RegCtrtFee.DEFAULT,
    ) -> TokCtrtWithSplit:
        """
        register registers a token contract with split

        Args:
            by (acnt.Account): The action taker
            max (int): The max amount that can be issued
            unit (int): The granularity of splitting a token
            token_description (str): The description of the token
            ctrt_description (str, optional): The description of the contract. Defaults to "".
            fee (int, optional):  Register fee. Defaults to md.RegCtrtFee.DEFAULT.

        Returns:
            TokCtrtWithSplit: A token contract with split
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

        return cls(
            data["contractId"],
            chain=by.chain,
        )

    @property
    async def unit(self) -> int:
        """
        unit returns the unit in integer format.

        Returns:
            int: The unit in integer format.
        """
        info = await self._chain.api.ctrt.get_tok_info(self.tok_id.data)
        self._unit = info["unity"]
        return self._unit

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
                    de.Amount(md.Int(new_unit)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data


class TokCtrtWithoutSplitV2Whitelist(TokCtrtWithoutSplit):

    CTRT_META = CtrtMeta.from_b58_str(
        "7BekqFZ2yZqjiQFFnsxL4CDRFWCjHdZvFXQd6sxAgEktxwn5kkR6vkV27SFC7VmhuMysVfunZWTtHAqPjg4gGz72pha6TMUerSUSXSn7BHaVexyQJoUfqDT5bdr3XVpok1mU2gT29mwtJ6BibizpAEgZZncZauDnvqrWWdkCmRP8VXpPBiPEaUZuq9eRusrUcc5YHshhN6BVkArN84tarVQH3pTRmiekdQveuxFw4r4weXUxwEGCkYX3Zqeqc4mmRsajVCQwV5DuGTEwaBVWiAAfHLGPFgJF6w6aP3d22tdBRLqZ2Y4G5WHdhMunNDEZ2E79w7gbwqDXtz3eVfGtyET5NZEJGmM2S8pZSn2MPjvfPAYZMa9Zd4WXnPLZng1pxjYvrpqPDy27VQu1rhvxXMNPVMdP9QyCQSoExZUot1FmskS1NcmzKfguwsSWR1Z1py58iVDKm8t7x7RnaP7avcjtvixJQkPGg7qaxBKfRQ26vFePWeNdkbJwQJvqComvjEg3hEYjQrysk3j3M9QWEgXQzRqTPTFEVCTJSbdpL2GyYXYC4cLcB81UzJuWf2zoERNPdfpHwumoaaaSutfg7dccbWRaqogrBf6u9PfANQm9TsFca37UHhxvsq8WZdu71NQCY1V7w9NKKLbHF7MjjyCs6w2TM4Ej9Tyj8hFR4qo3MosgSbmQt298aEB3qQHVF8FshVwGg2vqAK7PNBHE7KgBgXQJiVRc4X1XZvWQt4uASvMowRECURoMZ17z2s3LnDrQYVqYedfzjJXxwsWXQkoQp51WWkFfp7QStBtfEhdUx15wtD8sjDdNrda8n3P6sNrN8J7NXxH4JPE7DzLLCjPSbn5Yc2jzomULSRiQN2yzC5qE43XiHB89VFqTHTduCFbP3Pom3uc5iBgjW9ky8LyPBMcsqQZSv99adjgbKpeaGPtJN6iUQ9mae1ddw6SBKTxZVZvqK6k7dJBjJ5UsFDyXLWkm8jogkRCFBfXPxmxyB5ihqk2wnsWNEbKEz6sg6RJqy5SR9A8r3QEx8FZt5z4DJpHyUAoi6KKVHEJfRvdjtjSDrayG2WUrBCgTTHsyGZEnuXLRXpy7XmdzFSwKSr4p7NPbAqt44yHdgjycn2MY5X1P9rneBdh4LukH3syRAarjmTSZr67QexRE4cca5fnxUZJ2zYNWRynqWmZy6aCBLBQziP81bHHbN5WP9MMseovCvzTpMso9TB3QLSRkCphJpyvv9qLN4tpFB9r9g3UGhTqqJFvxJDcLwR485AqLymM91kMjTvodniJ4coymUeE3MjGf2P67z4UiBDBxnzWbkCzmaPpkWFY9125hg9SovQrJnn9zzpF5smp7oiHhjrkzyi2G4qWVidtaWi6TipZFXwb8z6TSSjZkaj4SWexgnE2bUKeJS9P1xYwVSX39At735bqhfKCNP29n7UzX7bMwQiTWWK8bCiCpYSXfcfUpxtbYXdHgGMEZzpzawS9H5UeFiw31rS5Caps7QQJmMeetAuDa8tsiMJ9QauABLfJ4G6Hjkn5GM9jH9yXJWj2boH1U4ErVQXbr9KvmSsSsLeLLc3XeKQaczMtLroQax4D5estuP3Cy1gfqhbTsEWL2HkF7dUKDnuLmzsjv3kZXF9PMhcVR1Qj9j8KaYWYqKYV5TxXkrPrzSVa1yYEjU71A6ZYW327vgFJYFUJmx9vqTGym3yRiSoJiaYVfgf8iLwqS1EKSTMiisxE8hCHfKiew4YmiCTxPkq7pc5tHrKkogoRX7GdDnX93BsxGACu9nEbXwDZERLFLexrnRKpWDjqR2Z6CLWhXNPDJYMcUQ5rfGAhgu4ZK16q1"
    )

    class FuncIdx(Ctrt.FuncIdx):
        SUPERSEDE = 0
        ISSUE = 1
        DESTROY = 2
        UPDATE_LIST = 3
        SEND = 4
        TRANSFER = 5
        DEPOSIT = 6
        WITHDRAW = 7
        TOTAL_SUPPLY = 8
        MAX_SUPPLY = 9
        BALANCE_OF = 10
        GET_ISSUER = 11

    class StateVar(Ctrt.StateVar):
        """
        StateVar is the enum class for state variables of a contract.
        """

        ISSUER = 0
        MAKER = 1
        REGULATOR = 2

    class DBKey(TokCtrtWithoutSplit.DBKey):
        """
        DBKey is the class for DB key of a contract used to query data.
        """

        @classmethod
        def for_regulator(cls) -> TokCtrtWithoutSplitV2Whitelist.DBKey:
            """
            for_regulator returns the DBKey for querying the regulator.

            Returns:
                TokCtrtWithoutSplitV2Whitelist.DBKey: The DBKey.
            """
            b = TokCtrtWithoutSplitV2Whitelist.StateVar.REGULATOR.serialize()
            return cls(b)

        @classmethod
        def _for_is_in_list(
            cls, addr_data_entry: Union[de.Addr, de.CtrtAcnt]
        ) -> TokCtrtWithoutSplitV2Whitelist.DBKey:
            """
            _for_is_in_list returns the DBKey for querying the status of if the address in the given data entry
            is in the list.
            It's a helper method for is_XXX_in_list

            Args:
                addr_data_entry (Union[de.Addr, de.CtrtAcnt]): The data entry for the address.

            Returns:
                TokCtrtWithoutSplitV2Whitelist.DBKey: The DBKey.
            """
            stmp = TokCtrtWithoutSplitV2Whitelist.StateMap(
                idx=0,
                data_entry=addr_data_entry,
            )
            b = stmp.serialize()
            return cls(b)

        @classmethod
        def for_is_user_in_list(cls, addr: str) -> TokCtrtWithoutSplitV2Whitelist.DBKey:
            """
            for_is_user_in_list returns the DBKey for querying the status of if
            the given user address is in the list.

            Returns:
                TokCtrtWithoutSplitV2Whitelist.DBKey: The DBKey.
            """
            addr_de = de.Addr(md.Addr(addr))
            return cls._for_is_in_list(addr_de)

        @classmethod
        def for_is_ctrt_in_list(cls, addr: str) -> TokCtrtWithoutSplitV2Whitelist.DBKey:
            """
            for_is_ctrt_in_list returns the DBKey for querying the status of if
            the given contract address is in the list.

            Returns:
                TokCtrtWithoutSplitV2Whitelist.DBKey: The DBKey.
            """
            addr_de = de.CtrtAcnt(md.CtrtID(addr))
            return cls._for_is_in_list(addr_de)

    @property
    async def regulator(self) -> md.Addr:
        """
        regulator queries & returns the regulator of the contract.

        Returns:
            md.Addr: The address of the regulator of the contract.
        """
        raw_val = await self._query_db_key(self.DBKey.for_regulator())
        return md.Addr(raw_val)

    @classmethod
    async def register(
        cls,
        by: acnt.Account,
        max: Union[int, float],
        unit: int,
        token_description: str = "",
        ctrt_description: str = "",
        fee: int = md.RegCtrtFee.DEFAULT,
    ) -> TokCtrtWithoutSplitV2Whitelist:
        """
        register registers a token contract v2 with white list

        Args:
            by (acnt.Account): The action taker
            max (int): The max amount that can be issued
            unit (int): The granularity of splitting a token
            token_description (str): The description of the token
            ctrt_description (str, optional): The description of the contract. Defaults to "".
            fee (int, optional):  Register fee. Defaults to md.RegCtrtFee.DEFAULT.

        Returns:
            TokCtrtWithoutSplitV2Whitelist: A token contract v2 with white list
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

        tc = cls(
            data["contractId"],
            chain=by.chain,
        )
        tc._unit = unit
        return tc

    async def _is_in_list(self, db_key: TokCtrtWithoutSplitV2Whitelist.DBKey) -> bool:
        """
        _is_in_list queries & returns the status of whether the address is
        in the list for the given db_key.

        Args:
            db_key (TokCtrtWithoutSplitV2Whitelist.DBKey): The DBKey for the query.

        Returns:
            bool: If the address is in the list.
        """
        data = await self._query_db_key(db_key)
        return data == "true"

    async def is_user_in_list(self, addr: str) -> bool:
        """
        is_user_in_list queries & returns the status of whether the user address in the white/black list.

        Args:
            addr (str): The address to check.

        Returns:
            bool: If the address is in the list.
        """
        return await self._is_in_list(self.DBKey.for_is_user_in_list(addr))

    async def is_ctrt_in_list(self, addr: str) -> bool:
        """
        is_ctrt_in_list queries & returns the status of whether the contract address in the white/black list.

        Args:
            addr (str): The address to check.

        Returns:
            bool: If the address is in the list.
        """
        return await self._is_in_list(self.DBKey.for_is_ctrt_in_list(addr))

    async def _update_list(
        self,
        by: acnt.Account,
        addr_data_entry: Union[de.Addr, de.CtrtAcnt],
        val: bool,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        _update_list updates the presence of the address within the given data entry in the list.
        It's the helper method for update_list.

        Args:
            by (acnt.Account): The action taker.
            addr_data_entry (Union[de.Addr, de.CtrtAcnt]): The data entry for the address to update.
            val (bool): The value to update to.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """
        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.UPDATE_LIST,
                data_stack=de.DataStack(addr_data_entry, de.Bool(md.Bool(val))),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def update_list_user(
        self,
        by: acnt.Account,
        addr: str,
        val: bool,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        update_list_user updates the presence of the user address in the list.

        Args:
            by (acnt.Account): The action taker.
            addr (str): The account address of the user.
            val (bool): The value to update to.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """
        user_md = md.Addr(addr)
        user_md.must_on(by.chain)
        return await self._update_list(by, de.Addr(user_md), val, attachment, fee)

    async def update_list_ctrt(
        self,
        by: acnt.Account,
        addr: str,
        val: bool,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        update_list_user updates the presence of the contract address in the list.

        Args:
            by (acnt.Account): The action taker.
            addr (str): The account address of the contract.
            val (bool): The value to update to.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """
        ctrt_md = md.CtrtID(addr)
        return await self._update_list(by, de.CtrtAcnt(ctrt_md), val, attachment, fee)

    async def supersede(
        self,
        by: acnt.Account,
        new_issuer: str,
        new_regulator: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        supersede transfers the issuer role of the contract to a new account.

        Args:
            by (acnt.Account): The action taker.
            new_issuer (str): The account address of the new issuer.
            new_regulator (str): The account address of the new regulator.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        new_issuer_md = md.Addr(new_issuer)
        new_issuer_md.must_on(by.chain)

        new_regulator_md = md.Addr(new_regulator)
        new_regulator_md.must_on(by.chain)

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SUPERSEDE,
                data_stack=de.DataStack(
                    de.Addr(new_issuer_md),
                    de.Addr(new_regulator_md),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data


class TokCtrtWithoutSplitV2Blacklist(TokCtrtWithoutSplitV2Whitelist):
    CTRT_META = CtrtMeta.from_b58_str(
        "2wsw3fMnDpB5PpXoJxJeuE9RkRNzQqZrV35hBa366PhG9Sb3sPeBNeYQo8CuExtT8GpKuc84PLMsevNoodw7YGVf24PKstuzhM96H2gQoawx4BVNZwy3UFyWn156SyZakSvJPXz521p1nzactXZod1Qnn7BWYXFYCU3JFe1LGy35Sg6aXwKz6swFmBtPg1vBeQsUq1TJ5GXkDksaUYjB8ix9ScNNG8faB1mCCMWwfrcr6PyBA7YeHsTLD86zuviak6HQEQQi9kqVr4XhnDJnZyiTKGcNDo49KZyTyvkPmkFyDEhLf9DYrJM3niePqtDQ9unJj52Bku7f47hrxo83eSh3UPncyq8Hti2Ffhgb8ZFCFdnPyRDEZ1YbKFGAsJL3h3GdPFoVdnYySmnVJWrm6fVUdGgkA5ijMeqEUpXte1m7MFYCJ1wQchjebpLk3NnZzrT8FysUJVUgUzmkoSniF2UPEPXuF9cyWFWGGoZjfDWqarPMi7miqdCPQMMw4QRvSWkB3gVyeZykAvKYzXm8wYGV6HDbipZeVoyZ1UVeR6E5C4VZQmjs4GupAR9EuT5mt1ALFT4HyAMX6RCRxjeHoSgnnUJcEiRHapAYSene174RvVkRGLTtonWTYnsXUrtPD6xks4GdpQWQv89EdNWFEtmMfyVvUEFuTPGXUS5TuqYxCzg8Gor5WjPip2wDmoMYQ3wikJoRpYSfRVw88RHQPBmkHrpeHYWkAx6N7Yk4WwgBF9SVVtEWnWmPVVbuH2bQrvks4iGL8DnmEiLMs6JuFsg3a3cMHqbdvQgfu72XYKFqQzzDbDhaqFKpR3bxgMMiJvGbPuydPk9DCsG5KpqZepkkD6RGhWTQzga9G6y6ryctoGZPBHpFRwirALkksarQSEuGryhatvnjqG9U14zyW2KvJYrErMyUVy3wNK5wRqAKMjE6hFPdoH9Cn6TYQLebVTBoYTfimn5gBmgnKqBtXSfUxiwrjWujQPGxgtbNCL1RXRNRJ8nrtcpphQyRVZ8JVeubYq1zM7G1AUurEyAQi64rcbsimGptcXMAvt9TbwDjpUGRWvF6dyw1XijcukfZBQh1fG5C8peumkGnP8PemmYWKP7qsifNc44PqnNG5qYVivwtK4sz2h3B6pwneX8XNYtGSjVJCb6gJ7oDG45shocvALKNu7LwfJxXT7MPAdx7CjbHU5B3qs71wJphwkc4yWa6hHTamPTGRFGuhJa4kFfeGMctE1WZrFe47L32fKZkSxaX1sguoi5w9UPHw6udJiKPYENSSbASYpfS9q8suCs1bbq8jdMhCwoGMDZaA4MNAW1Q6sLSX6ezZ436AMbVnXZLQW8jdBaX8rvRSMJu8fdYU9PHq4MkoczxNz5jNvRiTX9jTpN1Z1P5rtgnf6XN9vzTLdqsvwZcXqvSdBwdTVgk7qn9uNjuFZEgSmA6rnPhSu6TMxJLmjKP93uqiNmXsj1NKtqBZiHjrRaUzA4pAFEyfZTdo8oaDH7umSBU2s9ff5Cruds7cYFopLm2KavHH33S7BczL7FMXAcqrESiPUzhUhHbkBKHGiCAUMVE8zxo6Eo85W2PGn6D39MaUfahEmzq8zxmrDQdmagx5EQZUev3fNCFzTzU4zpY1sra5ZPknXJkyKKfj4r9xy9Kfd8s5hsiKFyX6V1Kc2T1Ehpdkobwb7Wc8V1n1GaeL7jRgvhVg1inPaWZ3zyqNBjxnzqtLpZor3VdXLo6SikzWNahCMLNMXaoBvmJDEJUazC9qGxin7SC3YWCTAyoskJRhVMp592ehmpruu2azeCHBF2rzP6LabikVfkBSeAzGQKVeiEkU3devRNpjNM4YDXQDm9wbkPKWrqBK4SRdo44PRYG3XwNhu2gpNX8b9AuirrbRPiaJ1tJ7rzodHzLheMyUMXRB9nYx8JgrhkZzPZa4oUxo8JUNuKZnn7Ku7fEt5y"
    )
