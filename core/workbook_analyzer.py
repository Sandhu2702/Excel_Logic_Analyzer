"""
workbook_analyzer.py

Analyzes the structural characteristics of a workbook.

This module does NOT detect business logic.
Its responsibility is only to profile workbook structure.
"""

from core.excel_reader import WorkbookData


class WorkbookAnalyzer:
    """
    Performs structural analysis of an Excel workbook.

    Responsibilities
    ----------------
    - Analyze worksheets
    - Analyze columns
    - Build workbook summary

    This class does NOT detect:
    - Formulas
    - Lookups
    - Relationships
    - Conditions
    """

    def __init__(self, workbook_data: WorkbookData):
        """
        Initialize analyzer.

        Parameters
        ----------
        workbook_data : WorkbookData
            Workbook returned by ExcelReader.
        """
        self.workbook_data = workbook_data

    # --------------------------------------------------
    # Public Method
    # --------------------------------------------------

    def analyze(self) -> dict:
        """
        Analyze the workbook structure.

        Returns
        -------
        dict
            Structural information about the workbook.
        """

        workbook_analysis = {
            "file_name": self.workbook_data.file_name,
            "file_path": self.workbook_data.file_path,
            "sheet_count": self.workbook_data.sheet_count,
            "sheet_names": self.workbook_data.sheet_names,
            "sheets": []
        }

        # Analyze every worksheet
        for sheet_name, dataframe in self.workbook_data.sheets.items():

            sheet_result = self._analyze_sheet(
                sheet_name,
                dataframe
            )

            workbook_analysis["sheets"].append(sheet_result)

        return workbook_analysis

    # --------------------------------------------------
    # Analyze One Worksheet
    # --------------------------------------------------

    def _analyze_sheet(self, sheet_name, dataframe):
        """
        Analyze a single worksheet.
        Parameters
        ----------
        sheet_name : str
        Name of the worksheet.

        dataframe : pandas.DataFrame
        Worksheet data.

        Returns
        -------
        dict
          Structural information about the worksheet.
        """

        sheet_analysis = {
            "sheet_name": sheet_name,
            "row_count": len(dataframe),
            "column_count": len(dataframe.columns),
            "columns": []
        }

    # Analyze every column
        for column_name in dataframe.columns:

            column_result = self._analyze_column(
                column_name,
                dataframe[column_name]
            )

            sheet_analysis["columns"].append(column_result)

        return sheet_analysis
    # --------------------------------------------------
    # Analyze One Column
    # --------------------------------------------------

    def _analyze_column(self, column_name, column):
        """
        Analyze a single column.

        Parameters
        ----------
        column_name : str
            Name of the column.

        column : pandas.Series
            Column data.

        Returns
        -------
        dict
            Structural information about the column.
        """

        row_count = len(column)

        non_null_count = int(column.count())

        null_count = int(column.isna().sum())

        unique_count = int(column.nunique(dropna=True))

        duplicate_count = int(column.duplicated().sum())

        sample_values = (
            column.dropna()
                  .head(5)
                  .tolist()
        )

        return {

            "column_name": column_name,

            "data_type": str(column.dtype),

            "row_count": row_count,

            "non_null_count": non_null_count,

            "null_count": null_count,

            "unique_count": unique_count,

            "duplicate_count": duplicate_count,

            "sample_values": sample_values

         }