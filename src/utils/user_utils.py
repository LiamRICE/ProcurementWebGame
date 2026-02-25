import json
from typing import Dict
import os

# Add necessary libraries for encryption
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import hashlib
import secrets

def store_credentials(username: str, password: str) -> None:
    """
    Store a newly created user's credentials in a secure fashion.

    Args:
        username (str): The username of the newly created user.
        password (str): The password of the newly created user.

    Returns:
        None
    """

    # Create the directory to store credentials if it doesn't exist
    cred_dir = 'src/data/credentials/'
    os.makedirs(cred_dir, exist_ok=True)

    # Generate a secure key for encryption
    key = secrets.token_bytes(32)
    hashed_key = hashlib.sha256(key).hexdigest()

    # Store the credentials in JSON format with encryption
    cred_data: Dict[str, str] = {
        'username': username,
        'password': encrypt_password(password, key),
        'key': hashed_key
    }

    with open(os.path.join(cred_dir, f"{username}.json"), "w") as file:
        json.dump(cred_data, file)


def check_credentials(username: str, provided_password: str) -> bool:
    """
    Check a user's credentials against those stored in the credentials file.

    Args:
        username (str): The username to be checked.
        provided_password (str): The password provided by the user.

    Returns:
        bool: True if the credentials match, False otherwise.
    """

    # Load the encrypted credentials from the JSON file
    cred_dir = 'src/data/credentials/'
    with open(os.path.join(cred_dir, f"{username}.json"), "r") as file:
        stored_data: Dict[str, str] = json.load(file)
        print(stored_data)

    # Decrypt the stored password using the hashed key
    key = hashlib.sha256(stored_data['key'].encode()).digest()
    encrypted_password = stored_data['password']
    
    print("Encrypted password:", encrypted_password)

    # Create a cipher object for decryption
    cipher = Cipher(algorithms.AES(key), modes.CBC(b'\x00'*16), backend=default_backend())
    decryptor = cipher.decryptor()
    
    print("Decrypting password...")
    
    try:
        decrypted_password = decryptor.update(encrypted_password.encode()) + decryptor.finalize()
    except ValueError:  # Catch ValueError instead of InvalidPadding
        print("Decryption failed: Invalid padding")
        return False

    print("Decryption successful")

    # Remove padding
    padder = padding.PKCS7(128).unpadder()
    unpadded_password = padder.update(decrypted_password)
    
    print("Unpadded password:", unpadded_password)

    try:
        final_unpadded = padder.finalize()
    except ValueError:
        print("Decryption failed: Invalid padding")
        return False
    # Compare the provided password with the decrypted password
    print("Provided password:", provided_password)
    print("Unpadded password:", final_unpadded.decode())
    
    return provided_password == final_unpadded.decode()


def encrypt_password(password: str, key: bytes) -> str:
    """
    Encrypt a password using AES-256-CBC.

    Args:
        password (str): The password to be encrypted.
        key (bytes): The encryption key.

    Returns:
        str: The encrypted password as a hexadecimal string.
    """

    # Create a cipher object for encryption
    cipher = Cipher(algorithms.AES(key), modes.CBC(b'\x00'*16), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the password
    padder = padding.PKCS7(128).padder()
    padded_password = padder.update(password.encode()) + padder.finalize()

    # Encrypt the padded password
    encrypted_password = encryptor.update(padded_password) + encryptor.finalize()

    # Return the encrypted password as a hexadecimal string
    return encrypted_password.hex()

