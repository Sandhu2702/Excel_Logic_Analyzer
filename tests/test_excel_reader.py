from core.excel_reader import ExcelReader


def test_excel_reader():

    reader = ExcelReader()

    workbook = reader.read("sample_data/Employee_details.xlsx")

    print(type(workbook.workbook))
    print(workbook.workbook.sheetnames)


if __name__ == "__main__":
    test_excel_reader()