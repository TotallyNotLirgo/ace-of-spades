from hashlib import sha256
from uuid import uuid4


def generate_token():
    return uuid4().urn.split(':')[-1]


def hash_value(value: str):
    return sha256(value.encode()).hexdigest()
