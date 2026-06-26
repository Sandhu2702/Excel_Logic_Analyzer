"""
logic_detector.py

Detects formula cells in an Excel workbook.

This module does NOT analyze formulas.
It only identifies cells that contain logic (formulas).
"""

from openpyxl.cell.cell import Cell


class LogicDetector:
    """
    Detects formula cells in every worksheet.
    """

    def __init__(self, workbook_data):
        """
        Parameters
        ----------
        workbook_data : WorkbookData
            Output from ExcelReader.read()
        """
        self.workbook = workbook_data.workbook

    def detect(self):
        """
        Detect all formula cells in the workbook.

        Returns
        -------
        dict
            Dictionary containing all detected formula cells
            grouped by worksheet.
        """

        detected_logic = {}

        for worksheet in self.workbook.worksheets:
            detected_logic[worksheet.title] = self._detect_sheet(worksheet)

        return detected_logic

    def _detect_sheet(self, worksheet):
        """
        Detect all formula cells in a worksheet.
        """

        formula_cells = []

        for row in worksheet.iter_rows():

            for cell in row:

                cell_type = self._classify_cell(cell)

                if cell_type == "formula":

                    formula_cells.append(
                        {
                            "sheet": worksheet.title,
                            "cell": cell.coordinate,
                            "row": cell.row,
                            "column": cell.column,
                            "type": cell_type,
                            "formula": cell.value
                        }
                    )

        return formula_cells

    def _classify_cell(self, cell: Cell):
        """
        Classify the type of a cell.

        Returns
        -------
        str
            formula | number | text | empty
        """

        if self._is_formula(cell):
            return "formula"

        if self._is_empty(cell):
            return "empty"

        if self._is_number(cell):
            return "number"

        return "text"

    def _is_formula(self, cell: Cell):
        """
        Check whether a cell contains a formula.
        """

        return cell.data_type == "f"

    def _is_number(self, cell: Cell):
        """
        Check whether a cell contains a numeric value.
        """

        return isinstance(cell.value, (int, float))

    def _is_empty(self, cell: Cell):
        """
        Check whether a cell is empty.
        """

        return cell.value is None