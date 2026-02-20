import customtkinter as ctk
from ui.landing import Landing
from ui.login import Login
from ui.register import Register
from ui.dashboard import Dashboard


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Arbeitszeiten Tool")

        # Responsive window
        self.minsize(1000, 700)
        self.state("zoomed")  # Windows fullscreen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.current_user = None

        self.show_landing()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_landing(self):
        self.clear()
        Landing(self, self)

    def show_login(self):
        self.clear()
        Login(self, self)

    def show_register(self):
        self.clear()
        Register(self, self)

    def show_dashboard(self, user_id, username):
        self.clear()
        self.current_user = user_id
        Dashboard(self, self, user_id, username)

    def logout(self):
        self.current_user = None
        self.show_landing()


if __name__ == "__main__":
    app = App()
    app.mainloop()
