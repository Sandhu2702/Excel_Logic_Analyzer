from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

import pandas as pd

# Workbook Data Model----------------------->

@dataclass
class WorkbookData:
    """
    Stores all information related to an Excel workbook.
    """

    file_path: str
    file_name: str
    sheet_count: int
    sheet_names: list[str]

    # Dictionary:------------------------->
    # Key   -> Sheet Name
    # Value -> DataFrame
    sheets: Dict[str, pd.DataFrame] = field(default_factory=dict)

    # Dictionary containing metadata of each sheet
    metadata: Dict[str, dict] = field(default_factory=dict)

# Excel Reader-------------------------------------->

class ExcelReader:
    """
    Reads an Excel workbook and extracts all worksheet data.
    """

    SUPPORTED_EXTENSIONS = (".xlsx", ".xls")

    # Validate Excel File--------------------------->

    def validate_file(self, file_path: str) -> None:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found:\n{file_path}")

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                "Only .xlsx and .xls files are supported."
            )

    # Extract Metadata-------------------------------->

    def extract_metadata(
        self,
        dataframe: pd.DataFrame
    ) -> dict:

        return {

            "rows": len(dataframe),

            "columns": len(dataframe.columns),

            "column_names": dataframe.columns.tolist(),

            "data_types": dataframe.dtypes.astype(str).to_dict(),

            "missing_values": dataframe.isnull().sum().to_dict(),

            "duplicate_rows": int(dataframe.duplicated().sum())

        }

    # Read Workbook----------------------------------------->
    
    def read(self, file_path: str) -> WorkbookData:

        self.validate_file(file_path)

        excel_file = pd.ExcelFile(file_path)

        sheets = {}
        metadata = {}

        for sheet in excel_file.sheet_names:

            df = pd.read_excel(
                file_path,
                sheet_name=sheet
            )

            sheets[sheet] = df

            metadata[sheet] = self.extract_metadata(df)

        return WorkbookData(

            file_path=file_path,

            file_name=Path(file_path).name,

            sheet_count=len(excel_file.sheet_names),

            sheet_names=excel_file.sheet_names,

            sheets=sheets,

            metadata=metadata

        )