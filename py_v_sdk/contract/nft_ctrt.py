"""
nft_ctrt contains NFT contract.
"""
from __future__ import annotations
from typing import Dict, Any, TYPE_CHECKING

from loguru import logger

# https://stackoverflow.com/a/39757388
if TYPE_CHECKING:
    from py_v_sdk import account as acnt

from py_v_sdk import data_entry as de
from py_v_sdk import tx_req as tx
from py_v_sdk import model as md

from . import CtrtMeta, Ctrt


class NFTCtrt(Ctrt):
    """
    NFTCtrt is the class for VSYS NFT contract V1
    """

    CTRT_META = CtrtMeta.from_b58_str(
        "VJodouhmnHVDwtkBZ2NdgahT7NAgNE9EpWoZApzobhpua2nDL9D3sbHSoRRk8bEFeme2BHrXPdcq5VNJcPdGMUD54Smwatyx74cPJyet6bCWmLciHE2jGw9u5TmatjdpFSjGKegh76GvJstK3VaLagvsJJMaaKM9MNXYtgJyDr1Zw7U9PXV7N9TQnSsqz6EHMgDvd8aTDqEG7bxxAotkAgeh4KHqnk6Ga117q5AJctJcbUtD99iUgPmJrC8vzX85TEXgHRY1psW7D6daeExfVVrEPHFHrU6XfhegKv9vRbJBGL861U4Qg6HWbWxbuitgtKoBazSp7VofDtrZebq2NSpZoXCAZC8DRiaysanAqyCJZf7jJ8NfXtWej8L9vg8PVs65MrEmK8toadcyCA2UGzg6pQKrMKQEUahruBiS7zuo62eWwJBxUD1fQ1RGPk9BbMDk9FQQxXu3thSJPnKktq3aJhD9GNFpvyEAaWigp5nfjgH5doVTQk1PgoxeXRAWQNPztjNvZWv6iD85CoZqfCWdJbAXPrWvYW5FsRLW1xJ4ELRUfReMAjCGYuFWdA3CZyefpiDEWqVTe5SA6J6XeUppRyXKpKQTc6upesoAGZZ2NtFDryq22izC6D5p1i98YpC6Dk1qcKevaANKHH8TfFoQT717nrQEY2aLoWrA1ip2t5etdZjNVFmghxXEeCAGy3NcLDFHmAfcBZhHKeJHp8H8HbiMRtWe3wmwKX6mPx16ahnd3dMGCsxAZfjQcy4J1HpuCm7rHMULkixUFYRYqx85c7UpLcijLRybE1MLRjEZ5SEYtazNuiZBwq1KUcNipzrxta9Rpvt2j4WyMadxPf5r9YeAaJJp42PiC6SGfyjHjRQN4K3pohdQRbbG4HQ95NaWCy7CAwbpXRCh9NDMMQ2cmTfB3KFW2M"
    )

    class FuncIdx(Ctrt.FuncIdx):
        """
        FuncIdx is the enum class for function indexes of a contract.
        """

        SUPERSEDE = 0
        ISSUE = 1
        SEND = 2
        TRANSFER = 3
        DEPOSIT = 4
        WITHDRAW = 5

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
        def for_issuer(cls) -> NFTCtrt.DBKey:
            """
            for_issuer returns the NFTCtrt.DBKey object for querying the issuer.

            Returns:
                NFTCtrt.DBKey: The NFTCtrt.DBKey object.
            """
            b = NFTCtrt.StateVar.ISSUER.serialize()
            return cls(b)

        @classmethod
        def for_maker(cls) -> NFTCtrt.DBKey:
            """
            for_maker returns the NFTCtrt.DBKey object for querying the maker.

            Returns:
                NFTCtrt.DBKey: The NFTCtrt.DBKey object.
            """
            b = NFTCtrt.StateVar.MAKER.serialize()
            return cls(b)

    @classmethod
    async def register(
        cls,
        by: acnt.Account,
        description: str = "",
        fee: int = md.RegCtrtFee.DEFAULT,
    ) -> NFTCtrt:
        """
        register registers an NFT Contract.

        Args:
            by (acnt.Account): The action taker.
            description (str, optional): The description of the action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.RegCtrtFee.DEFAULT.

        Returns:
            NFTCtrt: The NFTCtrt object of the registered NFT contract.
        """
        data = await by._register_contract(
            tx.RegCtrtTxReq(
                data_stack=de.DataStack(),
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

    async def issue(
        self,
        by: acnt.Account,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        issue issues a token of the NFT contract.

        Args:
            by (acnt.Account): The action taker.
            attachment (str, optional): The attachment of the action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """
        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.ISSUE,
                data_stack=de.DataStack(
                    de.String(md.Str(attachment)),
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
        tok_idx: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        send sends the NFT token from the action taker to the recipient.

        Args:
            by (acnt.Account): The action taker.
            recipient (str): The account address of the recipient.
            tok_idx (int): The index of the token within this contract to send.
            attachment (str, optional): The attachment of the action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

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
                    de.INT32(md.TokenIdx(tok_idx)),
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
        tok_idx: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        transfer transfers the NFT token from the sender to the recipient.

        Args:
            by (acnt.Account): The action taker.
            sender (str): The account address of the sender.
            recipient (str): The account address of the recipient.
            tok_idx (int): The index of the token within this contract to transfer.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

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
                    de.INT32(md.TokenIdx(tok_idx)),
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
        ctrt_id: str,
        tok_idx: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        deposit deposits the NFT token from the action taker to another contract.

        Args:
            by (acnt.Account): The action taker.
            ctrt_id (str): The id of the contract to deposit into.
            tok_idx (int): The index of the token within this contract to deposit.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """
        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.DEPOSIT,
                data_stack=de.DataStack(
                    de.Addr(md.Addr(by.addr.b58_str)),
                    de.CtrtAcnt(md.CtrtID(ctrt_id)),
                    de.INT32(md.TokenIdx(tok_idx)),
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
        ctrt_id: str,
        tok_idx: int,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        withdraw withdraws the token from another contract to the action taker.

        Args:
            by (acnt.Account): The action taker.
            ctrt_id (str): The id of the contract to withdraw from.
            tok_idx (int): The index of the token within this contract to withdraw.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """
        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.WITHDRAW,
                data_stack=de.DataStack(
                    de.CtrtAcnt(md.CtrtID(ctrt_id)),
                    de.Addr(md.Addr(by.addr.b58_str)),
                    de.INT32(md.TokenIdx(tok_idx)),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data

    async def supersede(
        self,
        by: acnt.Account,
        new_issuer: str,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        """
        supersede transfers the issuer role of the contract to a new account.

        Args:
            by (acnt.Account): The action taker.
            new_issuer (str): The account address of the new issuer.
            attachment (str, optional): The attachment of this action. Defaults to "".
            fee (int, optional): The fee to pay for this action. Defaults to md.ExecCtrtFee.DEFAULT.

        Returns:
            Dict[str, Any]: The response returned by the Node API
        """

        new_issuer_md = md.Addr(new_issuer)
        new_issuer_md.must_on(by.chain)

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.SUPERSEDE,
                data_stack=de.DataStack(
                    de.Addr(new_issuer_md),
                ),
                timestamp=md.VSYSTimestamp.now(),
                attachment=md.Str(attachment),
                fee=md.ExecCtrtFee(fee),
            )
        )
        logger.debug(data)
        return data


class NFTCtrtV2Whitelist(NFTCtrt):
    """
    NFTCtrtV2Whitelist is the class for VSYS NFT contract V2 with whitelist
    """

    CTRT_META = CtrtMeta.from_b58_str(
        "RVbUxLpK4Vi15qHaDvy1e4kjNmQqLrcdDqXBjMBHB1RH3xPQS7tcuEEoxHZ72mUVttTa3EHMmD6gRUcKSXW1kQkNpBNEFzgfM2qSS2BRvdHdke9xNPgu6i2m8KbViKeBiq9ydsHMMkyZL5ShfpfBD8BfJmTiSERjgx7voeusYwhTWT2VDg4E2k3krqDmbCVTtvxm6nydPxxwDH9RBBWJwLjkMHRdaoDFXrDBA5KXc6YgSnT9P6JZKRAbTYAzAEF1514oGEvRjgz8HUhCzjVjmTUgjHXeYT416f8soj1xzmQW4LCZszSGeo1hMh5HZWshg9NwJGkJW9C2HVXr31RvSvKcLK6NgDEnxaci6H9mjBagXW5MNTp7KKKmEuurKVHw1GydPE2Zx91cvFzQ5Q4xiUWhRtMCyMmDp5AH4STRgcdyK4DsFR2unaxhQgEHzxCVR3EPe6cddnW6ZdGDvSV6KzDz1RBPUu6Ex7PUJ6L8GAdbunppVJrmLYER7aySP67Z2j7mqaRwCTDYSMeh47a3aCpuhG9dGoTMF9UZhxBZu5irg7fwzifPWJKQBKPp2JvefKanEwxPqLUbFq5a1Gu8dqFxaa6cC248EHHK1WqHtkZcUdFN65V2rhGCxPvNKADwH7STsn7awHuowUTJJe1EnTHvyJ9Yzd8Kg8JFn1Q5tTEAQTFujCMnriXxbqmjNYhQghqxyxjVL447NDmvYBqey7jcp4CBde9myjbFdxDvbtVDawwxoGvGnzosn14RsBBBZjxcqKDHAMbkJLdWkjL5n8yjXxiAZfbEt4Bk5uDK4YP8YgbGSHKVhGWYWbmKxEDGAziRnGTdwy79RPtTsb6zx8fCGfU3gCD4skY6ny6bM28Ue81YBMPt89TKm6Gt8GLhXHft8vSp9cUiV6dDauVHmyu1vgACcN7kpu1yMZExZEazUDSBf9SuiyEZWXsDkXjm4ayauX7oTakMuFFyRACtrAVowB9thQGt1jWeLdg1kVhucrdLJ2fj2NWRX87Q6UqAjmtjyVBKyntpheWpJTg8GzLbH2ASVF556pgpC1jNQXo3HxEBoTGnNzf4v3E8xqibBGxE3wY7hvpvEXv7ww3Yw1TxLjxtMDjqLuZvXrMWoqYxQEanHBfJkz3bCMeDajJbYwyqsVkgTXCpGNgXdUGYD1w5TV5DhbbPjxFnJ73aVJ7ANVmNi6UYNxCLWPkVmNNnRMWpGc2sBw9cK7GpChQedwK1u5GaRd1yR3JVTCn7GdwELFF8BWSiWCShh8aVNz1EThqz8uMUeU6iUr5W1LTVTFiJ1kfEDVZyLEKZbZWSJSV83c9bHW4jFm3rRraEwQiMaRvBkq3ELeFpZKMwKtKte9UWUniZU9QbAZwMvNAEQqkUavNwKQS7haUxCUR5jv6iBj6hZ25qVZU9CduqH3YZAmonAQsm9WVTbh91qeFVtjBAmVvfUJT1y6AGSWyHhpyzSrGqAeornSkwdcaZtTDwsVMqy6Y1tha2493HmQ7dE8Cty8VH"
    )

    class FuncIdx(Ctrt.FuncIdx):
        """
        FuncIdx is the enum class for function indexes of a contract.
        """

        SUPERSEDE = 0
        ISSUE = 1
        UPDATE_LIST = 2
        SEND = 3
        TRANSFER = 4
        DEPOSIT = 5
        WITHDRAW = 6

    async def _update_list(
        self,
        by: acnt.Account,
        addr: str,
        val: bool,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
        for_user: bool = True,
    ) -> Dict[str, Any]:
        addr_de = de.Addr if for_user else de.CtrtAcnt

        addr_md = md.Addr(addr)
        addr_md.must_on(by.chain)

        data = await by._execute_contract(
            tx.ExecCtrtFuncTxReq(
                ctrt_id=self._ctrt_id,
                func_id=self.FuncIdx.UPDATE_LIST,
                data_stack=de.DataStack(
                    addr_de(addr_md),
                    de.Bool(md.Bool(val)),
                ),
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
        return await self._update_list(by, addr, val, attachment, fee, True)

    async def update_list_ctrt(
        self,
        by: acnt.Account,
        addr: str,
        val: bool,
        attachment: str = "",
        fee: int = md.ExecCtrtFee.DEFAULT,
    ) -> Dict[str, Any]:
        return await self._update_list(by, addr, val, attachment, fee, False)


class NFTCtrtV2Blacklist(NFTCtrtV2Whitelist):
    """
    NFTCtrtV2Blacklist is the class for VSYS NFT contract V2 with blacklist
    """

    CTRT_META = CtrtMeta.from_b58_str(
        "RVbUxLpK4Vi15qHaDvy1e4kjNmQqLrcdDqXBjMBHB1RH3xPQS7tcuEEoxHZ72mUVttTa3EHMmD6gRUcKSXW1kQkNpBNEFzgfM2qSS2BRvdHdke9xNPgu6i2m8KbViKeBiq9ydsHMMkyZL5ShfpfBD8BfJmTiSERjgx7voeusYwhTWT2VDg4E2k3krqDmbCVTtvxm6nydPxxwDH9RBBWJwLjkMHRdaoDFXrDBA5KXc6YgSnT9P6JZKRAbTYAzAEF1514oGEvRjgz8HUhCzjVjmTUgjHXdpR6yuM3CwR8EYGbH9HNEcnUoTEcjLwGNCtUb2QBRJLzpu2VzhqJTZkXrrjuREfFpkBPN8WCYgi4LguF7avFQA4atahzVKU98j7UG9byW4ERkdHFduxSWX6nun8NYxgw4k1LyGe7A6NEo6vfAeBryYb5V2CowTiXb4xxhzjytuNPEckZYJcMLkgxtfzmcbfnqx7ff4hgWX2L5AWh5y9K21BDhrCWzjnb81atVvwBivMSBvaoFGNRj5RJ8Qz4r7cGyZ34PqcdZsbTvnTJTzHNLUxSyMQNqNBa3vwzifuuwPBUfZ7xKXGbQVo19D7BWzgVhmye1CKNxsW3QRNRYqrWZaiUqRmb1ids8BfAoyNEk9HzpJ3zYq28rjmZ4nZp8TCnaH7jZxUDeVhBfzQEmEbSSHDaPSnDNtLQ9VKQa9ov3ZTC2muUw7P8hUR3N5casgZpG3a23uYCLT4TKSRxQU9JZ3kPe2r8wVUvhmeJP9EJiUi4CmArEGQoGhQZLZuCneVZdWbreqMhnQLVjVekv5NPWwEf4UNgFH5RS6XQ2mcHqHd5KHAG9xa5qaPDQ6YZ4Fagh2bw92fw4CiDYiCodsPVYFqYDrWRJmbdY9xQmRZ4M4w4UKQU8HmwYhqCEtSLrH3dmuia2JkvEv8f47QZq78rLaUmcY5Fch9zjEZTe63StcdB1GycZoHK7iCoHrt1AjJ8Ex5J9xgJxbQ5nZEAS3vrqy9znznEuhawtL9PYn5VYEbFX6VdCTxbYcjehKXQRCxouyYAS35BqmoYuVYM54qtLUbgrXPUTefQ9XGGGAazeaSDkS3hASwx3DuLU7MYDmpYgyoefxEVVi8D2GVH6TaiU34qFTiTEK1348ZzruUugT5DZRwFgf5t197iYngD9AKb71TBsA2ZnJueNVFEFXmXgFKMU2eZvAZBFcoH1EAUttCgSztBwXMS9Cwqa5kXXwr1cxNUESzNoDgZWaEAHPiCB2PAjBdsgWGTbkepSBMbQTj5aKV4LybHoWs8JNKpHMMwSBeRLNmk3ibGkNu2qe7ZcZZJJqNz9vZjvhKJ8Ws1HYrqaPb7ysBHW7fU1mrh95y7AkSZGsKEbGNpyijpT66Q4wxpuysU6L3wDMdapdQLjdyBs3rjQtXRbhSiRyYZLShXUantffsBkMWmwD2WZg6Dp6hpZWBEFGq3kD1ysVbi47HqDTsD1aWTuE5hCY9XHmveE3WmRd8p56YZxmrXKh9Ns"
    )
