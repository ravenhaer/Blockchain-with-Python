# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 10:51:13 2022

@author: ANWESHA
"""

#Importing libraries
import datetime
import hashlib    #this will help generation hash nos. using hash funcs. like the SHA256
import json 
from flask import Flask, jsonify

# Part 1 Building the blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []   #initializing a list with []
    # init is a like the constructor in C++. Self keyword (similar to 'this' keyword in C++. But its a hidden argument in C++. We don't have to call it verytime we create a method) is used in Python to access all instances in a class. Self variable represents the instance of the object itself.
        self.create_block(proof = 1, previous_hash = '0')  #Our genesis block with 0 as hash of prev block
        
    def create_block(self, proof, previous_hash): #This func. creates all the blocks mined after genesis block. Since createblock func. called after mineblock func. , we take the proof of mining as arg. to create a block
        block = {'index' : len(self.chain) + 1,                    #This variable block is a dictionary  with the 4 keys : index is len. of blockchain + 1 because +1 is the index of new block, timestamp calls the datetime module inside datetime library alled at top at the time of block creation and hence the .now(), the last 2 keys take in the arguments of func. create_block we are inside
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash}
        self.chain.append(block) #append the new block reated to the blockhain
        return block
    
    def get_previous_block(self):
        return self.chain[-1]   #-1 is the index of previous block
    
    def proof_of_work(self, previous_proof):
        new_proof = 1 # This is what is commonly called the Nonce. We are calling it new_proof. To solve the proof problem, we will increment new_proof var. at each iteration of while loop until we get right proof/hash no.
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()    #the operation new_proof+prev_proof is symmetrical, i.e., new_proof+prev_proof=prev_proof+new_proof but it must be non-symmetrical otherwise we will get the same hash no. every 2 blocks. So we subtract  the square
            if hash_operation[:4] == '0000':     # :$ will give us first 4 indexes of string hash_operation ,i.e., 0, 1, 2, 3
                check_proof = True
            else:
                new_proof += 1
        
        return new_proof
    #The proof of work is the proof that miners have solved the problem we have created for them. The problem here is the hash no created by sha256 combined with hexdigest() fun should give a headeimal no. that starts with 4 leading zeroes(4 or any no of zeroes set by us); The more leading zeroes, the harder it is for miners to mine a block
  
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()     # .dumps() func. converts the block dictionary into a string so that we can do sha256 operation on it
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
            previous_block =block
            block_index += 1
        return True
    
    #To check the blockchain, we check 2 things: 1. we check every block's hash func. has 4 leading zeroez 2. We see the previous_hash of each block matches hash no. of its prev. block
    
    #Part 2 Mining the Blockchain
    
#Creating a Web App
app = Flask(__name__) 
    
#Creating a Blockchain
    
blockchain = Blockchain() #blockchain is instance of the class Blockchain created above
    
#Mining a new block
#Below we have the GET request to mine a new block
@app.route('/mine_block', methods = ['GET'])  #route() tells Flask which url should trigger our function. inside the route(), the url of the server runs. This url of server is http://127.0.0.1:5000/ but this portion is hidden.  the mine_block is appended after the last '/'   

def mine_block():
   previous_block = blockchain.get_previous_block() #We are calling this func. we created above
   previous_proof = previous_block['proof']
   proof = blockchain.proof_of_work(previous_proof)  #We the proof_of_work puzzle
   previous_hash = blockchain.hash(previous_block)
   block = blockchain.create_block(proof, previous_hash)   #Once we get prrof or the hash no with 4 leading zeroes for the current block, we append it to the blockchain
   response = {'message': 'Congratulations, you just mined a block!',
               'index': block['index'],     #This is the response to the 'GET' request above. We show a UI message on Postman interface in JSON format using var. response here which is a dictionary
               'timestamp': block['timestamp'],
               'proof': block['proof'],
               'previous_hash': block['previous_hash']}  #The words on left of ':' are keys of var. response and on right side we are using keys of block to give value to the keys on left
   return jsonify(response), 200   #200 is standard response for a successful HTTP request
     
#what we do in the mine_block() function above: 1. we find proof of work based on last proof given in last block. 2. Once we get proof, we get the other 3 keys ,i.e., index, timestamp and previous_hash 

#Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,      #The '.chain' on right side is the chain list you can see just below __init__ constructor. It has all the keys,i.e., index, timestamp, proof, previous_hash so we don't have to list them seperately
                'length': len(blockchain.chain)}
    return jsonify(response), 200

#Checking the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def check_chain():
    validity = blockchain.is_chain_valid(blockchain.chain)
    if validity is True:
        response = {'message': 'Blockchain is valid.'}
    else:
        response = {'message': "Yikes! The blockchain is not valid."}
    return jsonify(response), 200

#Running the App
app.run(host = '0.0.0.0', port = 5000)     #"app" object here and above is an instance of Flask class
#Adding the host argument above allows our server to become publicly available
   
  
    
        
  
       