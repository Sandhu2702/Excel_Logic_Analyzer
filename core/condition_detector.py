"""
condition_detector.py

Detects business conditions used in Excel formulas.

This module uses FormulaDetector output to identify
conditions such as:

- IF
- IFS
- AND
- OR

It extracts comparison conditions but does NOT
evaluate them or calculate confidence scores.
"""
import re

class ConditionDetector:
    """
    Detects logical conditions from Excel formulas.
    """
    OPERATORS = [
          ">=",
          "<=",
          "<>",
          ">",
          "<",
          "=",
        ]

    def __init__(self, formula_data):
        """
        Initialize detector.

        Parameters
        ----------
        formula_data : list
        Output from FormulaDetector.
        """

        self.formula_data = formula_data
        self.conditions = []

    def _extract_operator(self, condition):
        """
        Return the comparison operator used
        in a condition.
        """

        for operator in self.OPERATORS:
            if operator in condition:
                return operator

        return None
    
    def _split_conditions(self, text):
        """
        Split multiple conditions separated
        by commas.
        """

        conditions = []

        for part in text.split(","):

            part = part.strip()

            if part:
                conditions.append(part)

        return conditions
    
    def _extract_if(self, formula):
       """
       Extract the first condition from an IF formula.

       Example:
          =IF(C2>=90,"Excellent","Average")

       Returns:
        C2>=90
       """

       match = re.search(r"IF\s*\(([^,]+)", formula, re.IGNORECASE)

       if match:
          return match.group(1).strip()

       return None
    
    def _extract_and(self, formula):
       """
       Extract conditions inside an AND() function.

       Example:
          =IF(AND(C2>=90,D2="Yes"),100,0)

       Returns:
             ["C2>=90", 'D2="Yes"']
       """

       match = re.search(r"AND\s*\((.*?)\)", formula, re.IGNORECASE)

       if not match:
           return []

       return self._split_conditions(match.group(1))
    
    def _extract_or(self, formula):
       """
       Extract conditions inside an OR() function.

       Example:
          =IF(OR(C2>=90,D2="Yes"),100,0)

       Returns:
          ["C2>=90", 'D2="Yes"']
       """

       match = re.search(r"OR\s*\((.*?)\)", formula, re.IGNORECASE)

       if not match:
           return []

       return self._split_conditions(match.group(1))
    
    def _extract_ifs(self, formula):
       """
       Extract all comparison conditions from an IFS() formula.

       Example:
          =IFS(A2>90,"A",A2>80,"B",TRUE,"C")

       Returns:
          ["A2>90", "A2>80"]
       """

       match = re.search(r"IFS\s*\((.*)\)", formula, re.IGNORECASE)

       if not match:
          return []

       parts = [part.strip() for part in match.group(1).split(",")]

       conditions = []

       # Conditions are at even indexes (0, 2, 4, ...)
       for i in range(0, len(parts), 2):
          condition = parts[i]

          if condition.upper() != "TRUE":
              conditions.append(condition)

       return conditions
    
    def detect(self):
       """
       Detect business conditions from FormulaDetector output.

       Returns
       -------
       list
          List of detected conditions.
       """

       self.conditions = []

       # Loop through each sheet
       for sheet_name, formulas in self.formula_data.items():

         for item in formulas:

            formula = item.get("formula", "")
            category = item.get("category", "")

            extracted_conditions = []

            if formula.upper().startswith("=IFS"):
                extracted_conditions = self._extract_ifs(formula)

            elif "AND(" in formula.upper():
                extracted_conditions = self._extract_and(formula)

            elif "OR(" in formula.upper():
                extracted_conditions = self._extract_or(formula)

            elif formula.upper().startswith("=IF"):
                condition = self._extract_if(formula)

                if condition:
                    extracted_conditions = [condition]

            for condition in extracted_conditions:

                self.conditions.append(
                    {
                        "sheet": sheet_name,
                        "cell": item.get("cell"),
                        "formula": formula,
                        "formula_type": category,
                        "condition": condition,
                        "operator": self._extract_operator(condition),
                    }
                )

       return self.conditions

    def summary(self):
        """
        Return a summary of detected conditions.
        """

        summary = {
           "total_conditions": len(self.conditions),
           "greater_than": 0,
           "less_than": 0,
           "greater_equal": 0,
           "less_equal": 0,
           "equal": 0,
           "not_equal": 0,
        }

        for item in self.conditions:

           operator = item.get("operator")

           if operator == ">":
              summary["greater_than"] += 1

           elif operator == "<":
              summary["less_than"] += 1

           elif operator == ">=":
              summary["greater_equal"] += 1
 
           elif operator == "<=":
              summary["less_equal"] += 1

           elif operator == "=":
              summary["equal"] += 1

           elif operator == "<>":
              summary["not_equal"] += 1

        return summary