# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

project_dir = os.getcwd()

# --- DATAS ---
datas = []
datas += collect_data_files("customtkinter")

# Se ti serve ancora .env per altro, abilita questa riga.
# datas += [(os.path.join(project_dir, ".env"), ".")]

# --- Tcl/Tk (Tkinter) ---
python_root = os.path.abspath(os.path.join(os.path.dirname(sys.executable), ".."))
tcl_root = os.path.join(python_root, "tcl")

if os.path.isdir(os.path.join(tcl_root, "tcl8.6")):
    datas += [(os.path.join(tcl_root, "tcl8.6"), "tcl/tcl8.6")]
if os.path.isdir(os.path.join(tcl_root, "tk8.6")):
    datas += [(os.path.join(tcl_root, "tk8.6"), "tcl/tk8.6")]

# --- HIDDEN IMPORTS ---
hiddenimports = []
hiddenimports += collect_submodules("customtkinter")
hiddenimports += ["cryptography", "argon2"]

block_cipher = None

a = Analysis(
    ["main.py"],
    pathex=[project_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "mysql",
        "mysql.connector",
        "mysql.connector.pooling",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ONEFILE: niente exclude_binaries, niente COLLECT
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="PasswordManager",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    icon=os.path.join(project_dir, "passwordManager.ico"),
)
