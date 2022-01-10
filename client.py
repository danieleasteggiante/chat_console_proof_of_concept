import socket
from threading import Thread

host='192.168.0.111'
port=8085

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

i=0
nameConnection= ""

def receiveMsg():
    global i
    global nameConnection
    while True:
        msg = sock.recv(1024).decode('utf8')
        
        if "? * si o no *" in msg:
            sock.send(bytes(".",'utf8'))
        
        if msg =="#quit" and i<2:
            i+=1
            sock.send(bytes(msg, "utf8"))
            nameConnection=""
            
        if "**Ti sei connesso con" in msg:
            sock.send(bytes(".",'utf8'))
            nameConnection=msg[23:] + " : "
        
        if "**Hai scelto" in msg:
            sock.send(bytes(".",'utf8'))
            nameConnection=msg[13:] + " : "
        
        if "Lista utenti:" in msg:
            i=0

        if "**Ti sei connesso" in msg or "**Hai scelto" in msg or "Per uscire dalla chat: digitare '#quit'" in msg:
            print(msg)
        else:
            print(nameConnection + msg)


def sendMsg():
    global i
    global nameConnection

    while True:
        response = input()
        if response == "#quit":
            i=0
            nameConnection=""

        sock.send(bytes(response,'utf8'))

t1=Thread(target=receiveMsg)
t2=Thread(target=sendMsg)
t1.start()
t2.start()
