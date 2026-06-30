import os


def generate_flask_app(report):

    output_dir = "generated_app"

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(
        os.path.join(output_dir, "templates"),
        exist_ok=True
    )

    # -----------------------------
    # Flask App
    # -----------------------------

    flask_code = '''
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/source")
def source():
    return render_template("source.html")

@app.route("/target")
def target():
    return render_template("target.html")

if __name__ == "__main__":
    app.run(debug=True)
'''

    with open(
        os.path.join(output_dir, "app.py"),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(flask_code)

    # -----------------------------
    # Home Page
    # -----------------------------

    home_html = f'''
<!DOCTYPE html>

<html>
<head>
<title>{report["application_type"]}</title>
</head>

<body>

<h1>{report["application_type"]}</h1>

<h2>Modules</h2>

<ul>
'''

    for module in report["modules"]:
        home_html += f"<li>{module}</li>"

    home_html += '''

</ul>

<a href="/source">Source Data</a>
<br><br>
<a href="/target">Target Data</a>

</body>
</html>
'''

    with open(
        os.path.join(
            output_dir,
            "templates",
            "index.html"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(home_html)

    # -----------------------------
    # Source Page
    # -----------------------------

    source_html = """
<!DOCTYPE html>

<html>
<head>
<title>Source Entity</title>
</head>

<body>

<h1>Source Entity</h1>

<ul>
"""

    for col in report["source_columns"]:
        source_html += f"<li>{col}</li>"

    source_html += """

</ul>

<a href="/">Back</a>

</body>
</html>
"""

    with open(
        os.path.join(
            output_dir,
            "templates",
            "source.html"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(source_html)

    # -----------------------------
    # Target Page
    # -----------------------------

    target_html = """
<!DOCTYPE html>

<html>
<head>
<title>Target Entity</title>
</head>

<body>

<h1>Target Entity</h1>

<ul>
"""

    for col in report["target_columns"]:
        target_html += f"<li>{col}</li>"

    target_html += """

</ul>

<a href="/">Back</a>

</body>
</html>
"""

    with open(
        os.path.join(
            output_dir,
            "templates",
            "target.html"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(target_html)

    return output_dir