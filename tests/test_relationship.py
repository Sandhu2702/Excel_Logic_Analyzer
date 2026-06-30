from core.excel_reader import ExcelReader
from core.workbook_analyzer import WorkbookAnalyzer
from core.column_mapper import ColumnMapper
from core.logic_detector import LogicDetector
from core.formula_detector import FormulaDetector
from core.lookup_detector import LookupDetector
from core.relationship_detector import RelationshipDetector

SOURCE = "sample_data/Employee_details.xlsx"
TARGET = "sample_data/Performance_benefits.xlsx"

reader = ExcelReader()

# Read workbooks
source_data = reader.read(SOURCE)
target_data = reader.read(TARGET)

# Analyze workbook structure
source_profile = WorkbookAnalyzer(source_data).analyze()
target_profile = WorkbookAnalyzer(target_data).analyze()

# Column mapping
mapper = ColumnMapper(source_profile, target_profile)
column_mappings = mapper.map_columns()

# Detect formulas in target workbook
logic = LogicDetector(target_data).detect()

# Analyze formulas
formula_analysis = FormulaDetector(logic).detect()

# Detect lookup formulas
lookup_data = LookupDetector(formula_analysis).detect()

# Detect relationships
relationships = RelationshipDetector(
    source_profile,
    target_profile,
    column_mappings,
    lookup_data
).detect()

print("\n========== RELATIONSHIPS ==========\n")

for relation in relationships["relationships"]:
    print(relation)

print("\n========== SUMMARY ==========\n")

summary = RelationshipDetector(
    source_profile,
    target_profile,
    column_mappings,
    lookup_data
).summary(relationships)

print(summary)