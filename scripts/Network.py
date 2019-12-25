import socket

def getIp():
    hostname = socket.gethostname()    
    IPAddr = socket.gethostbyname(hostname)    
    return "Your Computer IP Address is:" + IPAddr

def getComputerName():
    hostname = socket.gethostname()  
    return "Your Computer Name is:" + hostname