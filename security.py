import base64
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SecurityUtils:
    @staticmethod
    def derive_key(master_password: str, salt: bytes) -> bytes:
        '''
        Genera una chiave derivata a partire dalla master password e da un salt.

        Parametri:
        master_password (str) -> password principale dell'utente
        salt (bytes) -> valore salt da utilizzare per la derivazione

        Valore di ritorno:
        bytes -> chiave derivata codificata in base64 urlsafe
        '''
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key

    @staticmethod
    def hash_password(password: str) -> str:
        '''
        Calcola l'hash SHA-256 di una password.

        Parametri:
        password (str) -> password in chiaro

        Valore di ritorno:
        str -> hash esadecimale della password
        '''
        return hashlib.sha256(password.encode()).hexdigest()