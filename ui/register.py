import customtkinter as ctk
from tkinter import messagebox
from auth import register


class Register(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pack(fill="both", expand=True)

        self.configure(fg_color=("#f4f6f9", "#1e1e1e"))

        self.build()

    def build(self):

        card = ctk.CTkFrame(self, width=460, corner_radius=25)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="Registrieren", font=("Arial", 30, "bold")).pack(
            pady=(40, 10)
        )

        ctk.CTkLabel(card, text="Erstelle dein Konto", text_color="gray").pack(
            pady=(0, 25)
        )

        self.username = ctk.CTkEntry(card, height=45, placeholder_text="Username")
        self.username.pack(fill="x", padx=40, pady=10)

        self.password = ctk.CTkEntry(
            card, height=45, placeholder_text="Password", show="*"
        )
        self.password.pack(fill="x", padx=40, pady=10)

        ctk.CTkButton(
            card,
            text="Account erstellen",
            height=50,
            corner_radius=12,
            command=self.handle_register,
        ).pack(fill="x", padx=40, pady=(25, 15))

        ctk.CTkButton(
            card,
            text="Schon ein Konto? Login",
            fg_color="transparent",
            text_color=("blue", "lightblue"),
            hover_color=("gray80", "gray20"),
            command=self.app.show_login,
        ).pack(pady=(0, 40))

    def handle_register(self):

        username = self.username.get()
        password = self.password.get()

        success, message = register(username, password)

        if success:
            messagebox.showinfo("Erfolg", message)
            self.app.show_login()
        else:
            messagebox.showerror("Fehler", message)
