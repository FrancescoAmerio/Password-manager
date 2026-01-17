# ---------------- MAIN ----------------
import os
import sys

from connection import DatabaseConnection
from passwordManagerGUI import PasswordManagerGUI
from passwordManager import PasswordManager
import customtkinter as ctk

def resource_path(relative_path):
    """ Ottiene il percorso assoluto delle risorse"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main() -> None:
    '''
    Funzione principale del programma.
    
    - Apre la connessione al database
    - Inizializza il gestore delle password
    - Configura la finestra principale dell'interfaccia grafica
    - Avvia il ciclo principale dell'applicazione
    - Chiude la connessione al database alla fine
     
    Valore di ritorno:
    None
    '''

    db = DatabaseConnection()
    db.open()
    pm = PasswordManager(db)

    root = ctk.CTk()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root.minsize(600, 400)
    root.maxsize(1200, 800)

    app = PasswordManagerGUI(root, pm)
    root.mainloop()
    db.close()


if __name__ == "__main__":
    main()