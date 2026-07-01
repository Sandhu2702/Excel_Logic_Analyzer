import customtkinter as ctk

class Dashboard(ctk.CTkToplevel):

    def __init__(self, parent, report):
        super().__init__(parent)

        self.title("Business Application Generator")
        self.geometry("1100x700")

        self.report = report

        title = ctk.CTkLabel(
            self,
            text="Excel to Business Application Generator",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.tabs.add("Entities")
        self.tabs.add("Relationships")
        self.tabs.add("Generated Application")

        self.create_entities_tab()
        self.create_relationships_tab()
        self.create_application_tab()

    # ==================================================
    # ENTITIES TAB
    # ==================================================

    def create_entities_tab(self):

        tab = self.tabs.tab("Entities")

        textbox = ctk.CTkTextbox(tab)
        textbox.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

        text = ""

        text += "SOURCE ENTITY\n"
        text += "-" * 40 + "\n\n"

        for col in self.report["source_columns"]:
            text += f"• {col}\n"

        text += "\n\n"

        text += "TARGET ENTITY\n"
        text += "-" * 40 + "\n\n"

        for col in self.report["target_columns"]:
            text += f"• {col}\n"

        textbox.insert("1.0", text)
        textbox.configure(state="disabled")

    # ==================================================
    # RELATIONSHIPS TAB
    # ==================================================

    def create_relationships_tab(self):

        tab = self.tabs.tab("Relationships")

        textbox = ctk.CTkTextbox(tab)
        textbox.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

        text = "DETECTED RELATIONSHIPS\n"
        text += "-" * 40 + "\n\n"

        if self.report["relationships"]:

           for rel in self.report["relationships"]:

               text += (
                  f"Parent Table : "
                  f"{rel['parent_table']}\n"
               )

               text += (
                  f"Parent Key   : "
                  f"{rel['parent_key']}\n\n"
               )

               text += (
                  f"Child Table  : "
                  f"{rel['child_table']}\n"
               )

               text += (
                  f"Child Key    : "
                  f"{rel['child_key']}\n\n"
               )

               relationship_name = (
                   rel["relationship_type"]
                   .replace("_", "-")
                   .title()
               )

               text += (
                  f"Relationship : "
                  f"{relationship_name}\n"
               )

               text += (
                 "\n----------------------------------\n\n"
               )

        else:

            text += "No relationships detected."

        textbox.insert("1.0", text)
        textbox.configure(state="disabled")

    # ==================================================
    # GENERATED APPLICATION TAB
    # ==================================================

    def create_application_tab(self):

        tab = self.tabs.tab("Generated Application")

        textbox = ctk.CTkTextbox(tab)

        textbox.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

        text = ""

        text += "APPLICATION DESIGN REPORT\n"
        text += "=" * 50 + "\n\n"

        # ----------------------------------------------
        # Entities
        # ----------------------------------------------

        text += "BUSINESS ENTITIES DETECTED\n"
        text += "-" * 30 + "\n"

        text += f"Source Entity ({len(self.report['source_columns'])} fields)\n"

        for col in self.report["source_columns"]:
            text += f"   • {col}\n"

        text += "\n"

        text += f"Target Entity ({len(self.report['target_columns'])} fields)\n"

        for col in self.report["target_columns"]:
            text += f"   • {col}\n"

        text += "\n\n"

        # ----------------------------------------------
        # Relationships
        # ----------------------------------------------

        text += "RELATIONSHIPS DETECTED\n"
        text += "-" * 30 + "\n"

        if self.report["relationships"]:

           for rel in self.report["relationships"]:

              text += (
                 f"   • {rel['parent_table']}."
                 f"{rel['parent_key']}"
                 f" → "
                 f"{rel['child_table']}."
                 f"{rel['child_key']}\n"
              )

        else:

            text += "   • No common relationship detected\n"

        text += "\n\n"

        # ----------------------------------------------
        # Application Type
        # ----------------------------------------------

        text += "SUGGESTED APPLICATION TYPE\n"
        text += "-" * 30 + "\n"

        text += f"   • {self.report['application_type']}\n"

        text += "\n\n"

        # ----------------------------------------------
        # Business Rules
        # ----------------------------------------------

        text += "BUSINESS RULES DETECTED\n"
        text += "-" * 30 + "\n"

        if self.report["business_rules"]:

            for rule in self.report["business_rules"]:
                text += f"   • {rule}\n"

        else:

            text += "   • No business rules detected\n"

        text += "\n\n"

        # ----------------------------------------------
        # Modules
        # ----------------------------------------------

        text += "SUGGESTED APPLICATION MODULES\n"
        text += "-" * 30 + "\n"

        for index, module in enumerate(
            self.report["modules"],
            start=1
        ):
            text += f"{index}. {module}\n"

        text += "\n\n"

        # ----------------------------------------------
        # Database Tables
        # ----------------------------------------------

        text += "SUGGESTED DATABASE TABLES\n"
        text += "-" * 30 + "\n"

        text += f"{self.report['source_table']}\n"

        for col in self.report["source_columns"]:
            text += f"   • {col}\n"

        text += "\n"

        text += f"{self.report['target_table']}\n"

        for col in self.report["target_columns"]:
            text += f"   • {col}\n"

        text += "\n\n"

        # ----------------------------------------------
        # Relationship Model
        # ----------------------------------------------

        text += "DATA RELATIONSHIP MODEL\n"
        text += "-" * 30 + "\n"

        if self.report["relationships"]:

            relation = self.report["relationships"][0]

            text += (
              f"{relation['parent_table']}"
              f" ({relation['parent_key']})\n"
            )

            text += "           |\n"
            text += "           |\n"

            relationship_name = (
               relation["relationship_type"]
               .replace("_", "-")
               .title()
            )

            text += (
              f"           | "
              f"{relationship_name}\n"
            )

            text += "           |\n"
            text += "           V\n"

            text += (
               f"{relation['child_table']}"
               f" ({relation['child_key']})\n"
            )

        text += "\n\n"

        # ----------------------------------------------
        # Suggested Screens
        # ----------------------------------------------

        text += "SUGGESTED WEB APPLICATION SCREENS\n"
        text += "-" * 30 + "\n"

        for module in self.report["modules"]:

            if "Management" in module:

                screen_name = module.replace(
                    "Management",
                    "Dashboard"
                )

                text += f"• {screen_name}\n"

        text += "• Reports Dashboard\n"
        text += "• Search Screen\n"

        text += "\n\n"

        # ----------------------------------------------
        # Recommendation
        # ----------------------------------------------

        text += "SYSTEM RECOMMENDATION\n"
        text += "-" * 30 + "\n"

        text += (
            f"The uploaded Excel files represent a "
            f"{self.report['application_type']}. "
            f"The detected entities, business rules and "
            f"relationships can be transformed into a "
            f"web-based application with dedicated modules, "
            f"database tables and reporting capabilities."
        )

        textbox.insert("1.0", text)
        textbox.configure(state="disabled")