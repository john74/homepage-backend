from django.conf import settings

from cryptography.fernet import Fernet


def decrypt_data(encrypted_data):
    if not encrypted_data:
        return

    key = settings.SECRET_KEY
    fernet = Fernet(key)
    raw_encrypted_data = encrypted_data[2:-1]
    encrypted_bytes = raw_encrypted_data.encode()
    decrypted_bytes = fernet.decrypt(encrypted_bytes)
    decrypted_data = decrypted_bytes.decode()

    return decrypted_data