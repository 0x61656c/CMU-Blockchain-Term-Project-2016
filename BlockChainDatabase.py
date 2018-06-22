import sqlite3
import hashlib
from BlockChainClasses import *
from BlockChainMining import *
from BlockChainIntegratedMining import * 

####
#DB Initialization
####

conn = sqlite3.connect("/Users/aalebel33/Desktop/BlockChain Dependencies/BCDB.db")
#allows filenames as input, but :memory uses RAM

c = conn.cursor() #Allows for sql commands
"""
#creates test table

c.execute("CREATE TABLE TestUsers1(\
            'first' TEXT,\
            'last' TEXT,\
            'balance' INTEGER,\
            'screenName' TEXT,\
            'password' TEXT,\
            'email' TEXT")) #documentation says use docstring"""
###

#creates user table
"""
c.execute(CREATE TABLE Users(\
            'first' TEXT,\
            'last' TEXT,\
            'balance' INTEGER,\
            'screenName' TEXT,\
            'password' TEXT,\
            'email' TEXT)
"""
###

#creates transaction table

#c.execute("CREATE TABLE Transactions('TransactionHash' text)")


###
#Helper Functions
###

def isLegalFields(L):
    """
    Function that checks a list for banned tokens.
    
    Additional Notes:
        -must take a list as input
        -used to prevent sql injection
        -doesnt check password because the value is hashed anyway, which
        mitigates the probability of injection.
        -Disabled for testing
    """
    bannedTokens = "!\#$\%&()*+,-./:;<=>?[\\]^_{|}~"

    
    for entry in L:
        for char in bannedTokens:
            if char in entry: 
                return False
    return True
        
            
###
#DB modification
###
def newUserDBEntry(user):
    """
    Function designed to insert class instances of users to an associated SQLite
    database.
    
    Additional Notes: 
        must be running in the same thread as the associated SQLite db connection
    """
    conn = sqlite3.connect("/Users/aalebel33/Desktop/BlockChain Dependencies/BCDB.db")
    c = conn.cursor()
    first = user.getFirst()
    last = user.getLast()
    #balance = user.getBalance() [not needed because new wallets will always
    #start with zero
    screen = user.getScreenName()
    password = user.getPassword()
    hashPass = hashlib.sha224(password.encode("utf-8")).hexdigest()
    email = user.getEmail()
    fieldList = [first, last, screen, email]
    connectionString = """INSERT INTO TestUsers1 VALUES ('%s', '%s', 0 , '%s', '%s', '%s')"""\
    %(first.strip(), last.strip(), screen.strip(), hashPass.strip(), email.strip())
    print(connectionString)
            
    if isLegalFields(fieldList):##(indent next line)
        c.execute(connectionString)
    else: 
        c.execute(connectionString)
        #print("Nope") #disable for testing
    conn.commit()
    conn.close()

# c.execute("SELECT * FROM users WHERE screenName = 'Master'")
# print(c.fetchone())
#c.fetchmany(n) returns n rows as list
#c.fetchall() returns remaining rows as list or emptylist if none
# print(c.fetchone())

    
def newTransferUserDBEntry(user):
    """
    Function designed to insert class instances of users to an associated SQLite
    database.
    
    Additional Notes: 
        must be running in the same thread as the associated SQLite db connection
    """
    conn = sqlite3.connect("/Users/aalebel33/Desktop/BlockChain Dependencies/BCDB.db")
    c = conn.cursor()
    first = user.getFirst()
    last = user.getLast()
    #balance = user.getBalance() [not needed because new wallets will always
    #start with zero
    screen = user.getScreenName()
    password = user.getPassword()
    balance = user.getBalance()
    hashPass = hashlib.sha224(password.encode("utf-8")).hexdigest()
    email = user.getEmail()
    fieldList = [first, last, screen, email]
    connectionString = """INSERT INTO TestUsers1 VALUES ('%s', '%s', %i , '%s', '%s', '%s')"""\
    %(first.strip(), last.strip(), int(balance), screen.strip(), hashPass.strip(), email.strip())
    print(connectionString)
    
    if isLegalFields(fieldList):##(indent next line)
        c.execute(connectionString)
    else: 
        c.execute(connectionString)
        #print("Nope") #disable for testing
    conn.commit()
    conn.close()

# c.execute("SELECT * FROM users WHERE screenName = 'Master'")
# print(c.fetchone())
#c.fetchmany(n) returns n rows as list
#c.fetchall() returns remaining rows as list or emptylist if none
# print(c.fetchone())


def getUserFromDatabase(username):
    """
    Function designed to pull user information from database.
    
    Additional Notes: also will be used for checking whether a username is taken.
    """
    conn = sqlite3.connect("/Users/aalebel33/Desktop/BlockChain Dependencies/BCDB.db")
    c = conn.cursor()
    
    connectionString = "SELECT * FROM TestUsers1 WHERE screenName = '%s'"%username
    print(connectionString)
    c.execute(connectionString)
    data = c.fetchone()
    print(data)
    
    conn.commit()
    conn.close()

    first = data[0]
    last = data[1]
    balance = data[2]
    screen = data[3]
    password = data[4]
    email = data[5]
    
    user = User(first, last, screen, password, email, balance)
    return user

def updateTransferSQL(username, newBalance):
    conn = sqlite3.connect("/Users/aalebel33/Desktop/BlockChain Dependencies/BCDB.db")
    c = conn.cursor()
    connectionString = "UPDATE testUsers1 SET balance = %i WHERE screenName = '%s'"%(newBalance, username)
    print(connectionString)
    c.execute(connectionString)
    conn.commit()
    conn.close()

def deleteUserFromDB(username):
    conn = sqlite3.connect("/Users/aalebel33/Desktop/BlockChain Dependencies/BCDB.db")
    c = conn.cursor()
    connectionString = "DELETE FROM TestUsers1 WHERE screenName = '%s'"%(username)
    print(connectionString)
    c.execute(connectionString)
    conn.commit()
    conn.close()

def transactionDBEntry(transaction):
    transHashable = transaction.getHashString()
    transHash = hash224(transHashable)
    conn = sqlite3.connect("/Users/aalebel33/Desktop/BlockChain Dependencies/BCDB.db")
    c = conn.cursor()
    connectionString = "INSERT INTO Transactions VALUES ('%s')"%(transHash)
    print(connectionString)
    c.execute(connectionString)
    conn.commit()
    conn.close()
    
def getLastBlock():
    conn = sqlite3.connect("/Users/aalebel33/Desktop/BlockChain Dependencies/BCDB.db")
    c = conn.cursor()
    
    connectionString = "SELECT * FROM Transactions ORDER BY ROWID DESC LIMIT 1"
    
    c.execute(connectionString)
    data = c.fetchone()
    conn.commit()
    conn.close()
    
    return data


def getSuperUser():
    # conn = sqlite3.connect("/Users/aalebel33/Desktop/BlockChain Dependencies/BCDB.db")
    # c = conn.cursor()
    # 
    # connectionString = "SELECT * FROM TestUsers1 WHERE screenName = 'Server'"
    # 
    # c.execute(connectionString)
    # data = c.fetchone()
    # conn.commit()
    # conn.close()
    # 
    super = getUserFromDatabase("Server")
    return super
    

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
    
def operator():    
    
    operate = True
    user = getUserFromDatabase("Server")
    start = 1
    end = 2
    
    while operate == True:
        balance = user.getBalance()
        if end == 36:
            operate = False
        else:
            mine(start, end)
            start += 1 
            end += 1
            user.buy(1)
            updateTransferSQL("Server", balance +1)
    
    
    

