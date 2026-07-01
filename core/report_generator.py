import pandas as pd


def generate_report(source_file, target_file):

    source_df = pd.read_excel(source_file)
    target_df = pd.read_excel(target_file)

    # ==========================================
    # Relationship Detection
    # ==========================================

    common_columns = list(
        set(source_df.columns) &
        set(target_df.columns)
    )

    # ==========================================
    # Column Analysis
    # ==========================================

    all_columns = [
        str(col).lower()
        for col in (
            list(source_df.columns)
            + list(target_df.columns)
        )
    ]

    # ==========================================
    # Application Type Detection
    # ==========================================

    application_type = "Business Management System"

    # Employee + Payroll

    if (
        any("employee" in col for col in all_columns)
        and (
            any("salary" in col for col in all_columns)
            or any("bonus" in col for col in all_columns)
            or any("tax" in col for col in all_columns)
        )
    ):

        application_type = (
            "Employee & Payroll Management System"
        )

    # Employee Only

    elif any("employee" in col for col in all_columns):

        application_type = (
            "Employee Management System"
        )

    # Customer

    elif (
        any("customer" in col for col in all_columns)
        or any("order" in col for col in all_columns)
    ):

        application_type = (
            "Customer Order Management System"
        )

    # Inventory

    elif (
        any("product" in col for col in all_columns)
        or any("inventory" in col for col in all_columns)
        or any("stock" in col for col in all_columns)
    ):

        application_type = (
            "Inventory Management System"
        )

    # Sales

    elif (
        any("sales" in col for col in all_columns)
        or any("revenue" in col for col in all_columns)
    ):

        application_type = (
            "Sales Management System"
        )

    # ==========================================
    # Database Table Names
    # ==========================================

    source_table = "source_data"
    target_table = "target_data"

    if "Employee" in application_type:

        source_table = "employee_master"

        if "Payroll" in application_type:
            target_table = "payroll_data"
        else:
            target_table = "employee_data"

    elif "Customer" in application_type:

        source_table = "customer_master"
        target_table = "customer_orders"

    elif "Inventory" in application_type:

        source_table = "product_master"
        target_table = "inventory_records"

    elif "Sales" in application_type:

        source_table = "sales_master"
        target_table = "sales_reports"

    # ==========================================
    # Business Rule Detection
    # ==========================================

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
            "Bonus Amount may be derived from Bonus %"
        )

    if (
        "tax" in target_cols
        and "final pay" in target_cols
    ):

        business_rules.append(
            "Final Pay may be derived after tax calculation"
        )

    if (
        "order amount" in target_cols
        and "customer id" in target_cols
    ):

        business_rules.append(
            "Order Amount is linked to Customer records"
        )

    if (
        "stock" in target_cols
        and "product id" in target_cols
    ):

        business_rules.append(
            "Stock records are linked to Product records"
        )

    # ==========================================
    # Module Detection
    # ==========================================

    modules = []

    if "Employee & Payroll" in application_type:

        modules.extend([
            "Employee Management",
            "Payroll Management",
            "Reports & Analytics",
            "Search & Filter"
        ])

    elif "Employee" in application_type:

        modules.extend([
            "Employee Management",
            "Reports & Analytics",
            "Search & Filter"
        ])

    elif "Customer" in application_type:

        modules.extend([
            "Customer Management",
            "Order Management",
            "Reports & Analytics",
            "Search & Filter"
        ])

    elif "Inventory" in application_type:

        modules.extend([
            "Product Management",
            "Inventory Management",
            "Stock Reports",
            "Search & Filter"
        ])

    elif "Sales" in application_type:

        modules.extend([
            "Sales Management",
            "Revenue Reports",
            "Analytics",
            "Search & Filter"
        ])

    else:

        modules.extend([
            "Data Management",
            "Reports",
            "Analytics",
            "Search & Filter"
        ])

    tables = [
      {
        "table_name": source_table,
        "columns": list(source_df.columns)
      },
      {
        "table_name": target_table,
        "columns": list(target_df.columns)
      }
    ]

    from core.database_relationship_detector import (
        DatabaseRelationshipDetector
    )

    detector = DatabaseRelationshipDetector({
        source_table: source_df,
        target_table: target_df
    })

    primary_keys = detector.detect_primary_keys()

    relationship_metadata = (
        detector.detect_foreign_keys()
    )

    source_column_types = {
      col: str(dtype)
      for col, dtype in source_df.dtypes.items()
    }

    target_column_types = {
      col: str(dtype)
      for col, dtype in target_df.dtypes.items()
    }

    print("\n===== RELATIONSHIP DEBUG =====")
    print("Primary Keys:")
    print(primary_keys)

    print("\nRelationships:")
    print(relationship_metadata)
    print("==============================\n")

    return {

        "source_columns": list(source_df.columns),

        "target_columns": list(target_df.columns),

        "source_column_types": source_column_types,

        "target_column_types": target_column_types,

        "primary_keys": primary_keys,

        "relationships": relationship_metadata,

        "source_rows": len(source_df),

        "target_rows": len(target_df),

        "application_type": application_type,

        "business_rules": business_rules,

        "modules": modules,

        "source_table": source_table,

        "target_table": target_table,

        "tables": tables
        
    }