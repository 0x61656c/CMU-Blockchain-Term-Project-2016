import hashlib
import random
from BlockChainClasses import *
from BlockChainDatabase import *
from BlockChainMining import * 
from BlockChainTransacting import *

def createTransferUser(first, last, balance, password, email, screenName):
    newUser = User(first, last, screenName, password, email, balance)
    return newUser

def isValidLogin(username, password):
    """
    Function that checks whether login info is valid. Takes username and pass
    as parameters
    
    Additional notes:
    
    """
    check = getUserFromDatabase(username)
    print(check.getPassword())
    passwordAttempt = hash224(password)
    print(passwordAttempt)
    return check.getPassword() == passwordAttempt
    

def getParenthesisContents(string):
    """
    Returns text inside parenthesis of a string
    """
    string = str(string) #covers case in which input is not a string
    a = string.find("(") + 1
    b = string.find(")")
    return string[a:b]
    
def interpretData(data):
    print(str(data))
    
    verifyRegistrationNext = False
    verifyRegistration = False
    
    if "verify(" in str(data):
        datastr = getParenthesisContents(data)
        dataList = str(datastr).split(",")
        for element in dataList:
            print(element)
        if len(dataList) == 5:
            try:
                first = dataList[0]
                print(first)
                last = dataList[1]
                screen = dataList[2]
                password = dataList[3]
                email= dataList[4]
    
    
                newUser = User(first, last, screen, password, email)
                print(newUser)
    
                newUserDBEntry(newUser)
                
                reply = """
    Registration Successful.
        
    """
            except: reply = """
    Invalid input(s). Please Try again.
            
    """
           
        else: 
            reply = """
    Invalid input(s). Please Try again.
            
    """
    
    elif str(data) == "b'login\\r\\n'":
        reply = """
    To log into an existing account, please submit a comma seperated list
    of the following attributes inside the login() command in the following
    format. 
    
                        login(username, password)
                        
    If you've forgotten your password, email alebel@cmu.edu to submit a request.
    Even in such an instance, passwords cannot be recovered without personally 
    meeting with proof of identity.
    
    """

    elif str(data) == "b'help\\r\\n'":
        reply = """
  #################################################################################
    The help function will be more helpful once you log in. 
    
    Top Level Commands:
    
    'help' - Did you mean: Recursion?
    
    'login' - Login to an existing account
    'register' - Register for a new account
    'quit' - Exit the current session
    
    'insertToken' - Insert a token from another node. Used to transfer funds 
    between nodes, or keep assets in cold storage.
  #################################################################################
  
    """
    else:
        if str(data) == "b'register\\r\\n'":
            reply = """ 
    Please enter a comma seperated list of the following attributes inside
    the verify() command in the following format.
        
    verify(FirstName, LastName, UserName, Password, EmailAddress)
    
    Your submission will be rejected if it contains special characters
    or phrases deemed dangerous. This is to prevent SQL injection attacks.
    
    Passwords are not stored on a database and thus cannot be recovered.
        
    """
    
        elif str(data) == "b'transfer\\r\\n'" or "send(" in str(data) or "balance" in str(data) or "getToken" in str(data) or "getHashRate" in str(data):
            reply = """
    You are not logged on! 
        
    """
        elif str(data) == "b'insertToken\\r\\n'":
            reply = """
    Please input the info you were given inside the insert() command in a tuple 
    of the following format:
            
    insert(Token, Key, Seed, Password)
    
    I've included a suite of protection measures to prevent the abuse of this feauture.
    If you attempt to do so, your account will be deleted and your existing funds will be permanently irretrievable.
    
    """
    
        elif str("insert(") in str(data):
            # try:
            data = getParenthesisContents(data)
            dataList = data.split(",")
            
            info = dataList[0]
            token = dataList[1]
            key = dataList[2]
            password = dataList[3]
            
            if checkTransferUser(info, token, key):
                    info = info.split("/")
                    # strippedInfo = []
                    # 
                    # for element in info:
                    #     newElement = element.strip()
                    #     strippedInfo.append(newElement)
                    
                    first = info[0]
                    last = info[1]
                    balance = info[2]
                    screenName = info[3]
                    email = info[4]
                    
                    newUser = createTransferUser(first, last, balance, password, email, screenName)
                    newTransferUserDBEntry(newUser)
                    reply = """
    User added to local system. You may now log on.

    """
            else:
                reply = """
    Your token has been rejected. Please try again.
        
        """
        
        else: 
            print(str(data))
            reply = """
    Unknown/Invalid Command
        
    """
    return reply

   
def userCommands(data, user):
    """
    Interprets data for logged in users. 
    
    Takes user commands and session user as inputs
    
    Additional Notes:
        -Kept seperate from interpretdata(data) because it was easier to keep 
        threads untangled this way. Repeatedly updating the user from a none value 
        was redundant and annoying.
        -User parameter is an instance of the user class
    """
    sessionUser = user.getScreenName()
    print(str(data))
    if str(data) == "b'balance\\r\\n'":
        currentBalance = user.getBalance()
        reply = """
    Your current balance is %i units
    
    """%currentBalance
    
    elif str(data) == "b'transfer\\r\\n'":
        reply = """
    Please enter a tuple of the quantity and the username of the recipient
    inside the send() command in the following format:
                        
    send(funds, recipient)
    
    """
    
    elif str(data) == "b'help\\r\\n'":
        reply = """
  #################################################################################
    Top Level Commands:
    
    'help' - Did you mean: Recursion?
    
    'balance' - Check your current balance
    'transfer' - Transfer funds
    'logout' - Log out of the current session
    'quit' - Exit the current session
    
    'generateToken' - Information for bringing funds to other nodes. Encrypts your
    data before transferring it to another node. On generating a token, key, and 
    seed, your local account information will be deleted. Proceed with caution.
    
    'getHashRate' - Returns the hashrate of the node. For SuperUsers only.
  #################################################################################
    
    """
    
    elif "send(" in str(data):
        
        refdata = getParenthesisContents(data)
        dataList = refdata.split(",")
        try:
            sender = getUserFromDatabase(sessionUser)
            recipient = getUserFromDatabase(str(dataList[1]).strip())
            sendUser = sender.getScreenName()
            recipientUser = recipient.getScreenName()

        
            transaction = transferFunds(sendUser, recipientUser, int(dataList[0]))
            transactionDBEntry(transaction)
            
            newbalance = sender.getBalance()
            reply = """
    You have sent %i units to %s. 
    Your new balance is %i.  
    
    """  %(int(dataList[0]), str(dataList[1]), newbalance - int(dataList[0]))
    
        except:
            reply = """
    Invaid inputs. Please Try again.
    """
        
    
    elif str(data) == "b'getHashRate\\r\\n'":
        if sessionUser == "Server":
            hashRate = getHashRate()
            reply = """
    Current hashrate is %i hashes per second
        
    """%hashRate
        else: reply =  """
    Only the super user can check the hashrate
    
    """
        
    
    elif str(data) == "b'generateToken\\r\\n'":
        ts = user.getTokenString()
        deleteKey = user.getScreenName()
        key = random.random()
        key *= 10
        key = int(key)
        
        hashstring = customEncrypt(ts, key)
        deleteUserFromDB(deleteKey)
        
        reply = """
    Your account has been deleted from this node.
    Keep the following information safe and confidential until your new instance 
    is created. Only one instance of an account can exist at a time.
    
    Token:%s
    Key:%i
    Seed:%s
    
    If you lose your information, your account will be permanently lost.
    
    """%(ts, key, hashstring)
    
    else:
    
        reply = """
    Unknown/Invalid Command
            
    """                
    
    return reply
    
