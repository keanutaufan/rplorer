from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(password: str):
    return ph.hash(password=password)


def verify_hash(hashed_password: str, password: str):
    return ph.verify(hash=hashed_password, password=password)


def check_needs_rehash(hashed_password: str):
    return ph.check_needs_rehash(hash=hashed_password)