from core.excel_reader import ExcelReader
from core.logic_detector import LogicDetector
from core.formula_detector import FormulaDetector
from core.lookup_detector import LookupDetector


def main():
    file_path = "sample_data/Employee details.xlsx"

    reader = ExcelReader()
    workbook = reader.read(file_path)

    logic = LogicDetector(workbook).detect()
    analyzed = FormulaDetector(logic).detect()

    detector = LookupDetector(analyzed)

    lookups = detector.detect()

    print("\n===== LOOKUP FORMULAS =====")

    for sheet, formulas in lookups.items():
        print(f"\nSheet: {sheet}")

        if not formulas:
            print("No lookup formulas found.")
            continue

        for formula in formulas:
            print(formula)

    print("\n===== SUMMARY =====")
    print(detector.summary(lookups))


if __name__ == "__main__":
    main()