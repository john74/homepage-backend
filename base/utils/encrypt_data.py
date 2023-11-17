from django.conf import settings

from cryptography.fernet import Fernet


def encrypt_data(data):
    if not data:
        return

    key = settings.SECRET_KEY
    fernet = Fernet(key)
    encrypted_bytes = data.encode()
    encrypted_data = fernet.encrypt(encrypted_bytes)

    return encrypted_data