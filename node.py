from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine', methods=['POST'])
def mine():
    miner_address = request.json.get("miner")
    if not miner_address:
        return jsonify({"error": "Miner address is required"}), 400
    block = blockchain.mine_block(miner_address)
    return jsonify({"message": "Block mined!", "block": block.__dict__}), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return jsonify({"length": len(chain_data), "chain": chain_data}), 200

if __name__ == '__main__':
    app.run(port=5000)
