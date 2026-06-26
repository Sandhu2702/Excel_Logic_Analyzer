"""
formula_detector.py

Analyzes Excel formulas and classifies them into categories.

This module does NOT explain business logic.
It only classifies formulas.
"""

import re


class FormulaDetector:
    """
    Classifies formulas detected by LogicDetector.
    """

    FUNCTION_CATEGORIES = {

        # Aggregate
        "SUM": "aggregate",
        "AVERAGE": "aggregate",
        "COUNT": "aggregate",
        "COUNTA": "aggregate",
        "MAX": "aggregate",
        "MIN": "aggregate",

        # Conditional
        "IF": "conditional",
        "IFS": "conditional",
        "SWITCH": "conditional",

        # Lookup
        "VLOOKUP": "lookup",
        "HLOOKUP": "lookup",
        "XLOOKUP": "lookup",
        "INDEX": "lookup",
        "MATCH": "lookup",

        # Logical
        "AND": "logical",
        "OR": "logical",
        "NOT": "logical",

        # Text
        "LEFT": "text",
        "RIGHT": "text",
        "MID": "text",
        "CONCAT": "text",
        "TEXTJOIN": "text",

        # Date
        "TODAY": "date",
        "NOW": "date",
        "YEAR": "date",
        "MONTH": "date",
        "DAY": "date",
    }

    ARITHMETIC_OPERATORS = ["+", "-", "*", "/", "^"]

    def __init__(self, detected_logic):
        """
        Parameters
        ----------
        detected_logic : dict
            Output from LogicDetector.detect()
        """
        self.detected_logic = detected_logic

    def detect(self):
        """
        Analyze all detected formulas.

        Returns
        -------
        dict
        """

        analyzed = {}

        for sheet_name, formulas in self.detected_logic.items():
            analyzed[sheet_name] = self._detect_sheet(formulas)

        return analyzed

    def _detect_sheet(self, formulas):

        analyzed_formulas = []

        for formula_info in formulas:

            formula = formula_info["formula"]

            function = self._extract_function(formula)

            category = self._classify_formula(formula, function)

            new_formula = formula_info.copy()

            new_formula["function"] = function

            new_formula["category"] = category

            analyzed_formulas.append(new_formula)

        return analyzed_formulas


    def _extract_function(self, formula):
        """
        Extract Excel function name.

        Examples
        --------
        =SUM(A1:A5)  -> SUM
        =IF(A1>10...) -> IF
        =A1+B1       -> None
        """

        match = re.match(r"=\s*([A-Za-z][A-Za-z0-9_]*)\(", formula)

        if match:
           return match.group(1).upper()

        return None

    def _classify_formula(self, formula, function):
        """
        Determine formula category.
        """

        if function:

            if function in self.FUNCTION_CATEGORIES:
                return self.FUNCTION_CATEGORIES[function]

            return "other"

        for operator in self.ARITHMETIC_OPERATORS:

            if operator in formula:
                return "arithmetic"

        return "other"