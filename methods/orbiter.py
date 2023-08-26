import random
from config import *
from contracts import *
from web3 import Web3


def orbiter_eth_to_scroll(wallet):
    web3 = Web3(Web3.HTTPProvider(rpc['sepolia']))

    amount_transfer = round(random.uniform(transaction_down, transaction_up), 5)

    address = web3.to_checksum_address(wallet[0])

    balance = web3.eth.get_balance(address)
    amount_balance = round(web3.from_wei(balance, 'ether'), 3)

    print(f'--> Orbiter Bridge | Sepolia to Scroll | Баланс: {amount_balance} ETH | Сумма перевода: {amount_transfer} ETH')

    try:
        if amount_transfer < amount_balance:
            nonce = web3.eth.get_transaction_count(address)
            tx = {
                'from': address,
                'to': orbiter['address'],
                'value': web3.to_wei(amount_transfer, 'ether'),
                'chainId': web3.eth.chain_id,
                'nonce': nonce,
                'maxPriorityFeePerGas': web3.to_wei(1.5, 'gwei'),
                'maxFeePerGas': web3.to_wei(1.5, 'gwei'),
                'gas': 21000
            }

            signed_tx = web3.eth.account.sign_transaction(tx, private_key=wallet[1])
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f'--> TX: https://sepolia.etherscan.io/tx/{web3.to_hex(tx_hash)}')
        else:
            print('--> Недостаточно ETH Sepolia для перевода!')

    except Exception as e:
        print(f'--> Err: {e}')


def orbiter_scroll_to_eth(wallet):
    web3 = Web3(Web3.HTTPProvider(rpc['scroll']))

    amount_transfer = round(random.uniform(transaction_down, transaction_up), 5)

    address = web3.to_checksum_address(wallet[0])

    balance = web3.eth.get_balance(address)
    amount_balance = round(web3.from_wei(balance, 'ether'), 3)

    print(f'--> Orbiter Bridge | Scroll to Sepolia | Баланс: {amount_balance} ETH | Сумма перевода: {amount_transfer} ETH')

    try:
        if amount_transfer < amount_balance:
            nonce = web3.eth.get_transaction_count(address)
            tx = {
                'from': address,
                'to': orbiter['address'],
                'value': web3.to_wei(amount_transfer, 'ether'),
                'chainId': web3.eth.chain_id,
                'gasPrice': web3.eth.gas_price,
                'gas': 21000,
                'nonce': nonce
            }

            signed_tx = web3.eth.account.sign_transaction(tx, private_key=wallet[1])
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f'--> TX: https://sepolia-blockscout.scroll.io/tx/{web3.to_hex(tx_hash)}')
        else:
            print('--> Недостаточно ETH Scroll для перевода!')

    except Exception as e:
        print(f'--> Err: {e}')