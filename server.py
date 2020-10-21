import socket
import threading

PORT =37777
SERVER=socket.gethostbyname(socket.gethostname())
#SERVER="86.120.241.45"
ADDR=(SERVER,PORT)
FORMAT='utf-8'
clients = []
names=[]



server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    #server.bind(ADDR)
    server.bind(ADDR)
except socket.error as e:
    str(e)

def broadcast(msg,client,name):
    for sock in range(len(clients)):
        if clients[sock]!=client:
            print(names)
            message=name+":  "+msg
            clients[sock].send(message.encode())
        else:
            pass

def handle_client(client):
    connected=True
    data = client.recv(2048).decode(FORMAT)
    name=data
    names.append(data)
    while connected:
        try:
            data=client.recv(2048).decode(FORMAT)
            print(data)
        except:
            pass
        if data:
            pass
            broadcast(data,client,name)
    client.close()

def start():
    server.listen()
    print("We are running in "+str(server))
    while True:
        client,client_address=server.accept()
        clients.append(client)
        thread=threading.Thread(target=handle_client,args=(client,))
        thread.start()

print("[STARTING] server is starting...")
start()