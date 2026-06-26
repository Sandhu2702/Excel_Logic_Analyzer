"""
lookup_detector.py

Detects lookup formulas from FormulaDetector output.

This module does NOT scan the workbook again.
It only extracts lookup-related formulas.
"""


class LookupDetector:
    """
    Detects lookup formulas from analyzed formulas.
    """

    LOOKUP_FUNCTIONS = {
        "VLOOKUP",
        "HLOOKUP",
        "XLOOKUP",
        "LOOKUP",
        "INDEX",
        "MATCH"
    }

    def __init__(self, analyzed_formulas):
        """
        Parameters
        ----------
        analyzed_formulas : dict
            Output of FormulaDetector.detect()
        """
        self.analyzed_formulas = analyzed_formulas

    def detect(self):
        """
        Extract lookup formulas.

        Returns
        -------
        dict
        """

        lookup_data = {}

        for sheet_name, formulas in self.analyzed_formulas.items():

            sheet_lookup = []

            for formula in formulas:

                function = formula.get("function")

                if function in self.LOOKUP_FUNCTIONS:

                    lookup_info = formula.copy()

                    # Detect INDEX + MATCH combination
                    if function == "INDEX":
                        if "MATCH(" in formula["formula"].upper():
                            lookup_info["lookup_type"] = "INDEX_MATCH"
                        else:
                            lookup_info["lookup_type"] = "INDEX"

                    elif function == "MATCH":
                        # Skip standalone MATCH if already part of INDEX_MATCH
                        if "INDEX(" in formula["formula"].upper():
                            continue
                        lookup_info["lookup_type"] = "MATCH"

                    else:
                        lookup_info["lookup_type"] = function

                    sheet_lookup.append(lookup_info)

            lookup_data[sheet_name] = sheet_lookup

        return lookup_data

    def summary(self, lookup_data):
        """
        Generate lookup summary.

        Parameters
        ----------
        lookup_data : dict

        Returns
        -------
        dict
        """

        summary = {
            "total_lookup_formulas": 0,
            "lookup_types": {}
        }

        for formulas in lookup_data.values():

            for formula in formulas:

                lookup = formula["lookup_type"]

                summary["total_lookup_formulas"] += 1

                summary["lookup_types"][lookup] = (
                    summary["lookup_types"].get(lookup, 0) + 1
                )

        return summary