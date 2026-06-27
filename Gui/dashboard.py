import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Dashboard(ctk.CTkToplevel):

    def __init__(self, parent, merged_df):
        super().__init__(parent)

        self.title("Excel Logic Analyzer Dashboard")
        self.geometry("1100x700")

        self.merged_df = merged_df

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

        columns = list(self.merged_df.columns)
        tree = ttk.Treeview(tab, columns=columns, show="headings", height=15)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        for _, row in self.merged_df.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(pady=20, fill="both", expand=True)

        export_btn = ctk.CTkButton(tab, text="Export to Excel", command=self.export_results)
        export_btn.pack(pady=10)

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
