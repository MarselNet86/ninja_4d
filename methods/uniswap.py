import random
from contracts import *
from config import *
from web3 import Web3
import json


async def convert_eth_to_weth(wallet):
    web3 = Web3(Web3.HTTPProvider(rpc['scroll']))
    with open('abi/uniswap_router.json', 'r') as abi_file:
        abi = json.load(abi_file)

    uniswap = web3.eth.contract(address=contracts['uniswap'], abi=abi)

    address = web3.to_checksum_address(wallet[0])
    balance = web3.eth.get_balance(address)
    amount_balance = round(web3.from_wei(balance, 'ether'), 5)
    amount_transfer = round(random.uniform(swap_down, swap_up), 5)

    print(f'--> Uniswap | ETH to WETH | Баланс: {amount_balance} ETH | Сумма перевода: {amount_transfer} ETH')

    try:
        if amount_transfer < amount_balance:
            nonce = web3.eth.get_transaction_count(address)
            tx = uniswap.functions.deposit().build_transaction({
                "from": address,
                "value": web3.to_wei(amount_transfer, 'ether'),
                "gasPrice": web3.eth.gas_price,
                "nonce": nonce,
            })

            gas = web3.eth.estimate_gas(tx)
            tx.update({'gas': gas + 15000})

            signed_tx = web3.eth.account.sign_transaction(tx, private_key=wallet[1])
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f'--> TX: https://blockscout.scroll.io/tx/{web3.to_hex(tx_hash)}')

        else:
            print('--> Недостаточно ETH для перевода в WETH!')

    except Exception as e:
        print(f'--> Err: {e}')


async def convert_weth_to_eth(wallet):
    web3 = Web3(Web3.HTTPProvider(rpc['scroll']))
    with open('abi/uniswap_router.json', 'r') as abi_file:
        abi = json.load(abi_file)

    uniswap = web3.eth.contract(address=contracts['uniswap'], abi=abi)

    address = web3.to_checksum_address(wallet[0])
    get_balance = uniswap.functions.balanceOf(address).call()
    amount_balance = round(web3.from_wei(get_balance, 'ether'), 2)
    amount_transfer = round(random.uniform(swap_down, swap_up), 5)

    print(f'--> Uniswap | WETH to ETH | Баланс: {amount_balance} WETH | Сумма перевода: {amount_transfer} WETH')

    nonce = web3.eth.get_transaction_count(address)
    amount = web3.to_wei(amount_transfer, 'ether')

    try:
        if amount_transfer < amount_balance:
            tx = uniswap.functions.withdraw(amount).build_transaction({
                "from": address,
                "gasPrice": web3.eth.gas_price,
                "nonce": nonce,
            })

            gas = web3.eth.estimate_gas(tx)
            tx.update({'gas': gas + 15000})

            signed_tx = web3.eth.account.sign_transaction(tx, private_key=wallet[1])
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f'--> TX: https://blockscout.scroll.io/tx/{web3.to_hex(tx_hash)}')
        else:
            print('--> Недостаточно WETH для перевода в ETH!')

    except Exception as e:
        print(f'--> Err: {e}')