import customtkinter as ctk

def toggle_theme(current_mode):

    if current_mode == "dark":
        ctk.set_appearance_mode("light")
        return "light"
    else:
        ctk.set_appearance_mode("dark")
        return "dark"