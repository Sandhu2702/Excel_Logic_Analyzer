import pandas as pd

from core.database_relationship_detector import (
    DatabaseRelationshipDetector
)

employee_df = pd.DataFrame({
    "emp_id": [101, 102, 103],
    "emp_name": ["John", "Mike", "Sara"]
})

payroll_df = pd.DataFrame({
    "payroll_id": [1, 2, 3],
    "emp_id": [101, 102, 103],
    "salary": [50000, 60000, 70000]
})

tables = {
    "employee_master": employee_df,
    "payroll_data": payroll_df
}

detector = DatabaseRelationshipDetector(tables)

print(detector.detect_primary_keys())

print("\nRelationships:\n")

for relation in detector.detect_foreign_keys():
    print(relation)