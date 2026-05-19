import os
from cryptography.fernet import Fernet

FERNET_KEY = os.getenv("FERNET_KEY")

if not FERNET_KEY:
    FERNET_KEY = Fernet.generate_key().decode()
    print("WARNING: demo Fernet key generated. For real use, store it in environment variable.")

fernet = Fernet(FERNET_KEY.encode())


def encrypt_value(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()


def decrypt_value(value: str) -> str:
    return fernet.decrypt(value.encode()).decode()