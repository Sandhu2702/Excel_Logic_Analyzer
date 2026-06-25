from core.excel_reader import ExcelReader

reader = ExcelReader()

source = reader.read("sample_data/Employee details.xlsx")

print("=" * 50)
print("Workbook Name :", source.file_name)
print("Sheet Count   :", source.sheet_count)
print("Sheet Names   :", source.sheet_names)
print("=" * 50)

for sheet_name, info in source.metadata.items():

    print(f"\nSheet : {sheet_name}")
    print("-" * 40)

    print("Rows      :", info["rows"])
    print("Columns   :", info["columns"])
    print("Column Names:")
    print(info["column_names"])

    print("\nData Types:")
    print(info["data_types"])

    print("\nMissing Values:")
    print(info["missing_values"])

    print("\nDuplicate Rows:")
    print(info["duplicate_rows"])