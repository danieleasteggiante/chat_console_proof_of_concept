import socket
import time
from threading import Thread

host='0.0.0.0'
port=8085

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(5)
print("Server Waiting for connections")
connections = {}

def acceptClients():
    c, addr = sock.accept()
    print("Connection from " , addr)
    c.send("Sei entrato in chat, ".encode('utf8'))
    c.send("inserisci tuo nome: ".encode('utf8'))
    nome = c.recv(1024).decode()
    print(nome)
    connections[nome]=[]
    connections[nome].append(c)
    connections[nome].append(addr)
    if len(connections)>0:
        startChat(c, nome)
    else:
        c.send("Errore contattare l'amministratore di sistema ".encode('utf8'))

def startChat(c, myname):
    global connections

    while len(connections)<2:
        c.send("sei solo attendi che si connetta qualcuno ".encode('utf8'))
        time.sleep(1)

    while len(connections[myname]) < 3:
        choosePerson(c, myname)

    chat1to1(connections[myname][0], connections[connections[myname][2]][0], myname)


def choosePerson(conn, nome):
    global connections
   
    conn.send("Scegli con chi ti vuoi connettere: ".encode('utf8'))
    listP = createListUsers(connections)
    conn.send("Lista utenti: ".encode('utf8'))
    conn.send(str(listP).encode('utf8'))

    control= True
    
    while control:
        withname = conn.recv(1024).decode()
        
        if withname == "lista":
            conn.send("Lista utenti: ".encode('utf8'))
            conn.send(str(listP).encode('utf8'))
            pass
        
        else:
            for key in connections:
                if key == withname:
                    if withname == nome:
                        conn.send(f"Non puoi scegliere te stesso".encode('utf8'))
                        break

                    conn.send(f"**Hai scelto {withname} ".encode('utf8'))
                    connections[nome].append(withname)
                    invite(nome, withname)
            
        if len(connections[nome])>2 :
            control = False
            break

def invite(nome, withName):
    global connections
    
    while True:

        connections[withName][0].send(f"{nome} si vuole connettere con te accetti? * si o no *".encode('utf8'))
        risposta = connections[withName][0].recv(1024).decode()

        if risposta == "si":
            connections[withName].append(nome)
            connections[withName][0].send(f"**Ti sei connesso con: {nome}".encode('utf8'))
            break

        elif risposta == "no":
            connections[nome].pop(2)
            connections[nome][0].send(f"{withName} ha rifiutato la connessione ".encode('utf8'))
            break

        else:
            continue

def createListUsers(dictP):
    listP = []
    for key in dictP:
        listP.append(key)
    return listP

def chat1to1(p1,p2, myname):
    global connections
    p1.send("Per uscire dalla chat: digitare '#quit' ".encode('utf8'))
    while True:
        msg=p1.recv(1024).decode()
        if msg == "#quit":
            p2.send(msg.encode('utf8'))
            connections[myname].pop(2)
            startChat(p1, myname)
            break

        p2.send(msg.encode('utf8'))

if __name__ == "__main__":
    i=0
    while len(connections) < 5 and i < 5:
        try:
            Thread(target=acceptClients, args=connections).start()
            i +=1
        except:
            print('Bo')
