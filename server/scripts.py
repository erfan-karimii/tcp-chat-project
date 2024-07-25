import hashlib
import uuid


def make_password(password):
    hash_object = hashlib.sha256()
    hash_object.update(password)
    return hash_object.hexdigest()


def generate_random_password():
    random_password = uuid.uuid4()
    random_hashed_password = make_password(random_password)
    return random_password , random_hashed_password