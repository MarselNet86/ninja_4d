import random
from contracts import *
from config import *
from web3 import Web3
import json
import math


async def bridge_eth_to_scroll(wallet):
    web3 = Web3(Web3.HTTPProvider(rpc['eth_goerli']))
    with open('abi/goerli_eth_contract.json', 'r') as abi_file:
        abi = json.load(abi_file)

    smart_contract = web3.eth.contract(address=contracts['goerli'], abi=abi)
    amount_transfer = round(random.uniform(eth_to_scroll_down, eth_to_scroll_up), 5)

    rounded_value = math.floor(amount_transfer / step) * step
    amount_uint256 = web3.to_wei(rounded_value, 'ether')

    address = web3.to_checksum_address(wallet[0])

    balance = web3.eth.get_balance(address)
    amount_balance = round(web3.from_wei(balance, 'ether'), 3)

    print(f'--> Bridge | Goerli to Scroll | Баланс: {amount_balance} ETH | Сумма перевода: {amount_transfer} ETH')

    try:
        if amount_transfer < amount_balance:
            nonce = web3.eth.get_transaction_count(address)
            tx = smart_contract.functions.depositETH(amount_uint256, 40000).build_transaction({
                'from': address,
                'value': web3.to_wei(float(amount_transfer) + 0.000004, 'ether'),
                'gasPrice': web3.eth.gas_price,
                'nonce': nonce
            })

            gas = web3.eth.estimate_gas(tx)
            tx.update({'gas': gas + 15000})

            signed_tx = web3.eth.account.sign_transaction(tx, private_key=wallet[1])
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f'--> TX: https://goerli.etherscan.io/tx/{web3.to_hex(tx_hash)}')
        else:
            print('--> Недостаточно ETH Goerli для перевода!')

    except Exception as e:
        print(f'--> Err: {e}')


async def bridge_scroll_to_eth(wallet):
    web3 = Web3(Web3.HTTPProvider(rpc['scroll']))
    with open('abi/scroll_eth_contract.json', 'r') as abi_file:
        abi = json.load(abi_file)

    smart_contract = web3.eth.contract(address=contracts['scroll'], abi=abi)
    address = web3.to_checksum_address(wallet[0])

    balance = web3.eth.get_balance(address)
    amount_balance = round(web3.from_wei(balance, 'ether'), 5)
    amount_transfer = round(random.uniform(scroll_to_eth_down, scroll_to_eth_up), 5)

    print(f'--> Bridge | Scroll to Goerli | Баланс: {amount_balance} ETH | Сумма перевода: {amount_transfer} ETH')

    try:
        if amount_transfer < amount_balance:
            nonce = web3.eth.get_transaction_count(address)
            tx = smart_contract.functions.withdrawETH(1000000000000000, 160000).build_transaction({
                'from': address,
                'value': web3.to_wei(float(amount_transfer), 'ether'),
                'gasPrice': web3.eth.gas_price,
                'nonce': nonce
            })

            gas = web3.eth.estimate_gas(tx)
            tx.update({'gas': gas + 15000})

            signed_tx = web3.eth.account.sign_transaction(tx, private_key=wallet[1])
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f'--> TX: https://blockscout.scroll.io/tx/{web3.to_hex(tx_hash)}')

        else:
            print('--> Недостаточно ETH Scroll для перевода!')

    except Exception as e:
        print(f'--> Err: {e}')