import hashlib
import time
from BlockChainClasses import *
from BlockChainDatabase import *

"""
block is a list of hashstrings
"""

def hash224(object):
    """
    returns the sha224 hash of a string. Pretty safe.
    """
    object = str(object)
    final = hashlib.sha224(object.encode("utf-8")).hexdigest()
    return final
    
    
print(hash224("662d149c0283816f8155eb0cdf6720e6cfd7ca25af7d796237d74505"))
#662d149c0283816f8155eb0cdf6720e6cfd7ca25af7d796237d74505


def customEncrypt(value, key):
    """
    Uses SHA224 to rehash a value (key) times. Used to verify users attempting
    to transfer from another system.
    """
    key = int(key)
    for increment in range(key):
        value = hash224(value)
    return value
    
    
def checkTransferUser(info, token, seed):
    """
    Checks whether a user is a legitamate user from another IP
    """
    if customEncrypt(info, token) == seed:
        return True
    else: return False

"""
Hash function rewards users probabilistically; if hashstring[0:n] (where n is 
the difficulty) is composed solely of zeroes, the block is marked as mined. At
this point, the block is archived, the hash of the block is stored on the chain, 
and the rewards of the block are divided based on user score relative to all other
users' scores on that block. 

Each time a block is mined, the difficulty increases by one. This means that the probabilty of a block being marked "mined" is 1/36^n, where n is the number of blocks previously mined. 

"""

def recursiveMine(block, difficulty, index = 0):
    """
    Recursive proof of work function
    """
    checkset = set()
    hashblock = hash224(block)
    print(hashblock)
    for element in range(difficulty):
        checkset.add(hashblock[element])
        
    if checkset == {"0"}:
        return "Block mined in %i hashes"%index
    
    else: return mine(hashblock, difficulty, index + 1 )

            
def iterativeMine(block, difficulty):
    """
    Iterative proof of work Function.
    """
    index = 0
    isValidBlock = False
    # time0 = time.time()
    
    while isValidBlock == False:
        checkset = set()
        index += 1
        block = hash224(block)
        
        for element in range(difficulty):
            checkset.add(block[element])
        
        if checkset == {"0"}:
            isValidBlock = True
            print(block)
                   
    # time1 = time.time()
    # timetaken = time1-time0
    return (index, block)

def getHashRate():
    """
    returns the hashrate of the system as an integer
    """
    
    time0 = time.time()
    hashes = iterativeMine("TestBlockStringHere", 5)
    time1 = time.time()
    timeTaken = (time1-time0) 
    
    hashRate = hashes[0] / timeTaken
    return hashRate



    
    
    

        
    
    
    