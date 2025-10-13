import customtkinter as ctk
from tkinter import messagebox, simpledialog
from passwordManager import PasswordManager
from connection import DatabaseConnection


class PasswordManagerGUI:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.root.title("🔐 Password Manager")

        self.login_frame = None
        self.main_frame = None

        self.build_login_frame()

    def build_login_frame(self):
        self.clear_frames()
        self.login_frame = ctk.CTkFrame(self.root)
        self.login_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Inserisci username")
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.login_frame, text="Master Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ctk.CTkEntry(self.login_frame, show="*", placeholder_text="Inserisci password")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkButton(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, pady=10)
        ctk.CTkButton(self.login_frame, text="Registrati", command=self.register).grid(row=2, column=1, pady=10)

    def build_main_frame(self):
        self.clear_frames()
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkButton(self.main_frame, text="Aggiungi password", command=self.add_password).pack(pady=5)
        ctk.CTkButton(self.main_frame, text="Visualizza password", command=self.get_password).pack(pady=5)
        ctk.CTkButton(self.main_frame, text="Lista servizi", command=self.list_services).pack(pady=5)
        ctk.CTkButton(self.main_frame, text="Aggiorna password", command=self.update_password).pack(pady=5)
        ctk.CTkButton(self.main_frame, text="Elimina password", command=self.delete_password).pack(pady=5)
        ctk.CTkButton(self.main_frame, text="Logout", command=self.logout).pack(pady=5)

    def clear_frames(self):
        if self.login_frame:
            self.login_frame.pack_forget()
        if self.main_frame:
            self.main_frame.pack_forget()

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

    root = ctk.CTk()

    # Imposta tema e colori
    ctk.set_appearance_mode("dark")   # "light", "dark", o "system"
    ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

    root.minsize(400, 300)
    root.maxsize(1200, 800)

    app = PasswordManagerGUI(root, pm)
    root.mainloop()
    db.close()



# import tkinter as tk
# import tkinter.font as tkFont
# from tkinter import messagebox, simpledialog
# from passwordManager import PasswordManager
# from connection import DatabaseConnection

# class PasswordManagerGUI:
#     def __init__(self, root, manager):
#         self.root = root
#         self.manager = manager
#         self.root.title("🔐 Password Manager")
        
#         # Configurazione tema scuro
#         self.setup_dark_theme()
        
#         # Frame principale che contiene tutto
#         self.main_container = tk.Frame(root, bg="#1a1a1a")
#         self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
#         # Mostra il frame di login all'avvio
#         self.show_login_frame()
    
#     def setup_dark_theme(self):
#         """Configura il tema scuro per l'applicazione"""
#         self.colors = {
#             'bg': '#1a1a1a',           # Sfondo principale
#             'fg': '#ffffff',           # Testo bianco
#             'button_bg': '#2d2d2d',    # Sfondo pulsanti
#             'button_hover': '#404040',  # Hover pulsanti
#             'entry_bg': '#252525',     # Sfondo input
#             'select_bg': '#0d7377',    # Selezione
#             'frame_bg': '#202020',     # Sfondo frame secondari
#             'list_bg': '#252525',      # Sfondo lista
#             'border': '#404040'        # Bordi
#         }
        
#         self.root.configure(bg=self.colors['bg'])
        
#     def show_login_frame(self):
#         """Mostra il frame di login"""
#         # Pulisci il container principale
#         for widget in self.main_container.winfo_children():
#             widget.destroy()
        
#         # Frame centrale per il login
#         login_frame = tk.Frame(self.main_container, bg=self.colors['frame_bg'], 
#                                relief=tk.RAISED, borderwidth=2)
#         login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
#         # Titolo
#         title = tk.Label(login_frame, text="🔐 Password Manager", 
#                         font=("Arial", 18, "bold"),
#                         bg=self.colors['frame_bg'], fg=self.colors['fg'])
#         title.grid(row=0, column=0, columnspan=2, pady=20, padx=40)
        
#         # Username
#         tk.Label(login_frame, text="Username:", 
#                 bg=self.colors['frame_bg'], fg=self.colors['fg'],
#                 font=("Arial", 11)).grid(row=1, column=0, padx=20, pady=10, sticky='e')
        
#         self.username_entry = tk.Entry(login_frame, 
#                                        bg=self.colors['entry_bg'], 
#                                        fg=self.colors['fg'],
#                                        insertbackground='white',
#                                        font=("Arial", 11))
#         self.username_entry.grid(row=1, column=1, padx=20, pady=10, ipadx=5, ipady=3)
        
#         # Password
#         tk.Label(login_frame, text="Password:", 
#                 bg=self.colors['frame_bg'], fg=self.colors['fg'],
#                 font=("Arial", 11)).grid(row=2, column=0, padx=20, pady=10, sticky='e')
        
#         self.password_entry = tk.Entry(login_frame, show="*",
#                                        bg=self.colors['entry_bg'], 
#                                        fg=self.colors['fg'],
#                                        insertbackground='white',
#                                        font=("Arial", 11))
#         self.password_entry.grid(row=2, column=1, padx=20, pady=10, ipadx=5, ipady=3)
        
#         # Frame per i pulsanti
#         button_frame = tk.Frame(login_frame, bg=self.colors['frame_bg'])
#         button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
#         # Pulsanti
#         self.create_button(button_frame, "Login", self.login).pack(side=tk.LEFT, padx=10)
#         self.create_button(button_frame, "Registrati", self.register).pack(side=tk.LEFT, padx=10)
        
#         # Focus sul primo campo
#         self.username_entry.focus_set()
        
#         # Bind Enter per login veloce
#         self.password_entry.bind('<Return>', lambda e: self.login())
    
#     def show_main_interface(self):
#         """Mostra l'interfaccia principale dopo il login"""
#         # Pulisci il container principale
#         for widget in self.main_container.winfo_children():
#             widget.destroy()
        
#         # Frame sinistro per il menu
#         left_frame = tk.Frame(self.main_container, bg=self.colors['frame_bg'], 
#                              width=200, relief=tk.RIDGE, borderwidth=1)
#         left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
#         left_frame.pack_propagate(False)
        
#         # Titolo del menu
#         menu_title = tk.Label(left_frame, text="Menu", 
#                              font=("Arial", 14, "bold"),
#                              bg=self.colors['frame_bg'], fg=self.colors['fg'])
#         menu_title.pack(pady=15)
        
#         # Pulsanti del menu
#         self.create_button(left_frame, "➕ Aggiungi", self.add_password).pack(pady=5, padx=20, fill=tk.X)
#         self.create_button(left_frame, "✏️ Modifica", self.update_password).pack(pady=5, padx=20, fill=tk.X)
#         self.create_button(left_frame, "🗑️ Elimina", self.delete_password).pack(pady=5, padx=20, fill=tk.X)
#         self.create_button(left_frame, "🔄 Aggiorna Lista", self.refresh_list).pack(pady=5, padx=20, fill=tk.X)
        
#         # Spazio vuoto espandibile
#         tk.Frame(left_frame, bg=self.colors['frame_bg']).pack(expand=True, fill=tk.Y)
        
#         # Pulsante logout in fondo
#         self.create_button(left_frame, "🚪 Logout", self.logout, 
#                           bg='#8b0000').pack(pady=20, padx=20, fill=tk.X)
        
#         # Frame destro per la lista dei servizi
#         right_frame = tk.Frame(self.main_container, bg=self.colors['frame_bg'],
#                               relief=tk.RIDGE, borderwidth=1)
#         right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
#         # Titolo della lista
#         list_title = tk.Label(right_frame, text="Servizi Salvati", 
#                              font=("Arial", 14, "bold"),
#                              bg=self.colors['frame_bg'], fg=self.colors['fg'])
#         list_title.pack(pady=10)
        
#         # Frame per la listbox con scrollbar
#         list_container = tk.Frame(right_frame, bg=self.colors['frame_bg'])
#         list_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
#         # Scrollbar
#         scrollbar = tk.Scrollbar(list_container, bg=self.colors['button_bg'])
#         scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
#         # Listbox per i servizi
#         self.services_listbox = tk.Listbox(list_container,
#                                            bg=self.colors['list_bg'],
#                                            fg=self.colors['fg'],
#                                            selectbackground=self.colors['select_bg'],
#                                            selectforeground=self.colors['fg'],
#                                            font=("Arial", 11),
#                                            height=15,
#                                            yscrollcommand=scrollbar.set)
#         self.services_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#         scrollbar.config(command=self.services_listbox.yview)
        
#         # Bind doppio click per visualizzare password
#         self.services_listbox.bind('<Double-Button-1>', self.show_password_from_list)
        
#         # Frame per mostrare la password selezionata
#         password_frame = tk.Frame(right_frame, bg=self.colors['frame_bg'], height=100)
#         password_frame.pack(fill=tk.X, padx=10, pady=10)
#         password_frame.pack_propagate(False)
        
#         # Label per istruzioni/password
#         self.password_display = tk.Label(password_frame,
#                                         text="Doppio click su un servizio per vedere la password",
#                                         bg=self.colors['frame_bg'],
#                                         fg='#888888',
#                                         font=("Arial", 10, "italic"))
#         self.password_display.pack(expand=True)
        
#         # Carica la lista dei servizi
#         self.refresh_list()
    
#     def create_button(self, parent, text, command, bg=None):
#         """Crea un pulsante con stile personalizzato"""
#         if bg is None:
#             bg = self.colors['button_bg']
            
#         btn = tk.Button(parent, text=text, command=command,
#                        bg=bg, fg=self.colors['fg'],
#                        font=("Arial", 10),
#                        relief=tk.FLAT,
#                        cursor="hand2",
#                        activebackground=self.colors['button_hover'],
#                        activeforeground=self.colors['fg'])
        
#         # Effetto hover
#         btn.bind("<Enter>", lambda e: btn.config(bg=self.colors['button_hover']))
#         btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        
#         return btn
    
#     def login(self):
#         """Gestisce il login"""
#         username = self.username_entry.get()
#         password = self.password_entry.get()
        
#         if not username or not password:
#             messagebox.showerror("Errore", "Inserisci username e password")
#             return
        
#         if self.manager.login(username, password):
#             messagebox.showinfo("Successo", f"Benvenuto {username}!")
#             self.show_main_interface()
#         else:
#             messagebox.showerror("Errore", "Credenziali non valide")
#             self.password_entry.delete(0, tk.END)
    
#     def register(self):
#         """Gestisce la registrazione"""
#         username = self.username_entry.get()
#         password = self.password_entry.get()
        
#         if not username or not password:
#             messagebox.showerror("Errore", "Inserisci username e password")
#             return
        
#         if self.manager.register_user(username, password):
#             messagebox.showinfo("Successo", "Registrazione completata! Ora puoi effettuare il login.")
#             self.password_entry.delete(0, tk.END)
#         else:
#             messagebox.showerror("Errore", "Registrazione fallita. L'utente potrebbe già esistere.")
    
#     def refresh_list(self):
#         """Aggiorna la lista dei servizi"""
#         self.services_listbox.delete(0, tk.END)
#         services = self.manager.list_services()
        
#         if services:
#             for _, service_name in services:
#                 self.services_listbox.insert(tk.END, f"  🔐  {service_name}")
#         else:
#             self.services_listbox.insert(tk.END, "  Nessun servizio salvato")
    
#     def show_password_from_list(self, event):
#         """Mostra la password del servizio selezionato"""
#         selection = self.services_listbox.curselection()
#         if selection:
#             index = selection[0]
#             service_text = self.services_listbox.get(index)
#             # Rimuovi l'icona e gli spazi
#             service_name = service_text.replace("  🔐  ", "").strip()
            
#             if service_name != "Nessun servizio salvato":
#                 pwd = self.manager.get_password(service_name)
#                 if pwd:
#                     self.password_display.config(
#                         text=f"Password per {service_name}:\n\n{pwd}",
#                         font=("Arial", 12, "bold"),
#                         fg=self.colors['select_bg']
#                     )
#                 else:
#                     self.password_display.config(
#                         text="Password non trovata",
#                         font=("Arial", 10, "italic"),
#                         fg='#ff6666'
#                     )
    
#     def add_password(self):
#         """Aggiunge una nuova password"""
#         service = simpledialog.askstring("Nuovo Servizio", "Nome del servizio:")
#         if service:
#             pwd = simpledialog.askstring("Password", f"Password per {service}:", show="*")
#             if pwd:
#                 self.manager.add_password(service, pwd)
#                 messagebox.showinfo("Successo", f"Password per {service} salvata!")
#                 self.refresh_list()
    
#     def update_password(self):
#         """Aggiorna una password esistente"""
#         selection = self.services_listbox.curselection()
#         if not selection:
#             messagebox.showwarning("Attenzione", "Seleziona un servizio dalla lista")
#             return
        
#         service_text = self.services_listbox.get(selection[0])
#         service_name = service_text.replace("  🔐  ", "").strip()
        
#         if service_name != "Nessun servizio salvato":
#             new_pwd = simpledialog.askstring("Aggiorna Password", 
#                                             f"Nuova password per {service_name}:", show="*")
#             if new_pwd:
#                 self.manager.update_password(service_name, new_pwd)
#                 messagebox.showinfo("Successo", f"Password per {service_name} aggiornata!")
#                 self.password_display.config(
#                     text="Password aggiornata con successo",
#                     font=("Arial", 10, "italic"),
#                     fg='#66ff66'
#                 )
    
#     def delete_password(self):
#         """Elimina una password"""
#         selection = self.services_listbox.curselection()
#         if not selection:
#             messagebox.showwarning("Attenzione", "Seleziona un servizio dalla lista")
#             return
        
#         service_text = self.services_listbox.get(selection[0])
#         service_name = service_text.replace("  🔐  ", "").strip()
        
#         if service_name != "Nessun servizio salvato":
#             if messagebox.askyesno("Conferma", f"Eliminare la password per {service_name}?"):
#                 self.manager.delete_password(service_name)
#                 messagebox.showinfo("Successo", f"Password per {service_name} eliminata!")
#                 self.refresh_list()
#                 self.password_display.config(
#                     text="Doppio click su un servizio per vedere la password",
#                     font=("Arial", 10, "italic"),
#                     fg='#888888'
#                 )
    
#     def logout(self):
#         """Effettua il logout"""
#         if messagebox.askyesno("Logout", "Vuoi davvero uscire?"):
#             self.manager.user_id = None
#             self.manager.cipher = None
#             self.show_login_frame()


# if __name__ == "__main__":
#     # Inizializza database e password manager
#     db = DatabaseConnection()
#     db.open()
#     pm = PasswordManager(db)
    
#     # Crea la finestra principale
#     root = tk.Tk()
#     root.geometry("800x500")
#     root.minsize(700, 400)
    
#     # Crea e avvia l'applicazione
#     app = PasswordManagerGUI(root, pm)
#     root.mainloop()
    
#     # Chiudi il database alla chiusura
#     db.close()