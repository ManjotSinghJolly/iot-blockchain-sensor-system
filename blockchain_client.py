import os
from dotenv import load_dotenv
from web3 import Web3

# ---------------- LOAD ENVIRONMENT VARIABLES ----------------
load_dotenv()

RPC_URL = os.getenv("SEPOLIA_RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")

# Convert to checksum addresses
CONTRACT_ADDRESS = Web3.to_checksum_address(CONTRACT_ADDRESS)
ACCOUNT_ADDRESS = Web3.to_checksum_address(ACCOUNT_ADDRESS)

# ---------------- WEB3 CONNECTION ----------------
web3 = Web3(Web3.HTTPProvider(RPC_URL))
if web3.is_connected():
    print("✅ Connected to Sepolia network!")
else:
    raise Exception("❌ Failed to connect to Sepolia network. Check your RPC URL or internet connection.")

# ---------------- CONTRACT ABI ----------------
contract_abi = [
    {
        "inputs": [{"internalType": "string", "name": "_dataHash", "type": "string"}],
        "name": "storeHash",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}],
        "name": "getRecord",
        "outputs": [
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]

# Initialize contract instance
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# ---------------- FUNCTION TO SEND HASH ----------------
def send_hash_to_blockchain(data_hash):
    try:
        # Get the next available nonce INCLUDING pending tx
        nonce = web3.eth.get_transaction_count(ACCOUNT_ADDRESS, 'pending')

        txn = contract.functions.storeHash(data_hash).build_transaction({
            "chainId": 11155111,  # Sepolia chain ID
            "gas": 200000,
            "gasPrice": web3.to_wei("10", "gwei"),
            "nonce": nonce,
        })

        signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)

        # submit signed raw transaction
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_hash_hex = web3.to_hex(tx_hash)

        print(f"✅ Sent to blockchain! TX hash: {tx_hash_hex}")
        return tx_hash_hex

    except Exception as e:
        error_msg = str(e)

        # Gracefully ignore already-known duplicate broadcast
        if "already known" in error_msg:
            print("⚠️ Node says this transaction already exists (pending duplicate). Ignoring.")
            return "duplicate"

        print(f"❌ Blockchain transaction failed: {error_msg}")
        return None

