import streamlit as st
import pandas as pd
from dataclasses import dataclass
from datetime import datetime
from typing import Any
import hashlib
from typing import List

@dataclass
class Record:
    sender: str   = ""
    receiver: str = ""
    amount: float = 0

@dataclass
class Block:
    creator_id: int
    prev_hash: str = ""
    hash: any = ""
    nonce : int = 0
    timestamp: str = datetime.utcnow().strftime("%H:%M:%S")
    record: Record = Record()

    def hash_block(self):

        sha = hashlib.sha256()

        data = str(self.record.sender).encode()
        sha.update(data)

        data = str(self.record.receiver).encode()
        sha.update(data)

        data = str(self.record.amount).encode()
        sha.update(data)

        creator_id = str(self.creator_id).encode()
        sha.update(data)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        self.hash = sha.hexdigest()

        return self.hash

@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4
    def add_block(self, block):
        self.chain += [block]
    def proof_of_work(self, block):
        calculated_hash = block.hash_block()
        num_of_zeros = "0"*self.difficulty

        while not calculated_hash.startswith(num_of_zeros):
            block.nonce += 1
            calculated_hash = block.hash_block()

        return block
    def is_valid(self): # function validates the entire chain, not potential new block
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block.prev_hash != block_hash:
                st.write("The chain is not valid")
                return False
            block_hash = block.hash_block()
        st.write("Chain is valid")
        return True

input_sender = st.text_input("Enter sender address", key=1)
input_receiver = st.text_input("Enter receiver address", key=2)
input_amount = 0
try:
    input_amount = float(st.text_input("Enter amount to send", key=3))
except:
    st.write("please enter a numeric for amount")

@st.cache(allow_output_mutation=True)
def setup():
    block = Block( 0,"","000" )
    block.hash_block()
    return PyChain([block])

diff = st.slider("Select Difficulty", min_value=1, max_value=5)

if st.button("Send Transaction") and input_amount > 0:
    pychain = setup()
    pychain.difficulty = diff
    prev_block = pychain.chain[-1]
    record = Record(input_sender, input_receiver, input_amount)
    block = Block( creator_id=prev_block.creator_id+1,
                  prev_hash=prev_block.hash_block(), record=record)
    block = pychain.proof_of_work(block)
    if pychain.is_valid():
        pychain.add_block(block)
    pychain_df = pd.DataFrame(pychain.chain)
    st.write(pychain_df)
    st.write(pychain_df.record)




