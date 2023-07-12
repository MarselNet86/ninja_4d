import asyncio
import random
from contracts import *
from web3 import Web3
from web3.exceptions import ContractLogicError
import json


async def get_faucet_tokens(wallet):
    web3 = Web3(Web3.HTTPProvider(rpc['scroll']))
    with open('abi/aave_faucet.json', 'r') as abi_file:
        abi = json.load(abi_file)

    aave_faucet = web3.eth.contract(address=contracts['aave_faucet'], abi=abi)

    address = web3.to_checksum_address(wallet[0])
    balance = web3.eth.get_balance(address)
    amount_balance = round(web3.from_wei(balance, 'ether'), 5)

    print(f'--> Aave Faucet | Get Test Tokens | Баланс: {amount_balance} ETH |')

    keys = list(aave_protocol.keys())
    random.shuffle(keys)

    shuffled_aave_protocol = {key: aave_protocol[key] for key in keys}

    for token in shuffled_aave_protocol.items():
        try:
            if amount_balance > 0:
                nonce = web3.eth.get_transaction_count(address)
                tx = aave_faucet.functions.mint(token[1], address, 100000000).build_transaction({
                    "gasPrice": web3.eth.gas_price,
                    "nonce": nonce,
                })

                gas = web3.eth.estimate_gas(tx)
                tx.update({'gas': gas + 15000})

                signed_tx = web3.eth.account.sign_transaction(tx, private_key=wallet[1])
                tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                print(f'--> Get Token: {token[0]} | TX: https://blockscout.scroll.io/tx/{web3.to_hex(tx_hash)}')

            else:
                print('--> Недостаточно ETH для минта токенов!')

        except ContractLogicError as e:
            if "Mint limit transaction exceeded" in str(e):
                print(f"--> Get Token: {token[0]} | Err: Превышен лимит на получение токенов!")

            else:
                print("--> Произошла ошибка в логике контракта:", str(e))

        waiting = random.randint(5, 60)
        print(f'--> Next mint in: {str(waiting)} sec\n')

        await asyncio.sleep(waiting)
