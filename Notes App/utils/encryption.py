from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

KEY_FILE = "data/encryption_key.key"

def get_or_create_key():
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

key = get_or_create_key()
cipher = Fernet(key)

def get_key_from_password(password):
    # Convert password to encryption key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'fixed_salt',  # In production, use a unique salt per user
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_note(content, password):
    try:
        key = get_key_from_password(password)
        f = Fernet(key)
        encrypted_content = f.encrypt(content.encode())
        return encrypted_content.decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        return None

def decrypt_note(encrypted_content, password):
    try:
        key = get_key_from_password(password)
        f = Fernet(key)
        decrypted_content = f.decrypt(encrypted_content.encode())
        return decrypted_content.decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        return None
