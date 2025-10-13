import tkinter as tk
from tkinter import messagebox, simpledialog
from passwordManager import PasswordManager
from connection import DatabaseConnection

class PasswordManagerGUI:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.root.title("🔐 Password Manager")

        self.login_frame = tk.Frame(root)
        self.main_frame = tk.Frame(root)

        self.build_login_frame()

    def build_login_frame(self):
        self.clear_frames()
        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="Master Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, pady=10)
        tk.Button(self.login_frame, text="Registrati", command=self.register).grid(row=2, column=1, pady=10)

        self.login_frame.pack()

    def build_main_frame(self):
        self.clear_frames()
        tk.Button(self.main_frame, text="Aggiungi password", command=self.add_password).pack(pady=5)
        tk.Button(self.main_frame, text="Visualizza password", command=self.get_password).pack(pady=5)
        tk.Button(self.main_frame, text="Lista servizi", command=self.list_services).pack(pady=5)
        tk.Button(self.main_frame, text="Aggiorna password", command=self.update_password).pack(pady=5)
        tk.Button(self.main_frame, text="Elimina password", command=self.delete_password).pack(pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.logout).pack(pady=5)
        self.main_frame.pack()

    def clear_frames(self):
        for frame in (self.login_frame, self.main_frame):
            frame.pack_forget()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.manager.login(username, password):
            messagebox.showinfo("Successo", f"Login effettuato come {username}")
            self.build_main_frame()
        else:
            messagebox.showerror("Errore", "Credenziali non valide")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.manager.register_user(username, password):
            messagebox.showinfo("Successo", "Registrazione completata!")
        else:
            messagebox.showerror("Errore", "Registrazione fallita")

    def add_password(self):
        service = simpledialog.askstring("Servizio", "Nome servizio:")
        pwd = simpledialog.askstring("Password", "Inserisci password:", show="*")
        if service and pwd:
            self.manager.add_password(service, pwd)
            messagebox.showinfo("OK", f"Password per {service} salvata!")

    def get_password(self):
        service = simpledialog.askstring("Servizio", "Nome servizio:")
        if service:
            pwd = self.manager.get_password(service)
            if pwd:
                messagebox.showinfo("Password", f"{service}: {pwd}")
            else:
                messagebox.showerror("Errore", "Servizio non trovato")

    def list_services(self):
        services = self.manager.list_services()
        if services:
            lista = "\n".join([s for _, s in services])
            messagebox.showinfo("Servizi salvati", lista)
        else:
            messagebox.showinfo("Servizi", "Nessun servizio salvato")

    def update_password(self):
        service = simpledialog.askstring("Servizio", "Nome servizio:")
        new_pwd = simpledialog.askstring("Nuova password", "Inserisci nuova password:", show="*")
        if service and new_pwd:
            self.manager.update_password(service, new_pwd)

    def delete_password(self):
        service = simpledialog.askstring("Servizio", "Nome servizio da eliminare:")
        if service:
            self.manager.delete_password(service)

    def logout(self):
        self.manager.user_id = None
        self.manager.cipher = None
        messagebox.showinfo("Logout", "Logout effettuato")
        self.build_login_frame()


if __name__ == "__main__":
    db = DatabaseConnection()
    db.open()
    pm = PasswordManager(db)

    root = tk.Tk()
    app = PasswordManagerGUI(root, pm)
    root.mainloop()
    db.close()