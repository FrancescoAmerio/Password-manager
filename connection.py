import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from typing import Optional, Any

class DatabaseConnection:
    # Credenziali caricate da .env (non hardcoded)
    def __init__(self, host: str = None, user: str = None, password: str = None, database: str = None) -> None:
        '''
        Costruttore della classe DatabaseConnection.
        Legge credenziali da variabili d'ambiente (.env).
        
        Parametri:
        host (str) -> indirizzo del server del database
        user (str) -> nome utente per la connessione
        password (str) -> password per la connessione
        database (str) -> nome del database da utilizzare
        '''
        load_dotenv()
        self.host = host or os.getenv("DB_HOST")
        self.user = user or os.getenv("DB_USER")
        self.password = password or os.getenv("DB_PASSWORD")
        self.database = database or os.getenv("DB_NAME")
        self.conn = None
        self.cursor = None

    def open(self) -> None:
        '''
        Apre la connessione al database.

        Valore di ritorno:
        None
        '''
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                print("Connection established successfully!")
        except Error as e:
            print("Connection error:", e)

    def execute_query(self, query: str, params: Optional[tuple[Any, ...]] = None) -> Optional[list[tuple[Any, ...]]]:
        '''
        Esegue una query SQL sul database.

        Parametri:
        query (str) -> stringa contenente la query SQL
        params (tuple[Any, ...] | None) -> parametri opzionali per la query

        Valore di ritorno:
        list[tuple[Any, ...]] -> risultati della query
        None -> se la connessione non è attiva o si verifica un errore
        '''
        if self.conn is None or not self.conn.is_connected():
            print("Connection is not active.")
            return None
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print("Error while executing query:", e)
            return None

    def close(self) -> None:
        '''
        Chiude la connessione al database.

        Valore di ritorno:
        None
        '''
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Connection closed.")