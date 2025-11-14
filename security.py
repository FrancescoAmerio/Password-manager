import base64
import hashlib
import os
import hmac
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


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
    def hash_password(password: str, salt: bytes) -> str:
        '''
        Calcola l'hash SHA-256 di una password usando un salt.

        Parametri:
        password (str) -> password in chiaro
        salt (bytes) -> salt da usare per l'hash

        Valore di ritorno:
        str -> hash esadecimale della password salata
        '''
        return hashlib.sha256(salt + password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, salt: bytes, stored_hash: str) -> bool:
        '''
        Verifica se una password corrisponde a un hash esistente.

        Parametri:
        password (str) -> password in chiaro inserita dall'utente
        salt (bytes) -> salt salvato nel DB
        stored_hash (str) -> hash esadecimale salvato nel DB

        Valore di ritorno:
        bool -> True se combaciano, False altrimenti
        '''
        candidate_hash = SecurityUtils.hash_password(password, salt)
        # Impiega sempre lo stesso tempo per prevenire attacchi di timing
        return hmac.compare_digest(candidate_hash, stored_hash)