import asyncio
import aiofiles
import random
from config import *
import time
from methods.scroll_bridge import bridge_eth_to_scroll, bridge_scroll_to_eth
from methods.uniswap import convert_eth_to_weth, convert_weth_to_eth
from methods.aave.get_tokens import get_faucet_tokens
from methods.orbiter import orbiter_eth_to_scroll, orbiter_scroll_to_eth


async def get_wallets():
    wallets = []
    async with aiofiles.open('wallets.txt', 'r') as file:
        lines = await file.readlines()
        for line in lines:
            address, private_key = line.strip().split(':')
            wallets.append((address, private_key))
    return wallets


async def main():
    wallets = await get_wallets()

    functions = [bridge_eth_to_scroll,
                 bridge_scroll_to_eth,
                 convert_eth_to_weth,
                 convert_weth_to_eth,
                 get_faucet_tokens,
                 orbiter_eth_to_scroll,
                 orbiter_scroll_to_eth]

    i = 1
    for wallet in wallets:
        random.shuffle(functions)
        rows = random.randint(transfer_min, transfer_max)
        waiting = random.randint(time_down, time_up) * 60
        print('\n' + time.strftime("%X", time.localtime()) + f' | {wallet[0]} | Аккаунт: {str(i)}/{len(wallets)} | Кол-во вызова методотов: {str(rows)}')
        for row in range(rows):
            await functions[row % len(functions)](wallet)
            print(f'--> Next transaction in: {str(waiting / 60)} min\n')
            await asyncio.sleep(waiting)

        print('-' * 40)
        i += 1

asyncio.run(main())