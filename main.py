# ---------------- MAIN ----------------
from connection import DatabaseConnection
from PasswordManagerGUI import PasswordManagerGUI
from passwordManager import PasswordManager
import customtkinter as ctk


if __name__ == "__main__":
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