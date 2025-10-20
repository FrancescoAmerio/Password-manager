
import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import messagebox


class PasswordManagerGUI:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.root.title("🔐 Password Manager")

        self.login_frame = None
        self.main_frame = None
        self.table = None
        self.add_form = None
        self.update_form = None


        self.build_login_frame()

    # ---------------- LOGIN ----------------
    def build_login_frame(self):
        self.clear_frames()
        self.login_frame = ctk.CTkFrame(self.root)
        self.login_frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.login_frame.columnconfigure(0, weight=1)
        self.login_frame.columnconfigure(1, weight=1)
        self.login_frame.columnconfigure(2, weight=1)
        self.login_frame.columnconfigure(3, weight=1)


        ctk.CTkLabel(self.login_frame, text="Username:").grid(row=0, column=1, padx=5, pady=5)
        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Inserisci username")
        self.username_entry.grid(row=0, column=2, padx=5, pady=5)

        ctk.CTkLabel(self.login_frame, text="Master Password:").grid(row=1, column=1, padx=5, pady=5)
        self.password_entry = ctk.CTkEntry(self.login_frame, show="*", placeholder_text="Inserisci password")
        self.password_entry.grid(row=1, column=2, padx=5, pady=5)

        ctk.CTkButton(self.login_frame, text="Login", command=self.login).grid(row=2, column=1, pady=10)
        ctk.CTkButton(self.login_frame, text="Registrati", command=self.register).grid(row=2, column=2, pady=10)

    # ---------------- MAIN ----------------
    def build_main_frame(self):
        self.clear_frames()
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # --- Sinistra: pulsanti ---
        left_frame = ctk.CTkFrame(self.main_frame)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkButton(left_frame, text="Aggiorna password", command=self.show_update_form).pack(pady=5)
        ctk.CTkButton(left_frame, text="Mostra password", command=self.show_password).pack(pady=5)
        ctk.CTkButton(left_frame, text="Copia password", command=self.copy_password).pack(pady=5)
        ctk.CTkButton(left_frame, text="Elimina password", command=self.delete_password).pack(pady=5)
        ctk.CTkButton(left_frame, text="Logout", command=self.logout).pack(pady=5)

        # --- Destra: tabella + pulsante + ---
        right_frame = ctk.CTkFrame(self.main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        add_button = ctk.CTkButton(right_frame, text="+", width=40, command=self.show_add_form)
        add_button.pack(anchor="ne", pady=5, padx=5)

        
        # Stile scuro per la tabella
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="black",
                        foreground="white",
                        fieldbackground="black",
                        rowheight=25,
                        font=("Arial", 12))
        style.configure("Treeview.Heading",
                        background="gray20",
                        foreground="white",
                        font=("Arial", 12, "bold"))
        style.map("Treeview", background=[("selected", "gray40")])


        self.table = ttk.Treeview(right_frame, columns=("Servizio", "Password"), show="headings")
        self.table.heading("Servizio", text="Servizio")
        self.table.heading("Password", text="Password")
        self.table.pack(fill="both", expand=True)

        self.refresh_table()

    # ---------------- FORM AGGIUNTA ----------------
    def show_add_form(self):
        if self.add_form:
            self.add_form.destroy()
        if self.update_form:
            self.update_form.destroy()

        self.add_form = ctk.CTkFrame(self.main_frame)
        self.add_form.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(self.add_form, text="Aggiungi nuovo servizio:").grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        ctk.CTkLabel(self.add_form, text="Servizio:").grid(row=1, column=0, padx=5, pady=5)
        self.new_service_entry = ctk.CTkEntry(self.add_form, placeholder_text="Nome servizio")
        self.new_service_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.add_form, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        self.new_pwd_entry = ctk.CTkEntry(self.add_form, show="*", placeholder_text="Inserisci password")
        self.new_pwd_entry.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkButton(self.add_form, text="Salva", command=self.save_new_password).grid(row=3, column=1, columnspan=1, pady=10)
        ctk.CTkButton(self.add_form, text="Annulla", command=self.build_main_frame).grid(row=3, column=0, columnspan=1, pady=10)

    def save_new_password(self):
        service = self.new_service_entry.get()
        pwd = self.new_pwd_entry.get()
        if service and pwd:
            self.manager.add_password(service, pwd)
            messagebox.showinfo("OK", f"Password per {service} salvata!")
            self.refresh_table()
            self.add_form.destroy()
            self.add_form = None
        else:
            messagebox.showerror("Errore", "Compila tutti i campi")

    # ---------------- UTILS ----------------
    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        services = self.manager.list_services()
        if services:
            for service_id, service_name in services:
                pwd =  "*****"
                self.table.insert("", "end", values=(service_name, pwd))

    def clear_frames(self):
        if self.login_frame:
            self.login_frame.pack_forget()
        if self.main_frame:
            self.main_frame.pack_forget()

    # ---------------- LOGICA ----------------
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

    def show_update_form(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("Errore", "Seleziona un servizio dalla tabella")
            return

        service = self.table.item(selected[0])["values"][0]

        # Se esiste già un form, lo distruggo
        if self.update_form:
            self.update_form.destroy()
        if self.add_form:
            self.add_form.destroy()

        self.update_form = ctk.CTkFrame(self.main_frame)
        self.update_form.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(self.update_form, text=f"Aggiorna password per: {service}").grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        ctk.CTkLabel(self.update_form, text="Nuova password:").grid(row=1, column=0, padx=5, pady=5)
        self.update_pwd_entry = ctk.CTkEntry(self.update_form, show="*", placeholder_text="Inserisci nuova password")
        self.update_pwd_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkButton(self.update_form, text="Aggiorna", command=self.save_updated_password).grid(row=2, column=1, columnspan=1, pady=10)
        ctk.CTkButton(self.update_form, text="Annulla", command=self.build_main_frame).grid(row=2, column=0, columnspan=1, pady=10)

    def show_password(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("Errore", "Seleziona un servizio dalla tabella")
            return
        service = self.table.item(selected[0])["values"][0]
        pwd =self.manager.get_password(service)
        # messagebox.showinfo("Password: ", pwd)
        self.table.item(selected[0], values=(service, pwd))
        # Dopo 5 secondi torna a nasconderla
        self.root.after(4000, lambda: self.table.item(selected[0], values=(service, "*****")))

    def copy_password(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("Errore", "Seleziona un servizio dalla tabella")
            return
        service = self.table.item(selected[0])["values"][0]
        pwd =self.manager.get_password(service)
        self.root.clipboard_clear()
        self.root.clipboard_append(pwd)
        self.root.update()
        if(pwd):
            messagebox.showinfo("Copiata", "Password copiata negli appunti")


    def save_updated_password(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("Errore", "Seleziona un servizio dalla tabella")
            return
        service = self.table.item(selected[0])["values"][0]
        new_pwd = self.update_pwd_entry.get()
        if new_pwd:
            self.manager.update_password(service, new_pwd)
            messagebox.showinfo("Successo", f"Password per {service} aggiornata!")
            self.refresh_table()
            self.update_form.destroy()
            self.update_form = None
        else:
            messagebox.showerror("Errore", "Inserisci una nuova password")


    def delete_password(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("Errore", "Seleziona un servizio dalla tabella")
            return
        service = self.table.item(selected[0])["values"][0]
        self.manager.delete_password(service)
        self.refresh_table()

    def logout(self):
        self.manager.user_id = None
        self.manager.cipher = None
        messagebox.showinfo("Logout", "Logout effettuato")
        self.build_login_frame()


