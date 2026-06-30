from core.report_generator import generate_report
import json

source_file = "sample_data/Employee Details.xlsx"
target_file = "sample_data/PERFORMANCE.xlsx"

result = generate_report(
    source_file,
    target_file
)

print(json.dumps(result, indent=4))