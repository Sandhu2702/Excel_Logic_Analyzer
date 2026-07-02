import os

def get_sqlite_type(dtype):

    dtype = str(dtype).lower()

    if "int" in dtype:
        return "INTEGER"

    elif "float" in dtype:
        return "REAL"

    else:
        return "TEXT"

def build_foreign_key_metadata(report):

    foreign_keys = {}

    relationships = report.get(
        "relationships",
        []
    )

    for rel in relationships:

        if rel.get("relationship_type") != "one_to_many":
            continue

        child_table = rel["child_table"]
        child_column = rel["child_key"]

        foreign_keys.setdefault(
            child_table,
            {}
        )

        foreign_keys[child_table][child_column] = {
            "parent_table": rel["parent_table"],
            "parent_column": rel["parent_key"],
            "context_name":
                f"{rel['parent_table']}_options"
        }

    return foreign_keys

def generate_database_schema(report, output_dir):

    schema_sql = ""

    relationships = report.get(
        "relationships",
        []
    )

    for table in report["tables"]:

        table_name = table["table_name"]

        if table_name == report["source_table"]:
            column_types = report["source_column_types"]
        else:
            column_types = report["target_column_types"]

        schema_sql += f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
"""

        for column in table["columns"]:

            sql_name = (
                column.lower()
                .replace(" ", "_")
                .replace("%", "percent")
                .replace("(", "")
                .replace(")", "")
            )

            sqlite_type = get_sqlite_type(
                column_types[column]
            )

            schema_sql += (
                f"    {sql_name} {sqlite_type},\n"
            )
        
        for relation in relationships:

            if relation["child_table"] != table_name:
               continue

            fk_column = (
               relation["child_key"]
               .lower()
               .replace(" ", "_")
               .replace("%", "percent")
               .replace("(", "")
               .replace(")", "")
            )

            parent_table = relation["parent_table"]

            parent_key = (
               relation["parent_key"]
               .lower()
               .replace(" ", "_")
               .replace("%", "percent")
               .replace("(", "")
               .replace(")", "")
            )

            schema_sql += (
               f"    FOREIGN KEY ({fk_column}) "
               f"REFERENCES {parent_table}({parent_key}),\n"
            )

        schema_sql = schema_sql.rstrip(",\n")

        schema_sql += "\n);\n\n"

    with open(
        os.path.join(output_dir, "schema.sql"),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(schema_sql)

def generate_flask_app(report):

    output_dir = "generated_app"

    foreign_key_metadata = (
        build_foreign_key_metadata(report)
    )

    business_rule_metadata = report.get(
       "business_rule_metadata",
       []
    )

    calculated_fields = {}

    for rule in business_rule_metadata:

        if rule["type"] != "calculation":
           continue

        calculated_fields[
           rule["target_field"]
        ] = rule

    print("\nForeign Key Metadata")
    print(foreign_key_metadata)

    os.makedirs(output_dir, exist_ok=True)

    templates_dir = os.path.join(
        output_dir,
        "templates"
    )

    os.makedirs(
        templates_dir,
        exist_ok=True
    )

    generate_database_schema(
        report,
        output_dir
    )

    # =====================================
    # Dynamic Route Generation
    # =====================================

    routes = ""

    for table in report["tables"]:

        table_name = table["table_name"]

        column_names = []

        for column in table["columns"]:

            sql_name = (
               column.lower()
               .replace(" ", "_")
               .replace("%", "percent")
               .replace("(", "")
               .replace(")", "")
            )

            column_names.append(sql_name)

        table_columns = set(column_names)

        fk_fields = foreign_key_metadata.get(
            table_name,
            {}
        )

        parent_queries = ""

        template_context = ""

        variable_loading_code = ""

        loaded_fields = set()

        calculated_field_names = {
           rule["target_field"]
           for rule in business_rule_metadata
           if rule["type"] == "calculation"
        }

        for rule in business_rule_metadata:

            if rule["target_field"] not in table_columns:
                continue

            for field in rule["source_fields"]:

                if field in calculated_field_names:
                    continue

                if field in loaded_fields:
                    continue

                loaded_fields.add(field)

                variable_loading_code += (
    f'        {field} = float('
    f'request.form.get("{field}") or 0)\n'
)

        calculation_code = ""

        for rule in business_rule_metadata:

          if rule["target_field"] not in table_columns:
             continue

          if rule["type"] != "calculation":
             continue

          calculation_code += (
    f'        {rule["target_field"]} = '
    f'({rule["formula"]})\n'
)
           
        print("\n=== VARIABLE LOADING CODE ===")
        print(variable_loading_code)
        print("============================\n")

        print("\n=== GENERATED CALCULATION CODE ===")
        print(calculation_code)
        print("=================================\n")

        for fk_column, fk_info in fk_fields.items():

            parent_table = fk_info["parent_table"]

            parent_column = (
                fk_info["parent_column"]
                .lower()
                .replace(" ", "_")
                .replace("%", "percent")
                .replace("(", "")
                .replace(")", "")
            )

            context_name = fk_info["context_name"]

            parent_queries += f"""
    {context_name} = conn.execute(
        "SELECT {parent_column} FROM {parent_table}"
    ).fetchall()
"""

            template_context += f""",
        {context_name}={context_name}
"""

        columns_sql = ", ".join(column_names)

        placeholders = ", ".join(
           ["?"] * len(column_names)
        )

        form_values_list = []

        for col in column_names:

            if col in calculated_fields:
               form_values_list.append(col)

            else:
                form_values_list.append(
                    f'request.form.get("{col}")'
                )

        form_values = ", ".join(
           form_values_list
        )

        update_values = ", ".join(
            [
                f'request.form.get("{col}")'
                for col in column_names
            ]
        )

        update_sql = ", ".join(
           [f"{col}=?" for col in column_names]
        )

        update_params_list = []

        for col in column_names:

            if col in calculated_fields:
               update_params_list.append(col)

            else:
               update_params_list.append(
                  f'request.form.get("{col}")'
               )

        update_params = ", ".join(
            update_params_list
        )

        routes += f"""

@app.route("/{table_name}")
def {table_name}():

    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM {table_name}"
    ).fetchall()

    conn.close()

    return render_template(
        "{table_name}_list.html",
        rows=rows,
        columns={column_names}
    )


@app.route(
    "/{table_name}/add",
    methods=["GET", "POST"]
)
def add_{table_name}():

    if request.method == "POST":

        conn = get_connection()

{variable_loading_code}

{calculation_code} 

        conn.execute(
            \"\"\"
            INSERT INTO {table_name}
            ({columns_sql})
            VALUES ({placeholders})
            \"\"\",
            ({form_values},)
        )

        conn.commit()
        conn.close()

        return redirect(
            url_for("{table_name}")
        )

    conn = get_connection()

{parent_queries}

    conn.close()

    return render_template(
       "{table_name}_add.html"
       {template_context}
    )


@app.route(
    "/{table_name}/delete/<int:id>",
    methods=["POST"]
)
def delete_{table_name}(id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM {table_name} WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(
        url_for("{table_name}")
    )

@app.route(
    "/{table_name}/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_{table_name}(id):

    conn = get_connection()

    if request.method == "POST":
    
{variable_loading_code}

{calculation_code}

        conn.execute(
           \"\"\"
           UPDATE {table_name}
           SET {update_sql}
           WHERE id = ?
           \"\"\",
           ({update_params}, id)
        )

        conn.commit()
        conn.close()

        return redirect(
            url_for("{table_name}")
        )

    row = conn.execute(
        "SELECT * FROM {table_name} WHERE id = ?",
        (id,)
    ).fetchone()

    {parent_queries}

    conn.close()

    return render_template(
        "{table_name}_edit.html",
        row=row
        {template_context}
    )
"""
    # =====================================
    # Flask App
    # =====================================

    flask_code = f'''
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)
import sqlite3

app = Flask(__name__)

def get_connection():

    conn = sqlite3.connect(
        "database.db"
    )

    conn.row_factory = sqlite3.Row

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn

def init_db():

    conn = sqlite3.connect("database.db")

    with open("schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")

{routes}

if __name__ == "__main__":

    init_db()

    app.run(debug=True)
'''

    with open(
        os.path.join(output_dir, "app.py"),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(flask_code)

    # =====================================
    # Home Page
    # =====================================

    home_html = f"""
<!DOCTYPE html>

<html>

<head>
<title>{report["application_type"]}</title>
</head>

<body>

<h1>{report["application_type"]}</h1>

<h2>Modules</h2>

<ul>
"""

    for module in report["modules"]:
        home_html += f"<li>{module}</li>"

    home_html += """
</ul>

<h2>Generated Tables</h2>
"""

    for table in report["tables"]:

        table_name = table["table_name"]

        display_name = (
            table_name
            .replace("_", " ")
            .title()
        )

        home_html += f"""
<a href="/{table_name}">
{display_name}
</a>

<br><br>
"""

    home_html += """
</body>
</html>
"""

    with open(
        os.path.join(
            templates_dir,
            "index.html"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(home_html)

    # =====================================
    # Dynamic Template Generation
    # =====================================

    for table in report["tables"]:

        table_name = table["table_name"]

        columns = table["columns"]

        fk_fields = foreign_key_metadata.get(
            table_name,
            {}
        )

        table_calculated_fields = (
            calculated_fields
        )

        display_name = (
            table_name
            .replace("_", " ")
            .title()
        )

        # ---------------------------------
        # LIST PAGE
        # ---------------------------------

        list_html = f"""
<!DOCTYPE html>

<html>

<head>
<title>{display_name}</title>
</head>

<body>

<h1>{display_name}</h1>

<a href="/{table_name}/add">
Add Record
</a>

<br><br>

<table border="1">

<tr>
<th>ID</th>

{{% for col in columns %}}
<th>{{{{ col }}}}</th>
{{% endfor %}}

<th>Actions</th>

</tr>

{{% for row in rows %}}

<tr>

<td>{{{{ row["id"] }}}}</td>

{{% for col in columns %}}
<td>{{{{ row[col] }}}}</td>
{{% endfor %}}

<td>

<a href="/{table_name}/edit/{{{{ row['id'] }}}}">
Edit
</a>

<br><br>

<form
    method="POST"
    action="/{table_name}/delete/{{{{ row['id'] }}}}"
>

<button type="submit">
Delete
</button>

</form>

</td>


</tr>

{{% endfor %}}

</table>

<br><br>

<a href="/">
Back Home
</a>

</body>
</html>
"""

        with open(
            os.path.join(
                templates_dir,
                f"{table_name}_list.html"
            ),
            "w",
            encoding="utf-8"
        ) as f:

            f.write(list_html)

        # ---------------------------------
        # ADD PAGE
        # ---------------------------------

        add_html = f"""
<!DOCTYPE html>

<html>

<head>
<title>Add {display_name}</title>
</head>

<body>

<h1>Add {display_name}</h1>

<form method="POST">
"""

        for col in columns:

           sql_name = (
               col.lower()
               .replace(" ", "_")
               .replace("%", "percent")
               .replace("(", "")
               .replace(")", "")
           )

           if col in fk_fields:

               context_name = (
                   fk_fields[col]["context_name"]
               )

               parent_column = (
                   fk_fields[col]["parent_column"]
                   .lower()
                   .replace(" ", "_")
                   .replace("%", "percent")
                   .replace("(", "")
                   .replace(")", "")
               )

               add_html += f"""
        <label>{col}</label>
        <br>

        <select name="{sql_name}">

        {{% for item in {context_name} %}}

        <option value="{{{{ item['{parent_column}'] }}}}">
           {{{{ item['{parent_column}'] }}}}
        </option>

        {{% endfor %}}

        </select>

        <br><br>
        """

           else:

               readonly_attr = ""

               if sql_name in table_calculated_fields:
                  readonly_attr = "readonly"

               add_html += f"""
           <label>{col}</label>
           <br>

           <input
           type="text"
           name="{sql_name}"
           {readonly_attr}
           >

           <br><br>
           """

        add_html += """
<button type="submit">
Save
</button>

</form>

<br>

<a href="/">
Back Home
</a>

</body>
</html>
"""

        with open(
            os.path.join(
                templates_dir,
                f"{table_name}_add.html"
            ),
            "w",
            encoding="utf-8"
        ) as f:

            f.write(add_html)


        edit_html = f"""
<!DOCTYPE html>

<html>

<head>
<title>Edit {display_name}</title>
</head>

<body>

<h1>Edit {display_name}</h1>

<form method="POST">
"""

        for col in columns:

           sql_name = (
              col.lower()
              .replace(" ", "_")
              .replace("%", "percent")
              .replace("(", "")
              .replace(")", "")
           )

           if col in fk_fields:

              context_name = (
                fk_fields[col]["context_name"]
              )

              parent_column = (
                  fk_fields[col]["parent_column"]
                  .lower()
                  .replace(" ", "_")
                  .replace("%", "percent")
                  .replace("(", "")
                  .replace(")", "")
              )

              edit_html += f"""
        <label>{col}</label>

        <br>

        <select name="{sql_name}">

        {{% for item in {context_name} %}}

        <option
        value="{{{{ item['{parent_column}'] }}}}"

        {{% if row['{sql_name}'] == item['{parent_column}'] %}}
        selected
        {{% endif %}}

        >
        {{{{ item['{parent_column}'] }}}}
        </option>

        {{% endfor %}}

        </select>

        <br><br>
        """

           else:

               readonly_attr = ""

               if sql_name in table_calculated_fields:
                   readonly_attr = "readonly"

               edit_html += f"""
           <label>{col}</label>

           <br>

           <input
           type="text"
           name="{sql_name}"
           value="{{{{ row['{sql_name}'] }}}}"
           {readonly_attr}
           >

           <br><br>
           """

        edit_html += """
<button type="submit">
Update
</button>

</form>

<br>

<a href="/">
Back Home
</a>

</body>
</html>
"""

        with open(
          os.path.join(
             templates_dir,
             f"{table_name}_edit.html"
          ),
          "w",
          encoding="utf-8"
        ) as f:

          f.write(edit_html)

    return output_dir