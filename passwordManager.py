from cryptography.fernet import Fernet
from security import SecurityUtils

class PasswordManager:
    def __init__(self, db_connection):
        """Inizializza il gestore password con connessione DB"""
        self.db = db_connection
        self.cipher = None
        self.user_id = None
        

    def register_user(self, username, master_password):
        """Registra un nuovo utente"""
        try:
            hashed_pwd = SecurityUtils.hash_password(master_password)
            
            # Verifica se l'utente esiste già
            check_query = "SELECT id FROM users WHERE username = %s"
            result = self.db.execute_query(check_query, (username,))
            
            if result:
                print(f"✗ Username '{username}' già esistente!")
                return False
            
            # Inserisce il nuovo utente
            insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            self.db.cursor.execute(insert_query, (username, hashed_pwd))
            self.db.conn.commit()
            
            print(f"✓ Utente '{username}' registrato con successo!")
            return True
        except Exception as e:
            print(f"✗ Errore durante la registrazione: {e}")
            return False
    
    def login(self, username, master_password):
        """Effettua il login e inizializza la cifratura"""
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
                print(f"✓ Login effettuato come '{username}'!")
                return True
            else:
                print("✗ Credenziali non valide!")
                return False
        except Exception as e:
            print(f"✗ Errore durante il login: {e}")
            return False
    
    def add_password(self, service, password):
        """Aggiunge una nuova password cifrata"""
        if not self.cipher or not self.user_id:
            print("✗ Devi prima effettuare il login!")
            return False
        
        try:
            encrypted_pwd = self.cipher.encrypt(password.encode()).decode()
            
            query = "INSERT INTO user_credentials (user_id, service, password) VALUES (%s, %s, %s)"
            self.db.cursor.execute(query, (self.user_id, service, encrypted_pwd))
            self.db.conn.commit()
            
            print(f"✓ Password per '{service}' salvata con successo!")
            return True
        except Exception as e:
            print(f"✗ Errore durante il salvataggio: {e}")
            return False
    
    def get_password(self, service):
        """Recupera e decifra una password"""
        if not self.cipher or not self.user_id:
            print("✗ Devi prima effettuare il login!")
            return None
        
        try:
            query = "SELECT password FROM user_credentials WHERE user_id = %s AND service = %s"
            result = self.db.execute_query(query, (self.user_id, service))
            
            if result and len(result) > 0:
                encrypted_pwd = result[0][0]
                decrypted_pwd = self.cipher.decrypt(encrypted_pwd.encode()).decode()
                return decrypted_pwd
            else:
                print(f"✗ Nessuna password trovata per '{service}'")
                return None
        except Exception as e:
            print(f"✗ Errore durante il recupero: {e}")
            return None
    
    def list_services(self):
        """Elenca tutti i servizi salvati"""
        if not self.user_id:
            print("✗ Devi prima effettuare il login!")
            return []
        
        try:
            query = "SELECT id, service FROM user_credentials WHERE user_id = %s ORDER BY service"
            result = self.db.execute_query(query, (self.user_id,))
            return result if result else []
        except Exception as e:
            print(f"✗ Errore durante il recupero dei servizi: {e}")
            return []
    
    def update_password(self, service, new_password):
        """Aggiorna una password esistente"""
        if not self.cipher or not self.user_id:
            print("✗ Devi prima effettuare il login!")
            return False
        
        try:
            encrypted_pwd = self.cipher.encrypt(new_password.encode()).decode()
            
            query = "UPDATE user_credentials SET password = %s WHERE user_id = %s AND service = %s"
            self.db.cursor.execute(query, (encrypted_pwd, self.user_id, service))
            self.db.conn.commit()
            
            if self.db.cursor.rowcount > 0:
                print(f"✓ Password per '{service}' aggiornata con successo!")
                return True
            else:
                print(f"✗ Servizio '{service}' non trovato!")
                return False
        except Exception as e:
            print(f"✗ Errore durante l'aggiornamento: {e}")
            return False
    
    def delete_password(self, service):
        """Elimina una password"""
        if not self.user_id:
            print("✗ Devi prima effettuare il login!")
            return False
        
        try:
            query = "DELETE FROM user_credentials WHERE user_id = %s AND service = %s"
            self.db.cursor.execute(query, (self.user_id, service))
            self.db.conn.commit()
            
            if self.db.cursor.rowcount > 0:
                print(f"✓ Password per '{service}' eliminata con successo!")
                return True
            else:
                print(f"✗ Servizio '{service}' non trovato!")
                return False
        except Exception as e:
            print(f"✗ Errore durante l'eliminazione: {e}")
            return False
