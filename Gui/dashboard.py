import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Dashboard(ctk.CTkToplevel):

    def __init__(self, parent, merged_df, formula_results, lookup_results, condition_results, relationship_results):
        super().__init__(parent)

        self.title("Excel Logic Analyzer Dashboard")
        self.geometry("1100x700")

        self.merged_df = merged_df
        self.formula_results = formula_results
        self.lookup_results = lookup_results
        self.condition_results = condition_results
        self.relationship_results = relationship_results

        title = ctk.CTkLabel(self, text="Excel Logic Analyzer Dashboard", font=("Arial", 28, "bold"))
        title.pack(pady=20)

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=20)

        self.tabs.add("Workbook Summary")
        self.tabs.add("Logic Report")
        self.tabs.add("Charts")   # ✅ New Tab

        self.create_summary_tab()
        self.create_logic_report_tab()
        self.create_charts_tab()  # ✅ Call chart function

    def create_summary_tab(self):
        tab = self.tabs.tab("Workbook Summary")
        textbox = ctk.CTkTextbox(tab, width=950, height=550)
        textbox.pack(padx=20, pady=20, fill="both", expand=True)

        summary_text = f"Rows: {len(self.merged_df)}\nColumns: {len(self.merged_df.columns)}\n\n"
        summary_text += "Column Names:\n"
        for col in self.merged_df.columns:
            summary_text += f"   • {col}\n"

        textbox.insert("1.0", summary_text)
        textbox.configure(state="disabled")

    def create_logic_report_tab(self):

       tab = self.tabs.tab("Logic Report")

       textbox = ctk.CTkTextbox(
          tab,
          width=950,
          height=550
       )

       textbox.pack(
          padx=20,
          pady=20,
          fill="both",
          expand=True
          )

       report = ""

       report += "========== FORMULAS ==========\n\n"

       total_formulas = 0

       for sheet_name, formulas in self.formula_results.items():

          report += f"\nSheet: {sheet_name}\n"

          for formula in formulas:

            total_formulas += 1

            report += (
                f'Cell: {formula["cell"]} | '
                f'Function: {formula.get("function")} | '
                f'Category: {formula["category"]}\n'
            )

          report += f"\nTotal Formulas: {total_formulas}\n\n"

          report += "\n========== LOOKUPS ==========\n\n"

          for sheet_name, lookups in self.lookup_results.items():

            for lookup in lookups:

              report += (
                 f'{lookup["cell"]} -> '
                 f'{lookup["lookup_type"]}\n'
              )

          report += "\n========== CONDITIONS ==========\n\n"

          if len(self.condition_results) == 0:

             report += "No conditions detected.\n"

          else:

             for condition in self.condition_results:

               report += (
                  f'{condition["condition"]} '
                  f'({condition["operator"]})\n'
               )

             report += "\n========== RELATIONSHIPS ==========\n\n"

          for relation in self.relationship_results["relationships"]:

            report += (
              f'{relation["relationship"]} | '
              f'{relation["target_column"]}\n'
            )

          textbox.insert("1.0", report)

          textbox.configure(state="disabled")

          def export_results(self):
            try:
                self.merged_df.to_excel("output_report.xlsx", index=False)
                messagebox.showinfo("Export", "Report exported successfully as output_report.xlsx")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")

    def create_charts_tab(self):
        tab = self.tabs.tab("Charts")

        # ✅ Department-wise Average Salary
        dept_salary = self.merged_df.groupby("Department")["Salary"].mean()

        fig, ax = plt.subplots(figsize=(6,4))
        dept_salary.plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title("Department-wise Average Salary")
        ax.set_ylabel("Average Salary")
        ax.set_xlabel("Department")

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20, fill="both", expand=True)
