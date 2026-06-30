from core.excel_reader import ExcelReader
from core.logic_detector import LogicDetector
from core.formula_detector import FormulaDetector


def test_formula_detector():

    reader = ExcelReader()

    workbook = reader.read("sample_data/Performance_benefits.xlsx")

    logic = LogicDetector(workbook)

    logic_output = logic.detect()

    detector = FormulaDetector(logic_output)

    result = detector.detect()

    print(result)


if __name__ == "__main__":
    test_formula_detector()