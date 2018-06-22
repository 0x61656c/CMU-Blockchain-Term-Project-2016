from BlockChainClasses import *
from BlockChainDatabase import * 
from BlockChainMining import *

import datetime
import sqlite3

def getUserCopy(username):
    """
    Function designed to pull user information from database.
    
    Additional Notes: also will be used for checking whether a username is taken.
    This copy was made because the code wasn't working without it. It was easier to paste than
    to restructure.
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
    
def updateTransferSQLCopy(username, newBalance):
    """
    Copy of the same function from another file.
    Notes: See above for explanation. Threads are hard to untangle, okay? ;(
    """
    conn = sqlite3.connect("/Users/aalebel33/Desktop/BlockChain Dependencies/BCDB.db")
    c = conn.cursor()
    connectionString = "UPDATE testUsers1 SET balance = %i WHERE screenName = '%s'"%(newBalance, username)
    print(connectionString)
    c.execute(connectionString)
    conn.commit()
    conn.close()
    
def transferFunds(sender, receiver, amount):
    sender = getUserCopy(sender)
    receiver = getUserCopy(receiver)
    time = datetime.datetime.now().time()
    take = sender.getBalance()
    print(take)
    print(take-amount)
    if take - amount > 0:
        
        
        sender.sell(amount)
        newSenderBalance = sender.getBalance()
        updateTransferSQLCopy(sender.getScreenName(), newSenderBalance)
        
        receiver.buy(amount)
        newReceiverBalance = receiver.getBalance()
        updateTransferSQLCopy(receiver.getScreenName(), newReceiverBalance)
        
        print("Done")
        return Transaction(0, time, receiver, sender, amount)
    
    else:
        print("Insufficient Funds")
        

        
    
        