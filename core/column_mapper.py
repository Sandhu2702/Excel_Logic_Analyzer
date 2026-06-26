"""
column_mapper.py

Maps workbook column headers to standardized semantic names.

This module does NOT detect business logic.
Its responsibility is only to normalize and standardize
column names across worksheets.
"""

import re


class ColumnMapper:
    """
    Maps worksheet column headers to standardized names.
    """

    ALIASES = {
        # Employee
        "employee id": "employee_id",
        "emp id": "employee_id",
        "empid": "employee_id",
        "employee code": "employee_id",
        "worker code": "employee_id",
        "id": "employee_id",

        "employee name": "employee_name",
        "emp name": "employee_name",
        "name": "employee_name",
        "employee": "employee_name",

        # Salary
        "basic": "basic_salary",
        "basic salary": "basic_salary",
        "base salary": "basic_salary",

        "gross": "gross_salary",
        "gross salary": "gross_salary",

        "net": "net_salary",
        "net pay": "net_salary",
        "net salary": "net_salary",

        "hra": "house_rent_allowance",
        "house rent allowance": "house_rent_allowance",

        "da": "dearness_allowance",
        "dearness allowance": "dearness_allowance",

        "pf": "provident_fund",
        "provident fund": "provident_fund",

        "ot": "overtime_hours",
        "overtime": "overtime_hours",
        "over time": "overtime_hours",

        # Attendance
        "date": "date",
        "attendance date": "date",

        "status": "attendance_status",
        "attendance": "attendance_status",

        # HR
        "department": "department",
        "designation": "designation",
        "joining date": "joining_date",
        "dob": "date_of_birth",
        "birth date": "date_of_birth",
    }

    def __init__(self, source_profile: dict, target_profile: dict):
        """
        Parameters
        ----------
        source_profile : dict
            Output from WorkbookAnalyzer.analyze() for source workbook.

        target_profile : dict
            Output from WorkbookAnalyzer.analyze() for target workbook.
        """

        self.source_profile = source_profile
        self.target_profile = target_profile

    # --------------------------------------------------
    # Public Method
    # --------------------------------------------------

    def map_columns(self):
        """
        Compare standardized columns between
        source and target workbooks.
        """

        source_headers = self._standardize_workbook(self.source_profile)
        target_headers = self._standardize_workbook(self.target_profile)

        mappings = []

        for source_sheet, source_cols in source_headers.items():

            for target_sheet, target_cols in target_headers.items():

                for source_original, source_std in source_cols.items():

                    for target_original, target_std in target_cols.items():

                        if source_std == target_std:

                            mappings.append({

                                "source_sheet": source_sheet,
                                "source_column": source_original,

                                "target_sheet": target_sheet,
                                "target_column": target_original,

                                "standard_name": source_std

                            })

        return mappings

    # --------------------------------------------------
    # Workbook Standardization
    # --------------------------------------------------

    def _standardize_workbook(self, profile):
        """
        Standardize every worksheet in a workbook.
        """

        standardized = {}

        sheets = profile.get("sheets", [])

        for sheet in sheets:

            sheet_name = sheet["sheet_name"]

            standardized[sheet_name] = self._map_sheet(sheet)

        return standardized

    # --------------------------------------------------
    # Sheet Standardization
    # --------------------------------------------------

    def _map_sheet(self, sheet_info):
        """
        Standardize every column header
        inside one worksheet.
        """

        mapping = {}

        columns = sheet_info.get("columns", [])

        for column in columns:

            header = column["column_name"]

            if self._is_empty(header):
                continue

            mapping[header] = self._find_alias(header)

        return mapping

    # --------------------------------------------------
    # Alias Detection
    # --------------------------------------------------

    def _find_alias(self, header):
        """
        Return standardized alias if found.
        Otherwise return normalized header.
        """

        normalized = self._normalize(header)

        if normalized in self.ALIASES:
            return self.ALIASES[normalized]

        return normalized.replace(" ", "_")

    # --------------------------------------------------
    # Header Normalization
    # --------------------------------------------------

    def _normalize(self, text):
        """
        Normalize header text.

        Example
        -------
        Employee-ID
        Employee_ID
        employee id

        →

        employee id
        """

        if text is None:
            return ""

        text = str(text).strip().lower()

        text = text.replace("_", " ")
        text = text.replace("-", " ")

        text = re.sub(r"\s+", " ", text)

        return text

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------

    def _is_empty(self, value):
        """
        Check whether a header is empty.
        """

        if value is None:
            return True

        if str(value).strip() == "":
            return True

        return False

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self, mappings):
        """
        Generate mapping summary.
        """

        return {

            "total_mappings": len(mappings),

            "mapped_columns": sorted(
                {
                    mapping["standard_name"]
                    for mapping in mappings
                }
            )

        }