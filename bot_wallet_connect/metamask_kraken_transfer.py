from web3 import Web3
#from eth_account import Account

# Connecting to infura
infura_api_key = '9590b80ff31f41509bc9c5d285ebdd4d'
infura_url = f'https://mainnet.infura.io/v3/{infura_api_key}'
web3 = Web3(Web3.HTTPProvider(infura_url))

#mainnet addresses
sender_address = "0x3225b3BDbfdC2b2B597b4Bb344B9fC6A3e99dC03"                   #this need to be replaced with the user's metamask wallet address
sender_address.strip()
recipient_address = "0x2F45493f174D724DCAD4B7B5380E1edE58e3CaD4"                #this need to be replaced with the wallet address of the wallet that the bot uses
recipient_address.strip()

#private key
sender_private_key = "6ee403152a5402d92324966e55a832add974a6c3ff26712bd1eaa4ecf2b8ddca"             #this need to be replaced with the user's metamask wallet's privatekey

# Calculating the amount to be transferred
amount_to_transfer_wei = web3.to_wei(1, 'ether') 
nonce = web3.eth.get_transaction_count(sender_address)


# Creating a transaction dictionary
transaction = {
    'to': recipient_address,
    'value': amount_to_transfer_wei,  # Amount to send 
    'gas': 21000,  # Gas limit
    'gasPrice': web3.to_wei('50', 'gwei'),  # Gas price (50 Gwei in this example)
    'nonce': nonce,
    'chainId': 1  
}

# Sign the transaction
signed_txn = web3.eth.account.sign_transaction(transaction, sender_private_key)

# Send the signed transaction
tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

print("Transaction complete")

print("Transaction Hash:", tx_hash.hex())
