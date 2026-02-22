import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import datetime
import locale
import os

from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm

from openpyxl import Workbook

from utils.calculation import calculate
from email_service import send_email
from database import get_connection
from settings import save_settings

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Dashboard(ctk.CTkFrame):

    def __init__(self, parent, app, user_id, username):
        super().__init__(parent)

        self.app = app
        self.user_id = user_id
        self.username = username
        self.current_month = datetime.datetime.now().month

        self.pack(fill="both", expand=True)

        # responsive grid
        for i in range(7):
            self.grid_rowconfigure(i, weight=0)
        self.grid_rowconfigure(5, weight=1)  # table grows
        self.grid_columnconfigure(0, weight=1)

        self.build()
        self.load_data()

    # ================= UI =================

    def build(self):

        # TOP BAR
        top = ctk.CTkFrame(self, height=60)
        top.grid(row=0, column=0, sticky="ew", pady=(10, 0))
        top.pack_propagate(False)

        ctk.CTkLabel(
            top,
            text=f"Willkommen, {self.username}",
            font=("Arial", 18, "bold"),
        ).pack(side="left", padx=20)

        ctk.CTkButton(top, text="Theme", width=90, command=self.toggle_theme).pack(
            side="right", padx=10
        )

        ctk.CTkButton(top, text="Logout", width=90, command=self.app.logout).pack(
            side="right", padx=10
        )

        # FILTER
        filter_frame = ctk.CTkFrame(self)
        filter_frame.grid(row=1, column=0, sticky="ew", padx=40, pady=10)

        ctk.CTkLabel(filter_frame, text="Monat:").pack(side="left", padx=5)

        self.month_var = ctk.StringVar(value=str(self.current_month))
        ctk.CTkOptionMenu(
            filter_frame,
            values=[str(i) for i in range(1, 13)],
            variable=self.month_var,
            command=self.change_month,
            width=80,
        ).pack(side="left", padx=5)

        ctk.CTkLabel(filter_frame, text="Suche Datum:").pack(side="left", padx=15)

        self.search_entry = ctk.CTkEntry(filter_frame, width=120)
        self.search_entry.pack(side="left", padx=5)

        ctk.CTkButton(
            filter_frame, text="Suchen", width=80, command=self.search_by_date
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            filter_frame, text="Refresh", width=80, command=self.load_data
        ).pack(side="left", padx=10)

        # SUMMARY
        summary = ctk.CTkFrame(self)
        summary.grid(row=2, column=0, sticky="ew", padx=40, pady=10)

        self.total_income_label = ctk.CTkLabel(
            summary,
            text="Monats Einkommen: 0.00 €",
            font=("Arial", 14, "bold"),
        )
        self.total_income_label.pack(pady=10)

        # CHART
        self.chart_frame = ctk.CTkFrame(self)
        self.chart_frame.grid(row=3, column=0, sticky="ew", padx=40, pady=10)

        self.figure = Figure(figsize=(5, 2.5), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # INPUT
        form = ctk.CTkFrame(self)
        form.grid(row=4, column=0, sticky="ew", padx=40, pady=10)

        self.date = DateEntry(form, width=120)
        self.date.pack(side="left", padx=10)

        self.start = ctk.CTkEntry(form, width=120, placeholder_text="Start (HH:MM)")
        self.start.pack(side="left", padx=10)

        self.end = ctk.CTkEntry(form, width=120, placeholder_text="Ende (HH:MM)")
        self.end.pack(side="left", padx=10)

        ctk.CTkButton(form, text="Speichern", command=self.save).pack(
            side="left", padx=15
        )

        # TABLE
        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=5, column=0, sticky="nsew", padx=40, pady=10)

        columns = (
            "ID",
            "Datum",
            "Start",
            "Ende",
            "Arbeitszeit",
            "Überstunden",
            "Einkommen",
        )

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=110)

        self.tree.pack(fill="both", expand=True)

        # ACTION BAR
        bottom = ctk.CTkFrame(self)
        bottom.grid(row=6, column=0, pady=10)

        ctk.CTkButton(
            bottom, text="⋮ Aktionen", width=130, command=self.show_actions
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            bottom, text="PDF Export", width=130, command=self.export_pdf
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            bottom, text="Excel Export", width=130, command=self.export_excel
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            bottom, text="Email senden", width=130, command=self.email_report
        ).pack(side="left", padx=10)

    # ================= LOGIC =================

    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("light")
            save_settings({"theme": "light"})
        else:
            ctk.set_appearance_mode("dark")
            save_settings({"theme": "dark"})

    def save(self):
        worked, overtime, income = calculate(self.start.get(), self.end.get())

        conn = get_connection()
        c = conn.cursor()

        c.execute(
            """
            INSERT INTO work_entries
            (user_id, date, start, end, worked, overtime, income)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                self.user_id,
                self.date.get_date().strftime("%Y-%m-%d"),
                self.start.get(),
                self.end.get(),
                worked,
                overtime,
                income,
            ),
        )

        conn.commit()
        conn.close()

        self.start.delete(0, "end")
        self.end.delete(0, "end")

        self.load_data()

    def load_data(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        c = conn.cursor()

        c.execute(
            """
            SELECT id, date, start, end, worked, overtime, income
            FROM work_entries
            WHERE user_id=?
            """,
            (self.user_id,),
        )

        rows = c.fetchall()
        conn.close()

        total = 0
        filtered = []

        for r in rows:
            month = int(r[1].split("-")[1])
            if month == int(self.month_var.get()):
                filtered.append(r)

        for r in filtered:
            total += float(r[6])
            display = list(r)
            display[6] = f"{float(r[6]):.2f} €"
            self.tree.insert("", "end", values=display)

        self.total_income_label.configure(text=f"Monats Einkommen: {total:.2f} €")

        self.update_chart(filtered)

    def change_month(self, value):
        self.load_data()

    def search_by_date(self):
        search = self.search_entry.get()
        if not search:
            self.load_data()
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        c = conn.cursor()

        c.execute(
            """
            SELECT id, date, start, end, worked, overtime, income
            FROM work_entries
            WHERE user_id=? AND date LIKE ?
            """,
            (self.user_id, f"%{search}%"),
        )

        rows = c.fetchall()
        conn.close()

        for r in rows:
            display = list(r)
            display[6] = f"{float(r[6]):.2f} €"
            self.tree.insert("", "end", values=display)

    # ================= EDIT / DELETE =================

    def show_actions(self):

        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Hinweis", "Bitte Eintrag auswählen")
            return

        menu = ctk.CTkToplevel(self)
        menu.geometry("220x170")
        menu.title("Aktionen")
        menu.grab_set()

        ctk.CTkButton(
            menu,
            text="Bearbeiten",
            command=lambda: [menu.destroy(), self.open_edit_window()],
        ).pack(pady=15)

        ctk.CTkButton(
            menu,
            text="Löschen",
            fg_color="red",
            command=lambda: [menu.destroy(), self.confirm_delete()],
        ).pack(pady=10)

    def open_edit_window(self):

        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected)["values"]
        entry_id = values[0]

        edit = ctk.CTkToplevel(self)
        edit.geometry("350x300")
        edit.title("Eintrag bearbeiten")
        edit.grab_set()

        date_obj = datetime.datetime.strptime(values[1], "%Y-%m-%d").date()

        date = DateEntry(edit)
        date.set_date(date_obj)
        date.pack(pady=10)

        start = ctk.CTkEntry(edit)
        start.insert(0, values[2])
        start.pack(pady=5)

        end = ctk.CTkEntry(edit)
        end.insert(0, values[3])
        end.pack(pady=5)

        def save_changes():
            worked, overtime, income = calculate(start.get(), end.get())

            conn = get_connection()
            c = conn.cursor()

            c.execute(
                """
                UPDATE work_entries
                SET date=?, start=?, end=?,
                    worked=?, overtime=?, income=?
                WHERE id=?
                """,
                (
                    date.get_date().strftime("%Y-%m-%d"),
                    start.get(),
                    end.get(),
                    worked,
                    overtime,
                    income,
                    entry_id,
                ),
            )

            conn.commit()
            conn.close()

            edit.destroy()
            self.load_data()

        ctk.CTkButton(edit, text="Speichern", command=save_changes).pack(pady=20)

    def confirm_delete(self):

        selected = self.tree.selection()
        if not selected:
            return

        entry_id = self.tree.item(selected)["values"][0]

        confirm = messagebox.askyesno("Bestätigung", "Eintrag wirklich löschen?")

        if confirm:
            conn = get_connection()
            c = conn.cursor()
            c.execute("DELETE FROM work_entries WHERE id=?", (entry_id,))
            conn.commit()
            conn.close()
            self.load_data()

    # ================= EXPORT / EMAIL =================

    def export_pdf(self):
        now = datetime.datetime.now()
        filename = f"Arbeitszeit_{now.strftime('%m_%Y')}.pdf"

        path = filedialog.asksaveasfilename(
            initialfile=filename, defaultextension=".pdf"
        )

        if not path:
            return

        self.generate_pdf(path)

    def generate_pdf(self, path):
        locale.setlocale(locale.LC_TIME, "de_DE")

        doc = SimpleDocTemplate(path, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()
        elements.append(Paragraph("Arbeitszeiten Report", styles["Heading1"]))
        elements.append(Spacer(1, 20))

        data = [self.tree["columns"]]

        for row in self.tree.get_children():
            data.append(self.tree.item(row)["values"])

        table = Table(data)
        table.setStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        )

        elements.append(table)
        doc.build(elements)

    def export_excel(self):
        now = datetime.datetime.now()
        filename = f"Arbeitszeit_{now.strftime('%m_%Y')}.xlsx"

        path = filedialog.asksaveasfilename(
            initialfile=filename, defaultextension=".xlsx"
        )

        if not path:
            return

        wb = Workbook()
        ws = wb.active

        ws.append(self.tree["columns"])

        for row in self.tree.get_children():
            ws.append(self.tree.item(row)["values"])

        wb.save(path)

    def email_report(self):

        export_folder = "exports"
        os.makedirs(export_folder, exist_ok=True)

        filename = f"Arbeitszeit_{datetime.datetime.now().strftime('%m_%Y')}.pdf"
        pdf_path = os.path.join(export_folder, filename)

        self.generate_pdf(pdf_path)

        send_email(
            "chamati@live.com",
            "Arbeitszeit Report",
            "Anbei dein Report.",
            pdf_path,
        )

        messagebox.showinfo("Email", "Email gesendet!")
