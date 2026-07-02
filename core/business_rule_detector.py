class BusinessRuleDetector:

    def __init__(self, source_df, target_df):

        self.source_df = source_df
        self.target_df = target_df

    def detect_rules(self):

        rules = []

        columns = [
            str(col).lower().strip()
            for col in self.target_df.columns
        ]

        # ==================================
        # Bonus Amount Rule
        # ==================================

        if (
            "salary" in columns
            and "bonus %" in columns
            and "bonus amount" in columns
        ):

            rules.append({
                "type": "calculation",
                "target_field": "bonus_amount",
                "source_fields": [
                    "salary",
                    "bonus_percent"
                ],
                "formula":
                    "salary * bonus_percent / 100"
            })

        # ==================================
        # Net Salary Rule
        # ==================================

        if (
            "salary" in columns
            and "bonus amount" in columns
            and "tax" in columns
            and "net salary" in columns
        ):

            rules.append({
                "type": "calculation",
                "target_field": "net_salary",
                "source_fields": [
                    "salary",
                    "bonus_amount",
                    "tax"
                ],
                "formula":
                    "salary + bonus_amount - tax"
            })

        return rules