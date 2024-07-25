from custom_validations import ValidationError
from scripts import make_password, generate_random_password


class ChatUser:
    def __init__(self, conn, nickname, password=None):
        self.conn = conn
        self.nickname = nickname
        self.password = password
        self.role = None

    def change_password(self, old_password, new_passwod, new_password_2):
        if new_passwod != new_password_2:
            raise ValidationError("passwords does not match!")
        if old_password != self.password:
            raise ValidationError("sth is wrong")

        self.password = make_password(new_passwod)

    def set_random_password(self):
        _, random_password = generate_random_password()
        self.password = random_password

    def set_password(self):
        self.password = make_password(self.password.encode("utf-8"))

    def choose_password(self, password_choices, **kwargs):
        if password_choices not in ["0", "1", "2"]:
            raise ValueError("wrong password_choices value")

        method_map = {
            "0": self.set_password,
            "1": self.set_random_password,
            "2": self.change_password,
        }
        method_map[password_choices](**kwargs)
