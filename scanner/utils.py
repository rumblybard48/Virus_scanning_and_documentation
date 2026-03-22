import clamd
import os
from cryptography.fernet import Fernet

key='secret.key'

def generate_key():
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)

def load_key():
    return open('secret.key', 'rb').read()

def encrypt_file(source_path, destination_path, key):
    fernet = Fernet(key)
    with open(source_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(destination_path, 'wb') as enc_file:
        enc_file.write(encrypted)

def decrypt_file(source_path, destination_path, key):
    fernet = Fernet(key)
    with open(source_path, 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(destination_path, 'wb') as dec_file:
        dec_file.write(decrypted)

# THIS FUNCTION IS USED TO SCAN THE DOCUMENT FOR VIRUSES
def run_clamav_scan(file_path):
    try:
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"

        cd = clamd.ClamdNetworkSocket(host='127.0.0.1', port=3310)
        cd.ping()  # Check if clamd is running

        result = cd.scan(file_path)
        if result and result[file_path][0] == 'FOUND':
            return False, result[file_path][1]  # Return virus name
        return True, "Clean"
    except Exception as e:
        return False, f"Scan failed: {str(e)}"
