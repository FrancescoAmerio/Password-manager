from cryptography.fernet import Fernet
from security import SecurityUtils
from typing import Optional, Any

class PasswordManager:
    def __init__(self, db_connection) -> None:
        '''
        Costruttore della classe PasswordManager.

        Parametri:
        db_connection -> connessione al database
        '''
        self.db = db_connection
        self.cipher: Optional[Fernet] = None
        self.user_id: Optional[int] = None
        

    def register_user(self, username: str, master_password: str) -> bool:
        '''
        Registra un nuovo utente.

        Parametri:
        username (str) -> nome utente
        master_password (str) -> password principale

        Valore di ritorno:
        bool -> True se la registrazione è avvenuta con successo, False altrimenti
        '''
        try:
            if len(username) < 3 or len(master_password) < 3:
                print("Username o password devono essere di almeno 3 caratteri")
                return False

            # Verifica se l'utente esiste già
            check_query = "SELECT id FROM users WHERE username = ?"
            result = self.db.execute_query(check_query, (username,))

            if result:
                print(f"Username '{username}' già esistente!")
                return False

            # 1) genera un salt casuale (per Fernet key derivation)
            salt = SecurityUtils.generate_salt()

            # 2) calcola l'hash usando password (Argon2 include salt interno)
            hashed_pwd = SecurityUtils.hash_password(master_password)

            # 3) inserisce il nuovo utente con hash + salt (salt per derive_key)
            insert_query = "INSERT INTO users (username, password, salt) VALUES (?, ?, ?)"
            self.db.cursor.execute(insert_query, (username, hashed_pwd, salt))
            self.db.conn.commit()

            print(f"Utente '{username}' registrato con successo!")
            return True
        except Exception as e:
            print(f"Errore durante la registrazione: {e}")
            return False

    
    def login(self, username: str, master_password: str) -> bool:
        '''
        Effettua il login e inizializza la cifratura.

        Parametri:
        username (str) -> nome utente
        master_password (str) -> password principale

        Valore di ritorno:
        bool -> True se il login è avvenuto con successo, False altrimenti
        '''
        try:
            # Recupero id, hash e salt per quello username
            query = "SELECT id, password, salt FROM users WHERE username = ?"
            result = self.db.execute_query(query, (username,))

            if not result:
                print("Credenziali non valide!")
                return False

            user_id, stored_hash, salt = result[0]  # salt è bytes (VARBINARY)

            # Verifico la password (Argon2 contiene salt internamente)
            if not SecurityUtils.verify_password(master_password, stored_hash):
                print("Credenziali non valide!")
                return False

            # Login OK: salvo id utente
            self.user_id = user_id

            # Uso lo stesso salt per derivare la chiave di cifratura
            key = SecurityUtils.derive_key(master_password, salt)
            self.cipher = Fernet(key)

            print(f" Login effettuato come '{username}'!")
            return True

        except Exception as e:
            print(f" Errore durante il login: {e}")
            return False

    
    def add_password(self, service: str, password: str) -> bool:
        '''
        Aggiunge un nuovo servizio con una nuova password cifrata, evitando duplicati.

        Parametri:
        service (str) -> nome del servizio
        password (str) -> password da salvare

        Valore di ritorno:
        bool -> True se la password è stata salvata, False altrimenti
        '''
        if not self.cipher or not self.user_id:
            print("Devi prima effettuare il login!")
            return False
        
        try:
            # Controllo se il servizio esiste già per questo utente
            check_query = "SELECT id FROM user_credentials WHERE user_id = ? AND service = ?"
            result = self.db.execute_query(check_query, (self.user_id, service))
            
            if result and len(result) > 0:
                print(f" Esiste già una password salvata per il servizio '{service}'!")
                return False

            # Inserimento nuova password
            encrypted_pwd = self.cipher.encrypt(password.encode()).decode()
            
            insert_query = "INSERT INTO user_credentials (user_id, service, password) VALUES (?, ?, ?)"
            self.db.cursor.execute(insert_query, (self.user_id, service, encrypted_pwd))
            self.db.conn.commit()
            
            print(f"Password per '{service}' salvata con successo!")
            return True
    
        except Exception as e:
            print(f"Errore durante il salvataggio: {e}")
            return False
    
    def get_password(self, service: str) -> Optional[str]:
        '''
        Recupera e decifra una password.

        Parametri:
        service (str) -> nome del servizio

        Valore di ritorno:
        str -> password decifrata
        None -> se non trovata o in caso di errore
        '''
        if not self.cipher or not self.user_id:
            print("Devi prima effettuare il login!")
            return None
        
        try:
            query = "SELECT password FROM user_credentials WHERE user_id = ? AND service = ?"
            result = self.db.execute_query(query, (self.user_id, service))
            
            if result and len(result) > 0:
                encrypted_pwd = result[0][0]
                decrypted_pwd = self.cipher.decrypt(encrypted_pwd.encode()).decode()
                return decrypted_pwd
            else:
                print(f" Nessuna password trovata per '{service}'")
                return None
        except Exception as e:
            print(f" Errore durante il recupero: {e}")
            return None
    
    def list_services(self) -> list[tuple[int, str]]:
        '''
        Elenca tutti i servizi salvati.

        Valore di ritorno:
        list[tuple[int, str]] -> lista di tuple dove ogni tupla contiene:
            - id (int): identificativo univoco del servizio
            - service (str): nome del servizio
        '''
        if not self.user_id:
            print("Devi prima effettuare il login!")
            return []
        
        try:
            query = "SELECT id, service FROM user_credentials WHERE user_id = ? ORDER BY service"
            result = self.db.execute_query(query, (self.user_id,))
            return result if result else []
        except Exception as e:
            print(f" Errore durante il recupero dei servizi: {e}")
            return []

    def search_services(self, keyword: str) -> list[tuple[int, str]]:
        '''
        Cerca servizi salvati che contengono una determinata parola chiave.

        Parametri:
        keyword (str) -> testo da cercare all'interno del nome del servizio

        Valore di ritorno:
        list[tuple[int, str]] -> lista di tuple dove ogni tupla contiene:
            - id (int): identificativo univoco del servizio
            - service (str): nome del servizio che contiene la parola chiave
        '''
        if not self.user_id:
            print("Devi prima effettuare il login!")
            return []

        try:
            query = """
                SELECT id, service 
                FROM user_credentials 
                WHERE user_id = ? AND service LIKE ? 
                ORDER BY service
            """
            # '%keyword%' permette di cercare la parola anche nel mezzo del nome
            result = self.db.execute_query(query, (self.user_id, f"%{keyword}%"))
            
            if result and len(result) > 0:
                print(f"Trovati {len(result)} servizi che contengono '{keyword}':")
                return result
            else:
                print(f"Nessun servizio trovato per '{keyword}'.")
                return []
        except Exception as e:
            print(f"Errore durante la ricerca: {e}")
            return []

    def update_password(self, service: str, new_password: str) -> bool:
        '''
        Aggiorna una password esistente.

        Parametri:
        service (str) -> nome del servizio
        new_password (str) -> nuova password da salvare

        Valore di ritorno:
        bool -> True se aggiornata con successo, False altrimenti
        '''
        if not self.cipher or not self.user_id:
            print(" Devi prima effettuare il login!")
            return False
        
        try:
            encrypted_pwd = self.cipher.encrypt(new_password.encode()).decode()
            
            query = "UPDATE user_credentials SET password = ? WHERE user_id = ? AND service = ?"
            self.db.cursor.execute(query, (encrypted_pwd, self.user_id, service))
            self.db.conn.commit()
            
            if self.db.cursor.rowcount > 0:
                print(f" Password per '{service}' aggiornata con successo!")
                return True
            else:
                print(f" Servizio '{service}' non trovato!")
                return False
        except Exception as e:
            print(f" Errore durante l'aggiornamento: {e}")
            return False
    
    def delete_password(self, service: str) -> bool:
        '''
        Elimina una password.

        Parametri:
        service (str) -> nome del servizio

        Valore di ritorno:
        bool -> True se eliminata con successo, False altrimenti
        '''
        if not self.user_id:
            print(" Devi prima effettuare il login!")
            return False
        
        try:
            query = "DELETE FROM user_credentials WHERE user_id = ? AND service = ?"
            self.db.cursor.execute(query, (self.user_id, service))
            self.db.conn.commit()
            
            if self.db.cursor.rowcount > 0:
                print(f" Password per '{service}' eliminata con successo!")
                return True
            else:
                print(f" Servizio '{service}' non trovato!")
                return False
        except Exception as e:
            print(f" Errore durante l'eliminazione: {e}")
            return False