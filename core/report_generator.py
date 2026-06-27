import pandas as pd

def generate_report(emp_file, perf_file):
    # Read both Excel files
    emp_df = pd.read_excel(emp_file)
    perf_df = pd.read_excel(perf_file)

    # Merge on Employee ID
    merged = pd.merge(emp_df, perf_df, on="Employee ID", how="inner")

    return merged
