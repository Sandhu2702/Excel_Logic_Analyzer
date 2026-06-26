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

    def __init__(self, workbook_profile):
        """
        Parameters
        ----------
        workbook_profile : dict
            Output produced by WorkbookAnalyzer.analyze()
        """
        self.profile = workbook_profile

    def map_columns(self):
        """
        Standardize column names for every worksheet.

        Returns
        -------
        dict
        """

        mapped_workbook = {}

        sheets = self.profile.get("worksheets", {})

        for sheet_name, sheet_info in sheets.items():
            mapped_workbook[sheet_name] = self._map_sheet(sheet_info)

        return mapped_workbook

    def _map_sheet(self, sheet_info):
        """
        Map every header in a worksheet.
        """

        mapping = {}

        headers = sheet_info.get("headers", [])

        for header in headers:

            if self._is_empty(header):
                continue

            standardized = self._find_alias(header)

            mapping[header] = standardized

        return mapping

    def _find_alias(self, header):
        """
        Return standardized name if alias exists.
        Otherwise return normalized header.
        """

        normalized = self._normalize(header)

        if normalized in self.ALIASES:
            return self.ALIASES[normalized]

        return normalized.replace(" ", "_")

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

    def _is_empty(self, value):
        """
        Check whether a header is empty.
        """

        if value is None:
            return True

        if str(value).strip() == "":
            return True

        return False