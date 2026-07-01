import os

def get_sqlite_type(dtype):

    dtype = str(dtype).lower()

    if "int" in dtype:
        return "INTEGER"

    elif "float" in dtype:
        return "REAL"

    else:
        return "TEXT"

def generate_database_schema(report, output_dir):

    schema_sql = ""

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

        columns_sql = ", ".join(column_names)

        placeholders = ", ".join(
           ["?"] * len(column_names)
        )

        form_values = ", ".join(
            [
               f'request.form.get("{col}")'
               for col in column_names
            ]
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

    return render_template(
        "{table_name}_add.html"
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

</tr>

{{% for row in rows %}}

<tr>

<td>{{{{ row["id"] }}}}</td>

{{% for col in columns %}}
<td>{{{{ row[col] }}}}</td>
{{% endfor %}}

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

          add_html += f"""
        <label>{col}</label>
        <br>

        <input
        type="text"
        name="{sql_name}"
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

    return output_dir