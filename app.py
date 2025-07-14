from flask import Flask, jsonify, request, render_template
import requests
import json
import hashlib
from time import time
from uuid import uuid4

app = Flask(__name__, template_folder='.')
node_address = str(uuid4()).replace('-', '')

# ------------------- Blockchain Class ---------------------
class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')  # Genesis block

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, prev_proof):
        new_proof = 1
        while True:
            hash_op = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_op[:4] == '0000':
                return new_proof
            new_proof += 1

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        prev_block = chain[0]
        for i in range(1, len(chain)):
            block = chain[i]
            if block['previous_hash'] != self.hash(prev_block):
                return False
            if not self.valid_proof(prev_block['proof'], block['proof']):
                return False
            prev_block = block
        return True

    def valid_proof(self, prev, curr):
        hash_op = hashlib.sha256(str(curr**2 - prev**2).encode()).hexdigest()
        return hash_op[:4] == '0000'

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        return self.get_previous_block()['index'] + 1

# Instantiate
blockchain = Blockchain()
peers = set()

# ------------------ Routes --------------------------

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/mine', methods=['GET'])
def mine():
    previous_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(previous_block['proof'])
    blockchain.add_transaction(sender='Network', receiver=node_address, amount=1)
    block = blockchain.create_block(proof, blockchain.hash(previous_block))
    return jsonify({'message': 'Block Mined!', 'block': block}), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    tx = request.get_json()
    required = ['sender', 'receiver', 'amount']
    if not all(k in tx for k in required):
        return 'Invalid transaction data', 400
    idx = blockchain.add_transaction(tx['sender'], tx['receiver'], tx['amount'])
    return jsonify({'message': f'Transaction will be added to Block {idx}'}), 201

@app.route('/chain', methods=['GET'])
def chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200

@app.route('/register', methods=['POST'])
def register_node():
    data = request.get_json()
    node = data.get('node_url')
    if not node:
        return "No URL provided", 400
    peers.add(node)
    return jsonify({'message': 'Node added successfully', 'all_nodes': list(peers)}), 201

@app.route('/sync', methods=['GET'])
def sync():
    longest_chain = blockchain.chain
    max_length = len(longest_chain)

    for peer in peers:
        try:
            res = requests.get(f'{peer}/chain')
            if res.status_code == 200:
                peer_data = res.json()
                peer_chain = peer_data['chain']
                if len(peer_chain) > max_length and blockchain.is_chain_valid(peer_chain):
                    longest_chain = peer_chain
                    max_length = len(peer_chain)
        except:
            continue

    blockchain.chain = longest_chain
    return jsonify({'message': 'Chain synced successfully!', 'current_chain': blockchain.chain}), 200

if __name__ == '__main__':
    import sys
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port)
