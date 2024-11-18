import hashlib
import time
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import json


# Wallet class
class Wallet:
    def __init__(self):
        self.key = RSA.generate(2048)
        self.public_key = self.key.publickey().export_key().decode()
        self.private_key = self.key.export_key().decode()

    def sign_transaction(self, transaction):
        message = json.dumps(transaction, sort_keys=True).encode()
        h = SHA256.new(message)
        signature = pkcs1_15.new(self.key).sign(h)
        return signature

    @staticmethod
    def verify_transaction(transaction, signature, public_key):
        message = json.dumps(transaction, sort_keys=True).encode()
        h = SHA256.new(message)
        key = RSA.import_key(public_key)
        try:
            pkcs1_15.new(key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False


# Block class
class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(content.encode()).hexdigest()


# Blockchain class
class Blockchain:
    def __init__(self, difficulty=4, max_supply=50000000):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.mining_reward = 50
        self.max_supply = max_supply
        self.current_supply = 0
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def mine_block(self, miner_public_key):
        if self.current_supply >= self.max_supply:
            return "Max supply reached. Mining stopped."

        data = {
            "transactions": self.pending_transactions,
            "reward": self.mining_reward,
            "miner": miner_public_key
        }
        new_block = Block(
            len(self.chain),
            self.get_latest_block().hash,
            time.time(),
            data
        )

        # Proof of Work
        while not new_block.hash.startswith("0" * self.difficulty):
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()

        self.chain.append(new_block)
        self.current_supply += self.mining_reward
        self.pending_transactions = []  # Clear pending transactions
        return new_block

    def mint_token(self, amount, recipient_public_key):
        if self.current_supply + amount > self.max_supply:
            return "Minting failed: Max supply reached."

        mint_transaction = {
            "sender": "System",
            "recipient": recipient_public_key,
            "amount": amount
        }
        self.pending_transactions.append(mint_transaction)
        self.current_supply += amount
        return f"Minted {amount} tokens to {recipient_public_key}."

    def create_transaction(self, sender_wallet, recipient_public_key, amount):
        transaction = {
            "sender": sender_wallet.public_key,
            "recipient": recipient_public_key,
            "amount": amount
        }

        # Sign the transaction
        signature = sender_wallet.sign_transaction(transaction)
        transaction["signature"] = signature.hex()

        # Validate transaction
        if Wallet.verify_transaction(transaction, signature, sender_wallet.public_key):
            self.pending_transactions.append(transaction)
            return "Transaction added successfully!"
        else:
            return "Invalid transaction!"

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Validasi hash blok
            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
