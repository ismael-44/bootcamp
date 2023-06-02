import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse


class blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()
    
    def add_node(self,address,):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        # We will define as network the set of nodes that we have obtained
        network = self.nodes
        print(len(network))
        # We give the value of None to the variable longest_chain
        longest_chain = None
        # We define the maximum length of our chain of blocks
        max_length = len(self.chain)
        # We go through  all the nodes
        print(max_length)
        for node in network:
            response = requests.get(f'http://{node}/chain')
            print(node)
            print(response.status_code)
            json_obj = response.json()
            if isinstance(json_obj,dict):
                print("hey")
                if "length" in json_obj:
                    print(json_obj["length"])
                if "chain" in json_obj:
                    print(json_obj["chain"])
            if response.status_code == 200:
                length = json_obj["length"]
                print(length)
                chain = json_obj["chain"]
                print(chain)
                # In case of the maximun length is more than maxlenght and is valid
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
            if longest_chain:
                self.chain =longest_chain
                return True
            return False
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain)+1,
                'timestamp':str(datetime.datetime.now()),
                'proof':proof,
                'previous_hash':previous_hash,
                'transactions' : self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block
    
    def add_transaction(self, sender, reciver, amount):
        self.transactions.append({'sender':sender,
                                  'reciver':reciver,
                                  'amount':amount})
        previous_block = self.get_previous_block()
        return previous_block['index']+1
    
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof +=1
        return new_proof
        
    def hash(self,block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    

app = Flask(__name__)

node_address = str(uuid4()).replace('-','')



blockchain = blockchain()

@app.route('/mine_block', methods=['GET'])

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender= node_address, reciver = 'Eric', amount=1)
    block = blockchain.create_block(proof, previous_hash)
    response = {"message":"Congrats! You've mined a block",
                "index":block["index"],
                "timestamp":block["timestamp"],
                "proof":block["proof"],
                "transactions":block["transactions"],
                "previous_hash":block["previous_hash"]}
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length' : len(blockchain.chain)}
    return jsonify(response),200


@app.route('/verify', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': "La cadena es valida"}
    else:
        response = {'message': "El blockchain es invalido"}
    return jsonify(response), 200


@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender','reciver','amount']
    if not all (key in json for key in transaction_keys):
        return 'Some transaction element are empty', 400
    index = blockchain.add_transaction(json['sender'],json['reciver'],json['amount'])
    response = {'message':f'Adding transaction to block {index}'}
    return jsonify(response), 201

@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No node found', 401
    for node in nodes:
        blockchain.add_node(node)
    response = {'message':'All nodes found has been added succesfully. The black coin are now running on all this nodes:',
                'total_nodes':list(blockchain.nodes)}
    return jsonify(response), 201

@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {
            'message': 'The chain has been replaced by the longest',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'The chain is the longest',
            'actual_chain': blockchain.chain
        }
    return jsonify(response), 200

app.run(host="0.0.0.0", port = "5001")