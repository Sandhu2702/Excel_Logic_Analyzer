from core.excel_reader import ExcelReader
from core.logic_detector import LogicDetector


def test_logic_detector():

    reader = ExcelReader()

    workbook = reader.read("sample_data/PERFORMANCE.xlsx")

    detector = LogicDetector(workbook)

    result = detector.detect()

    print(result)


if __name__ == "__main__":
    test_logic_detector()