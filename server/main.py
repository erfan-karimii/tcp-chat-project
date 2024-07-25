import socket
import threading


# Connection Data
HOST = '127.0.0.1'
PORT = 55555

# Starting Server
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((HOST, PORT))
SERVER.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
SUPER_USERS_LIST = {'erfan':"94aefb8be78b2b7c344d11d1ba8a79ef087eceb19150881f69460b8772753263"}




def add_user(client):
    # Request And Store Nickname
    nickname = client.recv(1024).decode('ascii')
    nicknames.append(nickname)
    clients.append(client)

    # Print And Broadcast Nickname
    print("Nickname is {}".format(nickname))
    broadcast_for_others(client,"{} joined!".format(nickname).encode('ascii'))

    



# Sending Messages To All Connected Clients
def broadcast_for_others(sender,message):
    for client in clients:
        if client != sender:
            client.send(message)


# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast_for_others(client,message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast_for_others(client,'{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = SERVER.accept()
        print("Connected with {}".format(str(address)))
        
        add_user(client)
        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()