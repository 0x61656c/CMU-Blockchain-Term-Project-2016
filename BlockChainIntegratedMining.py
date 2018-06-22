from BlockChainClasses import *
from BlockChainTransacting import *
from BlockChainFunctions import *
from BlockChainDatabase import *


# t0 = Transaction(0, 0, "aalebel33", "pmielke", 100)
# hs0 = t0.getHashString
# 
# block = Block([hs0])
# 
# print(block)
# block.newTransaction(t0)
# 
# print(block)
# 
# u1 = getUserFromDatabase("aalebel33")
# u2 = getUserFromDatabase("pmielke")
# 
# transferFunds(u1, u2, 50)

"""
Preventing inflation:

4,294,967,296 IPV4 possible IPV4 addresses


"""
    
"""
This file is for experimentation

def hashCash(block, startDiff, endDiff):
    score = 0
    for difficulty in range(startDiff, endDiff):
        
        increment = 0
        print(difficulty)
        
        miner = iterativeMine(block, difficulty)
        index = miner[0]
        seed = miner[1]
        
        while not customEncrypt(block,increment) == seed:
            increment += 1
            
    return increment
        
def mine(start, end):
    block = getLastBlock()
    hashCash(block, start, end)
"""
        