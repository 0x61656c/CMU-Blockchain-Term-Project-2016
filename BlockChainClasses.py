import hashlib

class Block(object):
    """
    Info:
        Data structure for Blocks of transactions
        
        Holds information on the finite number of transactions that take
        place in a given period
        
    Methods:
        Builtin: 
            init(constructor), repr()/str(), 
        
        Custom:
            getBlock : returns the respective block number
            length : returns the number of transactions in the block
    
    Additional Comments:
        -Going to add hashing later. Not sure whether I want to do this with an
        aggregated hashString or with individual smaller hashes.
    """
    def __init__(self, transactionList):
        self.block = transactionList
        self.numberOfTransactions = len(self.block)
    
    def __repr__(self):
        return """<Block Object: %i entries> """%self.numberOfTransactions
    
    def getBlock(self):
        return self.block

    def length(self):
        return self.numberOfTransactions
    
    def newTransaction(self, transaction):
        self.block.append(transaction)
        self.numberOfTransactions += 1
        
class User(object):
    """
    Info:
        data structure for identifying individual users.
    
    Methods:
        Builtin: repr(),hash(),equality(),
    
        Custom: 
            getInfo(self): returns more indepth info based on self.screeName
        
    Additional comments:
        -hash and equality only check username, since other values are 
        likely to be repeated in large databases.
    """
    def __init__(self, firstName, lastName, screenName, password, email, balance = 0):
        self.firstName = firstName
        self.lastName = lastName
        self.password = password
        self.screenName = screenName
        self.balance = balance
        self.email = email
    
    def __repr__(self):
        return """<User %s; Balance: %i>"""%(self.screenName, self.balance)
    
    def __hash__(self):
        return hash(self.screenName)
    
    def __eq___(self, other):
        return hash(self.screenName) == hash(other.screenName)
    
    def getTokenString(self):
        return "%s/%s/%i/%s/%s"%(self.firstName, self.lastName, self.balance, 
        self.screenName, self.email)
    
    def getFirst(self):
        return self.firstName
    
    def getLast(self):
        return self.lastName
    
    def getBalance(self):
        return self.balance
        
    def getInfo(self):
        return (self.firstName, self.lastName, self.email)
    
    def getScreenName(self):
        return self.screenName
    
    def getPassword(self):
        return self.password
        
    def getEmail(self):
        return self.email
        
    def buy(self, quantity):
        self.balance += quantity
    
    def sell(self, quantity):
        self.balance -= quantity
    
class Transaction(object):
    """
    Info:
        Data structure for transaction instances
        
        Base data structure for blockchain.
        Holds info on individual transactions.
        Subclass of User.
    
    Methods: 
        Builtin:
            init(constructor),repr() / str(), eq(), hash()
        
        Custom:
            getTime, getIndex, getLastHash, getTransactionInfo
            (each is self descriptive)
    
    Additional Comments:
        -Remember to change terminology later
        -Will also be updated with better hash functions.
        
    """
    def __init__(self, index, time, buyer, seller, quantity, lastTransactionHash = None):
        self.index = index
        self.time = time
        self.seller = seller
        self.buyer = buyer 
        self.quantity = quantity
        self.lastHash = lastTransactionHash
        
        
        self.hashString = str(self.index) + "/" +\
        str(self.time) + "/" +\
        str(self.buyer) + "/" + \
        str(self.seller) + "/" +\
        str(self.quantity) + "/" +\
        str(self.lastHash)
    
    def __repr__(self):
        return """<Transaction: %s received %i units from %s at %s> """\
        %(self.buyer, self.quantity, self.seller, self.time)
    
    def __hash__(self):
        return hash(self.hashString)
    
    def __eq__(self, other):
        return hash(self) == hash(other)
        
    def getTime(self):
        return self.time
        
    def getIndex(self):
        return self.index
    
    def getLastHash(self):
        return self.lastHash
    
    def getTransactionInfo(self): 
        return (buyer, seller, quantity)
        
    def getHashString(self):
        return self.hashString
    
class MineWrapper(object):
    
    def __init__(self, user, start = 1, end = 2):
        self.user = user
        self.start = start
        self.end = end
    
    def make(self):
        balance = self.user.getBalance()
        mine(self.start, self.end)
        self.start += 1
        self.end += 1
        superUser.buy(1)
        updateTransferSQL(self.user, balance + 1)
        
    
    
def mineWrapper(superUser):
    
    start = 1
    end = 2
    
    while True:
        mine(start, end)
        start += 1
        end += 1
        superUser.buy(1)
    

    




    
    