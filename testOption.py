import py_v_sdk as pv
import asyncio


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

        # base_ctrt = await pv.TokenCtrtWithoutSplit.register(acnt0,1000,1)
        # target_ctrt = await pv.TokenCtrtWithoutSplit.register(acnt0,1000,1)
        # option_ctrt = await pv.TokenCtrtWithoutSplit.register(acnt0,1000,1)
        # proof_ctrt = await pv.TokenCtrtWithoutSplit.register(acnt0,1000,1)
        # print("base_ctrt: ", base_ctrt.ctrt_id)
        # print("target_ctrt: ", target_ctrt.ctrt_id)
        # print("option_ctrt: ", option_ctrt.ctrt_id)
        # print("proof_ctrt: ", proof_ctrt.ctrt_id)

        base_tok_id = "TWu5TgdR3mskWotcdtJE73oMpMYxUGHft5HbS8EXe"
        target_tok_id = "TWtKU66jaxGqXt2GCAgBY4Kbr8fJ4dPNMd6ZSGit6"
        option_tok_id = "TWuQpsALSj5NbqJC6S2dte5Y5YJCtcP1H5RHFbixT"
        proof_tok_id = "TWsjjcbaaENCmuACSTaUgjJjkibgKPvJ7Pj6AkDCV"

        base_ctrt = pv.TokenCtrtWithoutSplit("CF7Gip15dbhrUvniKR1iaeE4iT6XERJ6PhB", ch)
        target_ctrt = pv.TokenCtrtWithoutSplit(
            "CEzYnbcM8CJ57SnoxnEXjQmYUhTVXhkFEwt", ch
        )
        option_ctrt = pv.TokenCtrtWithoutSplit(
            "CFAENCMxJpmPhaukTgkoiNZZGZvj5wuFLA6", ch
        )
        proof_ctrt = pv.TokenCtrtWithoutSplit("CEuPoGtXxUa8GGYds6MEQWL27Tc6b51RyNM", ch)

        # await base_ctrt.deposit(acnt0, "CEs1MSnZ7PpWneUnXzdmums5LNZuDr9zeXV", 1000)
        # await target_ctrt.deposit(acnt0, "CEs1MSnZ7PpWneUnXzdmums5LNZuDr9zeXV", 1000)
        # await option_ctrt.deposit(acnt0, "CEs1MSnZ7PpWneUnXzdmums5LNZuDr9zeXV", 1000)
        # await proof_ctrt.deposit(acnt0, "CEs1MSnZ7PpWneUnXzdmums5LNZuDr9zeXV", 1000)

        # print(await base_ctrt.issue(acnt0,1000))
        # print(await target_ctrt.issue(acnt0,1000))
        # print(await option_ctrt.issue(acnt0,1000))
        # print(await proof_ctrt.issue(acnt0,1000))

        # test register
        # voption = await pv.VOptionCtrt.register(
        #     acnt0,base_tok_id, target_tok_id, option_tok_id, proof_tok_id,1646212102,1646215702)
        # print(voption.ctrt_id)
        option_instance = pv.VOptionCtrt("CEs1MSnZ7PpWneUnXzdmums5LNZuDr9zeXV", ch)

        # test activate
        # print(await option_instance.activate(acnt0,1000,10,1))
        # a =await option_instance.max_issue_num
        # print(a.data)

        # test mint
        # print(await option_instance.mint(acnt0,100))
        # mint_tx_id = "DkbPMbATCXnJ7Vugaad7ZMZnK8ihVqWSsJK8ykaXUnL8"
        # b = await option_instance.get_option_tok_bal(addr1)
        # print(b.data) # base:1000, target:800, option and proof: 200

        # test unlock
        # print(await option_instance.unlock(acnt0,100))
        # unlock_tx_id = "2tj91qZwXMbU6evxVfjZ5SDxWH5vEfjrhVjrQuJCbWBc"
        # b = await option_instance.get_target_tok_bal(addr1)
        # print(b.data)#base and target: 1000, option and proof: 0

        # test execute
        print(await option_instance.execute(acnt0, 100))

    finally:
        await api.sess.close()


if __name__ == "__main__":
    asyncio.run(main())
