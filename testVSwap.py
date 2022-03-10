import py_vsys as pv
import asyncio
import time
import py_vsys.model as md


async def main():
    try:
        api = await pv.NodeAPI.new("http://veldidina.vos.systems:9928")
        ch = pv.Chain(api)

        wal = pv.Wallet.from_seed_str(
            "wheel explain level seven scene coach cherry mutual spread account deposit rapid clinic critic glance"
        )
        acnt0 = wal.get_account(ch, 0)
        acnt1 = wal.get_account(ch, 2)
        addr1 = "AU8h6YH5iJuwFzcUdGugUwKo2E8tbEHdtqu"
        addr2 = "AUCzwTg7EjGoa68nRy27873LY5LtvKmQy2H"

        # ctrtA = await pv.TokCtrtWithoutSplit.register(acnt0,1000,1)
        # print(ctrtA.ctrt_id)
        # tok_ctrt_id1 = "CF2BkHjsjDN3PkHjEPfeureYbE5Pa9j5dkN"
        # token_id1 = pv.Ctrt.get_tok_id(md.CtrtID(tok_ctrt_id1),md.TokenIdx(0))
        ctrtA = pv.TokCtrtWithoutSplit("CFB7uJtDuQcf4fJ4GTSan3WuyKSCefcvKRi", ch)

        # ctrtB = await pv.TokCtrtWithoutSplit.register(acnt0,1000,1)
        # print(ctrtB.ctrt_id)
        tok_ctrt_id2 = "CEzctuQZBe7LcnV2hmcB3HfNECJsMzWfPdo"
        token_id2 = pv.Ctrt.get_tok_id(md.CtrtID(tok_ctrt_id2), md.TokenIdx(0))
        ctrtB = pv.TokCtrtWithoutSplit(tok_ctrt_id2, ch)

        # ctrtC = await pv.TokCtrtWithoutSplit.register(acnt0,1000,1)
        # print(ctrtC.ctrt_id)
        tok_ctrt_id3 = "CF6eFMf4dpDpnAeMKg92kDKg4tvEfjLUzMg"
        token_id3 = pv.Ctrt.get_tok_id(md.CtrtID(tok_ctrt_id3), md.TokenIdx(0))
        ctrtC = pv.TokCtrtWithoutSplit(tok_ctrt_id3, ch)

        # await ctrtA.deposit(acnt0,"CF5XanD64XpzMZPoaMZ1svYrAriaqsUDeSb", 1000)
        # print(await ctrtB.issue(acnt0, 1000))
        # print(await ctrtC.issue(acnt0, 1000))

        # await ctrtA.deposit(acnt0,"CF5XanD64XpzMZPoaMZ1svYrAriaqsUDeSb", 1000)
        # print(await ctrtB.deposit(acnt0,"CF5XanD64XpzMZPoaMZ1svYrAriaqsUDeSb", 1000))
        # await ctrtC.deposit(acnt0,"CF5XanD64XpzMZPoaMZ1svYrAriaqsUDeSb", 1000)

        # nc = await pv.VSwapCtrt.register(by=acnt0,tok_a_id=token_id1.data,tok_b_id=token_id2.data,liq_tok_id=token_id3.data,min_liq=100)
        # print(nc.ctrt_id) # CF5XanD64XpzMZPoaMZ1svYrAriaqsUDeSb

        nc = pv.VSwapCtrt("CF5XanD64XpzMZPoaMZ1svYrAriaqsUDeSb", ch)
        # print(await nc.total_liq_tok_supply)

        # print(await nc.get_liq_tok_bal(acnt0.addr.data))
        # print(await nc.get_tok_a_bal(acnt0.addr.data))
        print(await nc.get_tok_b_bal(acnt0.addr.data))

        resp = await nc.remove_liquidity(acnt0, 802, 100, 100, int(time.time()) + 600)
        print(resp)

    finally:
        await api.sess.close()


if __name__ == "__main__":
    asyncio.run(main())
