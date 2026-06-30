import customtkinter as ctk
from tkinter import filedialog
import os
from core.workbook_analyzer import WorkbookAnalyzer
from core.column_mapper import ColumnMapper
from core.logic_detector import LogicDetector
from core.formula_detector import FormulaDetector
from core.lookup_detector import LookupDetector
from core.condition_detector import ConditionDetector
from core.relationship_detector import RelationshipDetector
from core.excel_reader import ExcelReader
from core.report_generator import generate_report
from gui.dashboard import Dashboard


class HomeScreen(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.source_file = ""
        self.target_file = ""

        self.create_ui()

    def create_ui(self):
        card = ctk.CTkFrame(self, corner_radius=15)
        card.pack(padx=100, pady=50, fill="both", expand=True)

        title = ctk.CTkLabel(card, text="Excel Logic Analyzer", font=("Arial", 32, "bold"))
        title.pack(pady=(30, 10))

        subtitle = ctk.CTkLabel(card, text="Reverse Engineer Business Logic From Excel Files", font=("Arial", 14))
        subtitle.pack(pady=(0, 25))

        # Source Upload
        self.source_btn = ctk.CTkButton(card, text="📂 Upload Source Excel", command=self.select_source, width=300, height=45)
        self.source_btn.pack(pady=10)
        self.source_label = ctk.CTkLabel(card, text="No source file selected")
        self.source_label.pack()

        # Target Upload
        self.target_btn = ctk.CTkButton(card, text="📂 Upload Target Excel", command=self.select_target, width=300, height=45)
        self.target_btn.pack(pady=20)
        self.target_label = ctk.CTkLabel(card, text="No target file selected")
        self.target_label.pack()

        # Status
        self.status_label = ctk.CTkLabel(card, text="Status : Waiting for files...")
        self.status_label.pack(pady=25)

        # Analyze Button
        self.analyze_btn = ctk.CTkButton(card, text="Analyze Files", width=300, height=50, command=self.analyze_files)
        self.analyze_btn.pack(pady=20)

    def select_source(self):
        file = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls")])
        if file:
            self.source_file = file
            self.source_label.configure(text=os.path.basename(file))

    def select_target(self):
        file = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls")])
        if file:
            self.target_file = file
            self.target_label.configure(text=os.path.basename(file))

    def analyze_files(self):

        if not self.source_file or not self.target_file:
            self.status_label.configure(
              text="Please select both files first."
            )
            return
        
        try:

            self.status_label.configure(
               text="Analyzing files..."
            )

            # Existing merged report
            merged_df = generate_report(
                self.source_file,
                self.target_file
            )

            # Read workbooks
            reader = ExcelReader()

            source_data = reader.read(
                self.source_file
            )

            target_data = reader.read(
                self.target_file
            )

            # Analyze workbook structure
            source_profile = WorkbookAnalyzer(
                source_data
            ).analyze()

            target_profile = WorkbookAnalyzer(
                target_data
            ).analyze()

            # Column mapping
            column_mappings = ColumnMapper(
                source_profile,
                target_profile
            ).map_columns()

            # Detect formulas
            logic_results = LogicDetector(
                target_data
            ).detect()

            # Formula classification
            formula_results = FormulaDetector(
                logic_results
            ).detect()

            # Lookup detection
            lookup_results = LookupDetector(
                formula_results
            ).detect()

            # Condition detection
            condition_results = ConditionDetector(
                formula_results
            ).detect()

           # Relationship detection
            relationship_results = RelationshipDetector(
                source_profile,
                target_profile,
                column_mappings,
                lookup_results
            ).detect()

            Dashboard(
               self,
               merged_df,
               formula_results,
               lookup_results,
               condition_results,
               relationship_results
            )

            self.status_label.configure(
                text="Analysis completed successfully ✅"
            )

        except Exception as e:

            self.status_label.configure(
                text=f"Error : {e}"
            )


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Excel Logic Analyzer")
    app.geometry("1000x700")

    HomeScreen(app)
    app.mainloop()
