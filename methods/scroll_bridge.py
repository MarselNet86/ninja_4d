import random
from contracts import *
from config import *
from web3 import Web3
import json
import math


def get_sepolia_abi():
    with open('abi/sepolia_eth.json', 'r') as abi_file:
        abi = json.load(abi_file)

    return abi


def get_scroll_abi():
    with open('abi/scroll_eth.json', 'r') as abi_file:
        abi = json.load(abi_file)

    return abi


def bridge_eth_to_scroll(wallet):
    web3 = Web3(Web3.HTTPProvider(rpc['sepolia']))

    smart_contract = web3.eth.contract(address=contracts['eth_sepolia'], abi=get_sepolia_abi())
    amount_transfer = round(random.uniform(transaction_down, transaction_up), 5)

    amount_uint256 = web3.to_wei(amount_transfer, 'ether')

    address = web3.to_checksum_address(wallet[0])

    balance = web3.eth.get_balance(address)
    amount_balance = round(web3.from_wei(balance, 'ether'), 3)

    print(f'--> Bridge | Sepolia to Scroll | Баланс: {amount_balance} ETH | Сумма перевода: {amount_transfer} ETH')

    try:
        if amount_transfer < amount_balance:
            nonce = web3.eth.get_transaction_count(address)
            tx = smart_contract.functions.depositETH(amount_uint256, 400000).build_transaction({
                'from': address,
                'value': web3.to_wei(amount_transfer + 0.003, 'ether'),
                'gasPrice': web3.eth.gas_price,
                'nonce': nonce
            })

            gas = web3.eth.estimate_gas(tx)
            tx.update({'gas': gas + 15000})

            signed_tx = web3.eth.account.sign_transaction(tx, private_key=wallet[1])
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f'--> TX: https://sepolia.etherscan.io/tx/{web3.to_hex(tx_hash)}')
        else:
            print('--> Недостаточно ETH Sepolia для перевода!')

    except Exception as e:
        print(f'--> Err: {e}')


def bridge_scroll_to_eth(wallet):
    web3 = Web3(Web3.HTTPProvider(rpc['scroll']))

    smart_contract = web3.eth.contract(address=contracts['eth_scroll'], abi=get_scroll_abi())
    amount_transfer = round(random.uniform(transaction_down, transaction_up), 5)

    amount_uint256 = web3.to_wei(amount_transfer, 'ether')

    address = web3.to_checksum_address(wallet[0])

    balance = web3.eth.get_balance(address)
    amount_balance = round(web3.from_wei(balance, 'ether'), 3)

    print(f'--> Bridge | Scroll to Sepolia | Баланс: {amount_balance} ETH | Сумма перевода: {amount_transfer} ETH')

    try:
        if amount_transfer < amount_balance:
            nonce = web3.eth.get_transaction_count(address)
            tx = smart_contract.functions.withdrawETH(amount_uint256, 0).build_transaction({
                'from': address,
                'value': web3.to_wei(amount_transfer, 'ether'),
                'gasPrice': web3.eth.gas_price,
                'nonce': nonce
            })

            gas = web3.eth.estimate_gas(tx)
            tx.update({'gas': gas + 15000})

            signed_tx = web3.eth.account.sign_transaction(tx, private_key=wallet[1])
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f'--> TX: https://sepolia-blockscout.scroll.io/tx/{web3.to_hex(tx_hash)}')

        else:
            print('--> Недостаточно ETH Scroll для перевода!')

    except Exception as e:
        print(f'--> Err: {e}')