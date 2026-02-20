import customtkinter as ctk


class Landing(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pack(fill="both", expand=True)
        self.build()

    def build(self):

        ctk.CTkLabel(self, text="Arbeitszeiten Tool", font=("Arial", 28, "bold")).pack(
            pady=40
        )

        ctk.CTkButton(self, text="Login", width=200, command=self.app.show_login).pack(
            pady=10
        )

        ctk.CTkButton(
            self, text="Registrieren", width=200, command=self.app.show_register
        ).pack(pady=10)

        ctk.CTkButton(self, text="Theme wechseln", command=self.toggle_theme).pack(
            pady=30
        )

    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
