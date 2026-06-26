"""
Integration test for ConditionDetector.

Pipeline:
ExcelReader
    ↓
WorkbookAnalyzer
    ↓
LogicDetector
    ↓
FormulaDetector
    ↓
ConditionDetector
"""

from core.excel_reader import ExcelReader
from core.workbook_analyzer import WorkbookAnalyzer
from core.logic_detector import LogicDetector
from core.formula_detector import FormulaDetector
from core.condition_detector import ConditionDetector


SOURCE_FILE = "sample_data/Employee Details.xlsx"
TARGET_FILE = "sample_data/PERFORMANCE.xlsx"


def test_condition_detector():

    print("\n========== READING WORKBOOKS ==========\n")

    source_reader = ExcelReader()
    source_data = source_reader.read(SOURCE_FILE)

    target_reader = ExcelReader()
    target_data = target_reader.read(TARGET_FILE)

    print("Source workbook loaded.")
    print("Target workbook loaded.")

    print("\n========== ANALYZING WORKBOOKS ==========\n")

    source_profile = WorkbookAnalyzer(source_data).analyze()
    target_profile = WorkbookAnalyzer(target_data).analyze()

    print("Workbook analysis completed.")

    print("\n========== DETECTING FORMULAS ==========\n")

    logic_detector = LogicDetector(target_data)
    logic_results = logic_detector.detect()

    print("\n========== LOGIC RESULTS ==========\n")
    print("Type:", type(logic_results))
    print("Value:", logic_results)

    total_formulas = sum(len(formulas) for formulas in logic_results.values())
    print(f"Detected {total_formulas} formulas.")

    print("\n========== CLASSIFYING FORMULAS ==========\n")

    formula_detector = FormulaDetector(logic_results)
    formula_results = formula_detector.detect()

    total_classified = sum(len(formulas) for formulas in formula_results.values())
    print(f"Classified {total_classified} formulas.")

    print("\n========== DETECTING CONDITIONS ==========\n")

    detector = ConditionDetector(formula_results)

    print("\n========== FORMULA RESULTS ==========\n")

    print("Type:", type(formula_results))

    print("Value:", formula_results)

    if isinstance(formula_results, list) and len(formula_results) > 0:
       print("\nFirst Item Type:", type(formula_results[0]))
       print("First Item:", formula_results[0])

    conditions = detector.detect()

    for condition in conditions:
        print(condition)

    print("\n========== SUMMARY ==========\n")

    print(detector.summary())


if __name__ == "__main__":
    test_condition_detector()