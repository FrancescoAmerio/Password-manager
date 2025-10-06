from connection import DatabaseConnection
import getpass
import passwordManager


def main_menu():
    """Menu principale del password manager"""
    # Inizializza connessione database
    db = DatabaseConnection()
    
    db.open()
    
    if not db.conn or not db.conn.is_connected():
        print("✗ Impossibile connettersi al database!")
        return
    
    pm = passwordManager.PasswordManager(db)
    
    try:
        while True:
            print("\n" + "="*50)
            print("🔐 PASSWORD MANAGER")
            print("="*50)
            
            if not pm.user_id:
                print("1. Registra nuovo utente")
                print("2. Login")
                print("3. Esci")
                
                choice = input("\nScelta: ").strip()
                
                if choice == '1':
                    username = input("Username: ").strip()
                    master_pwd = getpass.getpass("Master Password: ")
                    confirm_pwd = getpass.getpass("Conferma Master Password: ")
                    
                    if master_pwd == confirm_pwd:
                        pm.register_user(username, master_pwd)
                    else:
                        print("✗ Le password non coincidono!")
                        
                elif choice == '2':
                    username = input("Username: ").strip()
                    master_pwd = getpass.getpass("Master Password: ")
                    pm.login(username, master_pwd)
                    
                elif choice == '3':
                    print("Arrivederci!")
                    break
                else:
                    print("✗ Scelta non valida!")
            else:
                print("1. Aggiungi password")
                print("2. Visualizza password")
                print("3. Lista servizi")
                print("4. Aggiorna password")
                print("5. Elimina password")
                print("6. Logout")
                
                choice = input("\nScelta: ").strip()
                
                if choice == '1':
                    service = input("Nome servizio: ").strip()
                    password = getpass.getpass("Password: ")
                    pm.add_password(service, password)
                    
                elif choice == '2':
                    service = input("Nome servizio: ").strip()
                    password = pm.get_password(service)
                    if password:
                        print(f"\n🔑 Password per '{service}': {password}")
                        
                elif choice == '3':
                    services = pm.list_services()
                    if services:
                        print("\n📋 Servizi salvati:")
                        for sid, service in services:
                            print(f"  - {service}")
                    else:
                        print("Nessun servizio salvato")
                        
                elif choice == '4':
                    service = input("Nome servizio: ").strip()
                    new_password = getpass.getpass("Nuova password: ")
                    pm.update_password(service, new_password)
                    
                elif choice == '5':
                    service = input("Nome servizio da eliminare: ").strip()
                    confirm = input(f"Sei sicuro di voler eliminare '{service}'? (s/n): ")
                    if confirm.lower() == 's':
                        pm.delete_password(service)
                        
                elif choice == '6':
                    pm.user_id = None
                    pm.cipher = None
                    print("✓ Logout effettuato!")
                else:
                    print("✗ Scelta non valida!")
    finally:
        db.close()


if __name__ == "__main__":
    main_menu()