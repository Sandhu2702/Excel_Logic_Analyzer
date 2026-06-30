print("GENERATED APP RUNNING")

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def init_db():

    print("Initializing database...")

    conn = sqlite3.connect("database.db")

    with open("schema.sql", "r", encoding="utf-8") as f:
        sql = f.read()
        print(sql)
        conn.executescript(sql)

    conn.commit()
    conn.close()

    print("Database created successfully")


@app.route("/")
def home():
       return render_template("index.html")

    
@app.route("/employee_master")
def employee_master():
    return render_template("employee_master_list.html")


@app.route("/employee_master/add")
def add_employee_master():
    return render_template("employee_master_add.html")


@app.route("/employee_payroll")
def employee_payroll():
    return render_template("employee_payroll_list.html")


@app.route("/employee_payroll/add")
def add_employee_payroll():
    return render_template("employee_payroll_add.html")


if __name__ == "__main__":

    print("APP STARTING")

    init_db()

    print("AFTER INIT_DB")

    app.run(debug=True)
    