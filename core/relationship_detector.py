"""
relationship_detector.py

Detects possible relationships between source and target
workbooks using column mappings and lookup formulas.

This module does NOT calculate confidence scores.
It only identifies possible relationships.
"""


class RelationshipDetector:
    """
    Detect possible relationships between
    source and target workbooks.
    """

    def __init__(
        self,
        source_profile: dict,
        target_profile: dict,
        column_mappings: list,
        lookup_data: dict,
    ):
        """
        Parameters
        ----------
        source_profile : dict
            Output from WorkbookAnalyzer.analyze()

        target_profile : dict
            Output from WorkbookAnalyzer.analyze()

        column_mappings : list
            Output from ColumnMapper.map_columns()

        lookup_data : dict
            Output from LookupDetector.detect()
        """

        self.source_profile = source_profile
        self.target_profile = target_profile
        self.column_mappings = column_mappings
        self.lookup_data = lookup_data

    # --------------------------------------------------
    # Public Method
    # --------------------------------------------------

    def detect(self):
        """
        Detect possible relationships.

        Returns
        -------
        dict
        """

        relationships = []

        # ------------------------------------------
        # Relationships from mapped columns
        # ------------------------------------------

        for mapping in self.column_mappings:

            relationships.append({

                "source_sheet": mapping["source_sheet"],

                "source_column": mapping["source_column"],

                "target_sheet": mapping["target_sheet"],

                "target_column": mapping["target_column"],

                "relationship": "column_mapping",

                "reason": "Standardized column names match"

            })

        # ------------------------------------------
        # Relationships from lookup formulas
        # ------------------------------------------

        for sheet_name, formulas in self.lookup_data.items():

            for formula in formulas:

                relationships.append({

                    "source_sheet": "Unknown",

                    "source_column": "Unknown",

                    "target_sheet": sheet_name,

                    "target_column": formula["cell"],

                    "relationship": formula["lookup_type"],

                    "reason": f'{formula["lookup_type"]} formula detected'

                })

        return {

            "relationships": relationships

        }

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self, relationship_data):
        """
        Generate relationship summary.
        """

        summary = {

            "total_relationships": 0,

            "relationship_types": {}

        }

        for relation in relationship_data["relationships"]:

            relation_type = relation["relationship"]

            summary["total_relationships"] += 1

            summary["relationship_types"][relation_type] = (

                summary["relationship_types"].get(

                    relation_type,

                    0

                ) + 1

            )

        return summary