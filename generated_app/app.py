
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
