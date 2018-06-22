import socket
import sys
from BlockChainFunctions import *
from BlockChainDatabase import *
from _thread import *

def main():
    host = ""
    port = 5556
    
    numUsers = 10
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.bind((host,port))
    except socket.error as error:
        sock.close()
        print("Port in use... Process will be terminated")
        exit()
    
    sock.listen(numUsers)
    print("Node Online...Accepting up to %i user(s) " %(numUsers))
    
    # miner = MineWrapper(super)
    # miner.make()
    
    def clientThread(connection):
        """
        Threading Function for sockets:
        allows users to each create an independent instance of the serverside program.
        
        Additional Notes: see BlockChainFuntions for more indepth info on commands
        """
        
        connection.send(str.encode("""
    Welcome to the CMU Virtual Economy Client
    """))
        connection.send(str.encode("""
    Type 'help' for a list of commands.
    """))
        connection.send(str.encode("""
        
    What would you like to do?
            
    """))
        currentUser = 0 #initiating current user. This is the easiest way to save this
        #info across a session.
        
        while True:
            data = connection.recv(1024)
            data.decode('utf-8')
            if not data :
                break
            
            #quits if user inputs quit command
            elif str(data) == "b'quit\\r\\n'":
                print("Client %s Disconnected." %addr[0])
                reply = "bye!"
                break
            elif str(data) == "b'logout\\r\\n'":
                currentUser = 0
                reply = """
    You have been logged out.
    
    """
            
            #logs in if user inputs login command
            elif str("login(") in str(data):
                if currentUser == 0:
                    try:
                        stripped = []
                        datastr = getParenthesisContents(data)
                        dataList = datastr.split(",")
                        for element in dataList:
                            element.strip()
                            stripped.append(element)
                            
                        if isValidLogin(dataList[0],dataList[1]):
                            currentUser = getUserFromDatabase(stripped[0])
                            name = str(currentUser.getFirst())
                            reply = """
    Welcome, %s.
            
    Type 'help' for a list of commands.
            
    """%name
                            if not currentUser == 0:
                                print(currentUser)
                            else: print("none")
                            
                            
                        else:
                            print(hash224(stripped[1]))
                            reply = """
    Invalid login. Please try again.
            
    """
                    except:
                            reply = """
    Invalid login. Please try again.
            
    """
                else: reply = """
    You are already logged in!
        
    """
    
            else: 
                print(currentUser)
                if currentUser is 0:
                    print("New operation performed by %s" %(addr[0]))
                    reply = interpretData(data)
                else: 
                    sessionUser = currentUser.getScreenName()
                    print("New operation performed by %s"%sessionUser)
                    reply = userCommands(data, currentUser)
        
            # if str(data) == "b'quit\\r\\n'":
            #     print("Client %s Disconnected." %addr[0])
            #     break
            # 
            # dataHash = hash(data)
            # dataHash = str(dataHash)
            # reply = "Hash: "+dataHash+"\n"
            # 
    
            connection.send(str.encode(reply))
        
        connection.close()
    
    
    while True:
        connection, addr = sock.accept()
        print("Connected to: %s: %s" %(addr[0], str(addr[1])))
        start_new_thread(clientThread,(connection,))
        
if __name__ == "__main__":
    main()

    

