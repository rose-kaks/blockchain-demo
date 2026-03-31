import hashlib
import time
import json
from datetime import datetime

class Block:
    def __init__(self, index, previous_hash, data):
        self.index = index
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "data": self.data,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty=2):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), previous_block.hash, data)
        new_block.mine_block(difficulty=2)  # Very easy difficulty for demo
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def print_chain(self):
        for block in self.chain:
            print("\n--- Block", block.index, "---")
            print("Timestamp:", block.timestamp)
            print("Data:", block.data)
            print("Previous Hash:", block.previous_hash)
            print("Hash:", block.hash)
            print("Nonce:", block.nonce)

# ========================
# Demo / Test
# ========================
if __name__ == "__main__":
    print("Creating a simple blockchain...\n")
    
    my_blockchain = Blockchain()
    
    print("Adding Block 1: Alice sent 10 coins to Bob")
    my_blockchain.add_block({"from": "Alice", "to": "Bob", "amount": 10})
    
    print("\nAdding Block 2: Bob sent 5 coins to Charlie")
    my_blockchain.add_block({"from": "Bob", "to": "Charlie", "amount": 5})
    
    print("\nBlockchain:")
    my_blockchain.print_chain()
    
    print("\nIs blockchain valid?", my_blockchain.is_chain_valid())
    
    # Tamper with data to demo security
    print("\nTampering with Block 1 data...")
    my_blockchain.chain[1].data = {"from": "Alice", "to": "Bob", "amount": 1000}
    print("Is blockchain still valid after tampering?", my_blockchain.is_chain_valid())