from core.column_mapper import ColumnMapper


def test_column_mapper():

    source_profile = {
        "worksheets": {
            "Employees": {
                "headers": [
                    "Employee ID",
                    "Employee Name",
                    "Department",
                    "Basic Salary",
                    "HRA",
                    "PF"
                ]
            }
        }
    }

    target_profile = {
        "worksheets": {
            "Performance": {
                "headers": [
                    "Emp ID",
                    "Name",
                    "Department",
                    "Basic Salary",
                    "Net Pay",
                    "HRA"
                ]
            }
        }
    }

    mapper = ColumnMapper(source_profile, target_profile)

    mappings = mapper.map_columns()

    print("\n===== COLUMN MAPPINGS =====\n")

    for mapping in mappings:
        print(mapping)

    print("\n===== SUMMARY =====\n")
    print(mapper.summary(mappings))


if __name__ == "__main__":
    test_column_mapper()