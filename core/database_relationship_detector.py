"""
database_relationship_detector.py

Detects database relationships for generated applications.

Version 1:
------------
- Primary Key Detection
- Foreign Key Detection
- One-to-Many Relationship Detection
"""

from collections import Counter


class DatabaseRelationshipDetector:
    """
    Detect primary keys and relationships
    between generated tables.
    """

    PK_KEYWORDS = [
        "id",
        "_id",
        "code",
        "_code"
    ]

    def __init__(self, tables_data: dict):
        """
        Parameters
        ----------
        tables_data : dict

        Example
        -------
        {
            "employee_master": dataframe,
            "payroll_data": dataframe
        }
        """

        self.tables_data = tables_data

    # --------------------------------------------------
    # Public Methods
    # --------------------------------------------------

    def detect_primary_keys(self):
        """
        Detect likely primary key for each table.

        Returns
        -------
        dict

        Example
        -------
        {
            "employee_master": "emp_id",
            "payroll_data": "payroll_id"
        }
        """

        primary_keys = {}

        for table_name, df in self.tables_data.items():

            best_column = None
            best_score = -1

            for column in df.columns:

                score = self._score_column(df, column)

                if score > best_score:
                    best_score = score
                    best_column = column

            primary_keys[table_name] = best_column

        return primary_keys
    
    def detect_foreign_keys(self):
        """
        Detect possible foreign key relationships.

        Returns
        -------
        list

        Example
        -------
        [
           {
              "parent_table": "employee_master",
              "parent_key": "emp_id",

              "child_table": "payroll_data",
              "child_key": "emp_id",

              "relationship_type": "one_to_many"
           }
        ]
        """

        relationships = []

        primary_keys = self.detect_primary_keys()

        for parent_table, parent_pk in primary_keys.items():

            parent_df = self.tables_data[parent_table]

            if parent_pk not in parent_df.columns:
               continue

            parent_values = set(
                parent_df[parent_pk]
                .dropna()
                .astype(str)
            ) 

            for child_table, child_df in self.tables_data.items():

               # Skip same table
               if child_table == parent_table:
                  continue

               # Check every column in child table
               for child_column in child_df.columns:

                   # Ignore child's own primary key
                   if child_column == primary_keys.get(child_table):
                      continue

                   # Column names must match initially
                   if child_column.lower() != parent_pk.lower():
                      continue

                   child_values = set(
                      child_df[child_column]
                      .dropna()
                      .astype(str)
                   )

                   # Empty column
                   if not child_values:
                      continue

                   # FK validation:
                   # child values should exist in parent values
                   if child_values.issubset(parent_values):

                      relationships.append({
                          "parent_table": parent_table,
                          "parent_key": parent_pk,

                          "child_table": child_table,
                          "child_key": child_column,

                          "relationship_type": "one_to_many"
                      })

        return relationships

    # --------------------------------------------------
    # Internal Methods
    # --------------------------------------------------

    def _score_column(self, df, column):
        """
        Score a column for primary key suitability.
        """

        score = 0

        column_lower = str(column).lower()

        # ----------------------------------
        # Naming Convention Score
        # ----------------------------------

        if column_lower == "id":
            score += 50

        elif column_lower.endswith("_id"):
            score += 45

        elif "id" in column_lower:
            score += 40

        elif column_lower.endswith("_code"):
            score += 35

        elif "code" in column_lower:
            score += 30

        # ----------------------------------
        # Uniqueness Score
        # ----------------------------------

        series = df[column]

        total_rows = len(series)

        if total_rows > 0:

            unique_count = series.nunique(dropna=True)

            uniqueness_ratio = unique_count / total_rows

            score += int(uniqueness_ratio * 30)

        # ----------------------------------
        # Null Score
        # ----------------------------------

        null_count = series.isna().sum()

        if null_count == 0:
            score += 20

        # ----------------------------------
        # First Column Bonus
        # ----------------------------------

        if column == df.columns[0]:
            score += 10

        return score

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self):
        """
        Generate detector summary.
        """

        primary_keys = self.detect_primary_keys()
        foreign_keys = self.detect_foreign_keys()

        return {
            "tables_analyzed": len(self.tables_data),
            "primary_keys_detected": primary_keys,
            "relationships_detected": len(foreign_keys),
            "relationships": foreign_keys
        }