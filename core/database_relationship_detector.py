"""
database_relationship_detector.py

Detects database relationships for generated applications.

Version 1:
------------
- Primary Key Detection
- Foreign Key Detection
- One-to-Many Relationship Detection
"""


class DatabaseRelationshipDetector:
    """
    Detect primary keys and relationships
    between generated tables.
    """

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
    # Primary Key Detection
    # --------------------------------------------------

    def detect_primary_keys(self):

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

    # --------------------------------------------------
    # Foreign Key Detection
    # --------------------------------------------------

    def detect_foreign_keys(self):

        relationships = []
        seen_relationships = set()

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

                if child_table == parent_table:
                    continue

                for child_column in child_df.columns:

                    if child_column.lower() != parent_pk.lower():
                        continue

                    child_values = set(
                        child_df[child_column]
                        .dropna()
                        .astype(str)
                    )

                    if not child_values:
                        continue

                    if not child_values.issubset(parent_values):
                        continue

                    relationship_key = tuple(
                        sorted([parent_table, child_table])
                    )

                    if relationship_key in seen_relationships:
                        continue

                    seen_relationships.add(
                        relationship_key
                    )

                    relationships.append({
                        "parent_table": parent_table,
                        "parent_key": parent_pk,
                        "child_table": child_table,
                        "child_key": child_column,
                        "relationship_type": "one_to_many"
                    })

        return relationships

    # --------------------------------------------------
    # Column Scoring
    # --------------------------------------------------

    def _score_column(self, df, column):

        score = 0

        column_lower = str(column).lower()

        # Naming convention

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

        # Uniqueness

        series = df[column]

        total_rows = len(series)

        if total_rows > 0:

            unique_count = series.nunique(
                dropna=True
            )

            uniqueness_ratio = (
                unique_count / total_rows
            )

            score += int(
                uniqueness_ratio * 30
            )

        # No NULLs

        if series.isna().sum() == 0:
            score += 20

        # First column bonus

        if column == df.columns[0]:
            score += 10

        return score

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self):

        primary_keys = (
            self.detect_primary_keys()
        )

        relationships = (
            self.detect_foreign_keys()
        )

        return {
            "tables_analyzed": len(
                self.tables_data
            ),
            "primary_keys_detected":
                primary_keys,
            "relationships_detected":
                len(relationships),
            "relationships":
                relationships
        }