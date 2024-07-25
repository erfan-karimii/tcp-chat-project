import socket
import threading


def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            print(message)
        except:
            print("An error occured!")
            client.close()
            break


def write():
    while True:
        try:
            msg = input()
        except (KeyboardInterrupt, EOFError):
            break

        formated_message = f"{nickname}: {msg}"
        client.send(formated_message.encode("ascii"))


if __name__ == "__main__":
    nickname = input("Choose your nickname: ")
    password = input("enter your password: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 55555))
    user_pass = nickname + "-" + password
    client.send(user_pass.encode("ascii"))

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
