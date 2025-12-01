# app_styles.py
import tkinter as tk
from tkinter import ttk

BG_MAIN = "#f0f2f5"
BG_PANEL = "#ffffff"
FG_TITLE = "#1f4e79"
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_SUBTITLE = ("Segoe UI", 12, "bold")
FONT_TEXT = ("Segoe UI", 10)

def setup_style():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        font=("Segoe UI", 9),
        rowheight=22
    )
    style.configure(
        "TButton",
        font=("Segoe UI", 9)
    )
