import customtkinter as ctk
from tkinter import messagebox
from auth import login


class Login(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pack(fill="both", expand=True)

        # soft background
        self.configure(fg_color=("#f4f6f9", "#1e1e1e"))

        self.build()

    def build(self):

        # CENTER CARD
        card = ctk.CTkFrame(self, width=460, corner_radius=25)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # TITLE
        ctk.CTkLabel(card, text="Login", font=("Arial", 30, "bold")).pack(pady=(40, 10))

        # SUBTITLE
        ctk.CTkLabel(card, text="Bitte melde dich an", text_color="gray").pack(
            pady=(0, 25)
        )

        # USERNAME
        self.username = ctk.CTkEntry(card, height=45, placeholder_text="Username")
        self.username.pack(fill="x", padx=40, pady=10)

        # PASSWORD
        self.password = ctk.CTkEntry(
            card, height=45, placeholder_text="Password", show="*"
        )
        self.password.pack(fill="x", padx=40, pady=10)

        # LOGIN BUTTON
        ctk.CTkButton(
            card, text="Login", height=50, corner_radius=12, command=self.handle_login
        ).pack(fill="x", padx=40, pady=(25, 15))

        # SWITCH TO REGISTER
        ctk.CTkButton(
            card,
            text="Noch kein Konto? Registrieren",
            fg_color="transparent",
            text_color=("blue", "lightblue"),
            hover_color=("gray80", "gray20"),
            command=self.app.show_register,
        ).pack(pady=(0, 40))

        # ENTER KEY SUPPORT
        self.bind("<Return>", lambda e: self.handle_login())

    def handle_login(self):

        user_id = login(self.username.get(), self.password.get())

        if user_id:
            self.app.show_dashboard(user_id, self.username.get())
        else:
            messagebox.showerror("Fehler", "Login fehlgeschlagen")
