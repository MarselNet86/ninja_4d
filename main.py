import random
from config import *
import time
from colorama import init, Fore
from colorama import Style
from methods.scroll_bridge import bridge_eth_to_scroll, bridge_scroll_to_eth
from methods.orbiter import orbiter_eth_to_scroll, orbiter_scroll_to_eth


def get_wallets():
    wallets = []
    with open('wallets.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            address, private_key = line.strip().split(':')
            wallets.append((address, private_key))
    return wallets


def main():
    wallets = get_wallets()

    functions = [bridge_eth_to_scroll,
                 orbiter_eth_to_scroll,
                 orbiter_scroll_to_eth]

    for val, wallet in enumerate(wallets, start=1):
        rows = random.randint(transfer_min, transfer_max)
        print('\n' + time.strftime("%X", time.localtime()) + f' | {Fore.BLUE}{wallet[0]}{Style.RESET_ALL} | '
                                                             f'Аккаунт: {Fore.BLUE}{val}/{len(wallets)}{Style.RESET_ALL} | '
                                                             f'Кол-во вызова методотов: {Fore.BLUE}{str(rows)}{Style.RESET_ALL}')
        for row in range(rows):
            waiting = random.randint(time_down, time_up)
            functions[row % len(functions)](wallet)

            print(f'{Fore.GREEN}--> Next transaction in: {waiting} sec {Style.RESET_ALL}\n')
            time.sleep(waiting)

        print(Style.BRIGHT + '-' * 40)


if __name__ == '__main__':
    print(Fore.GREEN + 'LCD Service for Scroll' + Style.RESET_ALL)
    main()

