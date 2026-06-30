import customtkinter as ctk
from tkinter import filedialog
import os

from core.report_generator import generate_report
from gui.dashboard import Dashboard
from core.app_generator import generate_flask_app


class HomeScreen(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill="both", expand=True)

        self.source_file = ""
        self.target_file = ""

        self.create_ui()

    def create_ui(self):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.pack(
            padx=100,
            pady=50,
            fill="both",
            expand=True
        )

        # Title

        title = ctk.CTkLabel(
            card,
            text="Excel Application Generator",
            font=("Arial", 32, "bold")
        )

        title.pack(pady=(30, 10))

        # Subtitle

        subtitle = ctk.CTkLabel(
            card,
            text="Generate Business Application Structure From Interrelated Excel Files",
            font=("Arial", 14)
        )

        subtitle.pack(pady=(0, 25))

        # ----------------------------------
        # Source Upload
        # ----------------------------------

        self.source_btn = ctk.CTkButton(
            card,
            text="📂 Upload Source Excel",
            command=self.select_source,
            width=300,
            height=45
        )

        self.source_btn.pack(pady=10)

        self.source_label = ctk.CTkLabel(
            card,
            text="No source file selected"
        )

        self.source_label.pack()

        # ----------------------------------
        # Target Upload
        # ----------------------------------

        self.target_btn = ctk.CTkButton(
            card,
            text="📂 Upload Target Excel",
            command=self.select_target,
            width=300,
            height=45
        )

        self.target_btn.pack(pady=20)

        self.target_label = ctk.CTkLabel(
            card,
            text="No target file selected"
        )

        self.target_label.pack()

        # ----------------------------------
        # Status
        # ----------------------------------

        self.status_label = ctk.CTkLabel(
            card,
            text="Status : Waiting for files..."
        )

        self.status_label.pack(pady=25)

        # ----------------------------------
        # Analyze Button
        # ----------------------------------

        self.analyze_btn = ctk.CTkButton(
            card,
            text="Generate Application Design",
            width=300,
            height=50,
            command=self.analyze_files
        )

        self.analyze_btn.pack(pady=20)

    # ----------------------------------
    # Select Source File
    # ----------------------------------

    def select_source(self):

        file = filedialog.askopenfilename(
            filetypes=[("Excel Files", "*.xlsx *.xls")]
        )

        if file:

            self.source_file = file

            self.source_label.configure(
                text=os.path.basename(file)
            )

    # ----------------------------------
    # Select Target File
    # ----------------------------------

    def select_target(self):

        file = filedialog.askopenfilename(
            filetypes=[("Excel Files", "*.xlsx *.xls")]
        )

        if file:

            self.target_file = file

            self.target_label.configure(
                text=os.path.basename(file)
            )

    # ----------------------------------
    # Analyze Files
    # ----------------------------------

    def analyze_files(self):

        if not self.source_file or not self.target_file:

            self.status_label.configure(
                text="Please select both Excel files first."
            )

            return

        try:

            self.status_label.configure(
                text="Application Generated Successfully ✅"
            )

            report = generate_report(
                self.source_file,
                self.target_file
            )

            generate_flask_app(report)

            Dashboard(
                self,
                report
            )

            self.status_label.configure(
                text="Application design generated successfully ✅"
            )

        except Exception as e:

            self.status_label.configure(
                text=f"Error : {e}"
            )


if __name__ == "__main__":

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()

    app.title("Excel Application Generator")

    app.geometry("1000x700")

    HomeScreen(app)

    app.mainloop()