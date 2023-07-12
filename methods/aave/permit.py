import asyncio
import random
from contracts import *
from config import *
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import ContractLogicError
import json


async def approve_tx(wallet):
    web3 = Web3(Web3.HTTPProvider(rpc['scroll']))
    with open('abi/aave_approve.json', 'r') as abi_file:
        abi = json.load(abi_file)

    smart_contract = web3.eth.contract(address=aave_lending['link'], abi=abi)
    address = web3.to_checksum_address(wallet[0])
    nonce = web3.eth.get_transaction_count(address)

    tx = smart_contract.functions.approve(address, web3.to_wei(100, 'ether')).build_transaction({
        'from': address,
        'gasPrice': web3.eth.gas_price,
        'nonce': nonce
    })

    gas = web3.eth.estimate_gas(tx)
    tx.update({'gas': gas + 15000})

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=wallet[1])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f'--> TX: https://blockscout.scroll.io/tx/{web3.to_hex(tx_hash)}')


async def permit_tx(wallet):
    web3 = Web3(Web3.HTTPProvider(rpc['scroll']))
    with open('abi/aave_permit.json', 'r') as abi_file:
        abi = json.load(abi_file)






