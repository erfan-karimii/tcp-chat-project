import socket
import threading


def send_nickname(client, nickname):
    client.send(nickname.encode("ascii"))


def receive(client):
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            print(message)
        except:
            print("An error occured!")
            client.close()
            break


def write(client):
    while True:
        try:
            msg = input()
        except (KeyboardInterrupt, EOFError):
            break

        formated_message = f"{nickname}: {msg}"
        client.send(formated_message.encode("ascii"))


if __name__ == "__main__":
    nickname = input("Choose your nickname: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 55555))

    send_nickname(client, nickname)

    receive_thread = threading.Thread(target=receive, args=(client,))
    receive_thread.start()

    write_thread = threading.Thread(target=write, args=(client,))
    write_thread.start()
