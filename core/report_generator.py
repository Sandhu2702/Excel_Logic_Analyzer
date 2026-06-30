import pandas as pd


def generate_report(source_file, target_file):

    source_df = pd.read_excel(source_file)
    target_df = pd.read_excel(target_file)

    # -----------------------------------
    # Common Relationships
    # -----------------------------------

    common_columns = list(
        set(source_df.columns) &
        set(target_df.columns)
    )

    # -----------------------------------
    # Application Type Detection
    # -----------------------------------

    all_columns = [
        str(col).lower()
        for col in (
            list(source_df.columns)
            + list(target_df.columns)
        )
    ]

    application_type = "Business Management System"

    if (
        any("employee" in col for col in all_columns)
        and any("salary" in col for col in all_columns)
        and any("performance" in col for col in all_columns)
    ):
        application_type = (
            "Employee Performance & Payroll Management System"
        )

    elif (
        any("employee" in col for col in all_columns)
        and any("salary" in col for col in all_columns)
    ):
        application_type = (
            "Employee Payroll Management System"
        )

    elif any("employee" in col for col in all_columns):
        application_type = (
            "Employee Management System"
        )

    elif (
        any("product" in col for col in all_columns)
        or any("inventory" in col for col in all_columns)
        or any("stock" in col for col in all_columns)
    ):
        application_type = (
            "Inventory Management System"
        )

    elif (
        any("customer" in col for col in all_columns)
        or any("order" in col for col in all_columns)
    ):
        application_type = (
            "Customer Order Management System"
        )

    # -----------------------------------
    # Database Table Generation
    # -----------------------------------

    source_table = "source_data"
    target_table = "target_data"

    if "Employee" in application_type:
        source_table = "employee_master"
        target_table = "employee_payroll"

    elif "Inventory" in application_type:
        source_table = "product_master"
        target_table = "inventory_records"

    elif "Customer" in application_type:
        source_table = "customer_master"
        target_table = "customer_orders"

    # -----------------------------------
    # Business Rule Detection
    # -----------------------------------

    business_rules = []

    target_cols = [
        str(col).lower()
        for col in target_df.columns
    ]

    if (
        "bonus %" in target_cols
        and "bonus amount" in target_cols
    ):
        business_rules.append(
            "Bonus Amount may be derived from Salary × Bonus %"
        )

    if (
        "tax" in target_cols
        and "final pay" in target_cols
    ):
        business_rules.append(
            "Final Pay may be derived using Salary, Bonus Amount and Tax"
        )

    # -----------------------------------
    # Dynamic Modules
    # -----------------------------------

    modules = []

    if "Employee" in application_type:

        modules.extend([
            "Employee Management",
            "Performance Management",
            "Payroll Management"
        ])

    elif "Inventory" in application_type:

        modules.extend([
            "Product Management",
            "Inventory Tracking",
            "Stock Reporting"
        ])

    elif "Customer" in application_type:

        modules.extend([
            "Customer Management",
            "Order Management",
            "Sales Reporting"
        ])

    else:

        modules.extend([
            "Data Management",
            "Reporting",
            "Analytics"
        ])

    return {

        "source_columns": list(source_df.columns),

        "target_columns": list(target_df.columns),

        "relationships": common_columns,

        "source_rows": len(source_df),

        "target_rows": len(target_df),

        "application_type": application_type,

        "business_rules": business_rules,

        "modules": modules,

        "source_table": source_table,

        "target_table": target_table
    }