import hashlib
import time

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

class Blockchain:
    def __init__(self, difficulty=4, max_supply=50000000):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.mining_reward = 50
        self.current_supply = 0
        self.max_supply = max_supply

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def mine_block(self, miner_address):
        if self.current_supply >= self.max_supply:
            return "Max supply reached. Mining stopped."

        data = {"reward": self.mining_reward, "to": miner_address}
        new_block = Block(
            len(self.chain),
            self.get_latest_block().hash,
            time.time(),
            data
        )

        while not new_block.hash.startswith("0" * self.difficulty):
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()

        self.chain.append(new_block)
        self.current_supply += self.mining_reward
        return new_block
