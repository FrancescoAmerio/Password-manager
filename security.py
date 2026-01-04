import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class SecurityUtils:
    @staticmethod
    def generate_salt(length: int = 16) -> bytes:
        '''
        Genera un salt casuale.

        Parametri:
        length (int) -> lunghezza del salt in byte (default 16)

        Valore di ritorno:
        bytes -> salt casuale
        '''
        return os.urandom(length)

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
        Calcola l'hash Argon2 della password.

        Parametri:
        password (str) -> password in chiaro

        Valore di ritorno:
        str -> hash Argon2 serializzato (include salt + hash)
        '''
        ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=4)
        return ph.hash(password)
    
    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        '''
        Verifica se una password corrisponde a un hash Argon2.

        Parametri:
        password (str) -> password in chiaro inserita dall'utente
        stored_hash (str) -> hash Argon2 salvato nel DB

        Valore di ritorno:
        bool -> True se combaciano, False altrimenti
        '''
        ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=4)
        try:
            ph.verify(stored_hash, password)
            return True
        except VerifyMismatchError:
            return False