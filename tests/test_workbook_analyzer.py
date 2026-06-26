from pprint import pprint

from core.excel_reader import ExcelReader
from core.workbook_analyzer import WorkbookAnalyzer

FILE_PATH = "sample_data/Employee details.xlsx"   # Change this path if needed


def main():

    reader = ExcelReader()

    workbook = reader.read(FILE_PATH)

    analyzer = WorkbookAnalyzer(workbook)

    result = analyzer.analyze()

    pprint(result, sort_dicts=False)


if __name__ == "__main__":
    main()