import base64
from cryptography.fernet import Fernet
from config import settings


def encrypt(txt: str or int) -> str:
    """
    Encrypts the transmitted information in base64
    Generate ENCRYPT_KEY (Fernet.generate_key()) and add it to the file .env
    """

    # convert integer etc to string first
    txt = str(txt)
    # get the key from settings
    cipher_suite = Fernet(settings.ENCRYPT_KEY) # key should be byte
    # #input should be byte, so convert the text to byte
    encrypted_text = cipher_suite.encrypt(txt.encode('utf8'))
    # encode to urlsafe base64 format
    encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode('utf8')
    return encrypted_text


def decrypt(string: str) -> str:
    """
    Decrypts information from base64
    """

    # base64 decode
    txt = base64.urlsafe_b64decode(string)
    cipher_suite = Fernet(settings.ENCRYPT_KEY)
    decoded_text = cipher_suite.decrypt(txt).decode('utf8')
    return decoded_text