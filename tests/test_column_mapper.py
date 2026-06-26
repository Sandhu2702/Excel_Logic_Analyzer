from core.column_mapper import ColumnMapper


def test_column_mapper():

    workbook_profile = {
        "worksheets": {
            "Payroll": {
                "headers": [
                    "Emp ID",
                    "Employee Name",
                    "Basic Salary",
                    "HRA",
                    "PF",
                    "Net Pay"
                ]
            },
            "Attendance": {
                "headers": [
                    "Emp ID",
                    "Date",
                    "Status"
                ]
            }
        }
    }

    mapper = ColumnMapper(workbook_profile)

    result = mapper.map_columns()

    print(result)

if __name__ == "__main__":
    test_column_mapper()