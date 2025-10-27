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
            hashed_pwd = SecurityUtils.hash_password(master_password)
            
            # Verifica se l'utente esiste già
            check_query = "SELECT id FROM users WHERE username = %s"
            result = self.db.execute_query(check_query, (username,))
            
            if (len(username) < 3 or len(master_password) < 3):
                print("Username o password devono essere di almeno 3 caratteri")
                return False
            elif result:
                print(f"Username '{username}' già esistente!")
                return False
            
            # Inserisce il nuovo utente
            insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            self.db.cursor.execute(insert_query, (username, hashed_pwd))
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
            hashed_pwd = SecurityUtils.hash_password(master_password)
            
            query = "SELECT id FROM users WHERE username = %s AND password = %s"
            result = self.db.execute_query(query, (username, hashed_pwd))
            
            if result and len(result) > 0:
                self.user_id = result[0][0]
                # Usa username come salt
                salt = username.encode()
                key = SecurityUtils.derive_key(master_password, salt)
                self.cipher = Fernet(key)
                print(f" Login effettuato come '{username}'!")
                return True
            else:
                print(" Credenziali non valide!")
                return False
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
            print(" Devi prima effettuare il login!")
            return False
        
        try:
            # Controllo se il servizio esiste già per questo utente
            check_query = "SELECT id FROM user_credentials WHERE user_id = %s AND service = %s"
            result = self.db.execute_query(check_query, (self.user_id, service))
            
            if result and len(result) > 0:
                print(f" Esiste già una password salvata per il servizio '{service}'!")
                return False

            # Inserimento nuova password
            encrypted_pwd = self.cipher.encrypt(password.encode()).decode()
            
            insert_query = "INSERT INTO user_credentials (user_id, service, password) VALUES (%s, %s, %s)"
            self.db.cursor.execute(insert_query, (self.user_id, service, encrypted_pwd))
            self.db.conn.commit()
            
            print(f"✓ Password per '{service}' salvata con successo!")
            return True
    
        except Exception as e:
            print(f"✗ Errore durante il salvataggio: {e}")
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
            print(" Devi prima effettuare il login!")
            return None
        
        try:
            query = "SELECT password FROM user_credentials WHERE user_id = %s AND service = %s"
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
    
    def list_services(self) -> list[tuple[Any, ...]]:
        '''
        Elenca tutti i servizi salvati.

        Valore di ritorno:
        list[tuple] -> lista di tuple contenenti id e nome del servizio
        '''
        if not self.user_id:
            print(" Devi prima effettuare il login!")
            return []
        
        try:
            query = "SELECT id, service FROM user_credentials WHERE user_id = %s ORDER BY service"
            result = self.db.execute_query(query, (self.user_id,))
            return result if result else []
        except Exception as e:
            print(f" Errore durante il recupero dei servizi: {e}")
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
            
            query = "UPDATE user_credentials SET password = %s WHERE user_id = %s AND service = %s"
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
            query = "DELETE FROM user_credentials WHERE user_id = %s AND service = %s"
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