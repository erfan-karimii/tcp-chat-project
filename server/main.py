import socket
import threading
from models import ChatUser

HOST = "127.0.0.1"
PORT = 55555

# Lists For Clients and Their Nicknames
CLIENTS = []

SUPER_USERS_LIST = {
    "erfan": "94aefb8be78b2b7c344d11d1ba8a79ef087eceb19150881f69460b8772753263"
}


class SocialMedia:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen()

        print(f"server start and listion on {HOST}:{PORT}")
        self.start_accepting_connection()

    def start_accepting_connection(self):
        while True:
            # Accept Connection
            client, address = self.server.accept()
            user_pass = client.recv(1024).decode("ascii")
            nickname, user_password_choice, password = user_pass.split("-")

            print(f"{nickname} Connected to server with {str(address)}")

            self.user = self.get_or_create_user(
                client, nickname, password, user_password_choice
            )
            CLIENTS.append(self.user)
            self.broadcast_for_others(
                self.user, "{} joined!".format(nickname).encode("ascii")
            )
            thread = threading.Thread(target=self.handle, args=(self.user,))
            thread.start()

    def get_or_create_user(self, client, nickname, password, user_password_choice):
        user = ChatUser(client, nickname, password)
        # if not exists
        user.choose_password(user_password_choice)
        return user

    @staticmethod
    def broadcast_for_others(sender, message):
        for user in CLIENTS:
            if user != sender:
                user.conn.send(message)

    @staticmethod
    def handle(user):
        while True:
            try:
                message = user.conn.recv(1024)
                SocialMedia.broadcast_for_others(user, message)
            except:
                user.conn.close()
                SocialMedia.broadcast_for_others(
                    user, f"{user.nickname} left!".encode("ascii")
                )
                CLIENTS.remove(user)
                break


if __name__ == "__main__":
    social_media = SocialMedia(HOST, PORT)
