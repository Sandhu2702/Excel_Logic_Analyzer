
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



@app.route("/employee_master")
def employee_master():

    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM employee_master"
    ).fetchall()

    conn.close()

    return render_template(
        "employee_master_list.html",
        rows=rows,
        columns=['employee_id', 'employee_name', 'department', 'experience_years', 'salary', 'performance_rating', 'attendance_percent', 'certification', 'location']
    )


@app.route(
    "/employee_master/add",
    methods=["GET", "POST"]
)
def add_employee_master():

    if request.method == "POST":

        conn = get_connection()

        conn.execute(
            """
            INSERT INTO employee_master
            (employee_id, employee_name, department, experience_years, salary, performance_rating, attendance_percent, certification, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (request.form.get("employee_id"), request.form.get("employee_name"), request.form.get("department"), request.form.get("experience_years"), request.form.get("salary"), request.form.get("performance_rating"), request.form.get("attendance_percent"), request.form.get("certification"), request.form.get("location"),)
        )

        conn.commit()
        conn.close()

        return redirect(
            url_for("employee_master")
        )

    conn = get_connection()



    conn.close()

    return render_template(
       "employee_master_add.html"
       
    )


@app.route(
    "/employee_master/delete/<int:id>",
    methods=["POST"]
)
def delete_employee_master(id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM employee_master WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(
        url_for("employee_master")
    )

@app.route(
    "/employee_master/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_employee_master(id):

    conn = get_connection()

    if request.method == "POST":

       conn.execute(
           """
           UPDATE employee_master
           SET employee_id=?, employee_name=?, department=?, experience_years=?, salary=?, performance_rating=?, attendance_percent=?, certification=?, location=?
           WHERE id = ?
           """,
           (request.form.get("employee_id"), request.form.get("employee_name"), request.form.get("department"), request.form.get("experience_years"), request.form.get("salary"), request.form.get("performance_rating"), request.form.get("attendance_percent"), request.form.get("certification"), request.form.get("location"), id)
       )

       conn.commit()
       conn.close()

       return redirect(
          url_for("employee_master")
       )

    row = conn.execute(
        "SELECT * FROM employee_master WHERE id = ?",
        (id,)
    ).fetchone()

    

    conn.close()

    return render_template(
        "employee_master_edit.html",
        row=row
        
    )


@app.route("/payroll_data")
def payroll_data():

    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM payroll_data"
    ).fetchall()

    conn.close()

    return render_template(
        "payroll_data_list.html",
        rows=rows,
        columns=['employee_id', 'salary', 'performance_score', 'department', 'bonus_percent', 'bonus_amount', 'scholarship', 'tax', 'net_salary', 'performance_grade', 'promotion', 'reward', 'experience_level']
    )


@app.route(
    "/payroll_data/add",
    methods=["GET", "POST"]
)
def add_payroll_data():

    if request.method == "POST":

        conn = get_connection()

        conn.execute(
            """
            INSERT INTO payroll_data
            (employee_id, salary, performance_score, department, bonus_percent, bonus_amount, scholarship, tax, net_salary, performance_grade, promotion, reward, experience_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (request.form.get("employee_id"), request.form.get("salary"), request.form.get("performance_score"), request.form.get("department"), request.form.get("bonus_percent"), request.form.get("bonus_amount"), request.form.get("scholarship"), request.form.get("tax"), request.form.get("net_salary"), request.form.get("performance_grade"), request.form.get("promotion"), request.form.get("reward"), request.form.get("experience_level"),)
        )

        conn.commit()
        conn.close()

        return redirect(
            url_for("payroll_data")
        )

    conn = get_connection()


    employee_master_options = conn.execute(
        "SELECT employee_id FROM employee_master"
    ).fetchall()


    conn.close()

    return render_template(
       "payroll_data_add.html"
       ,
        employee_master_options=employee_master_options

    )


@app.route(
    "/payroll_data/delete/<int:id>",
    methods=["POST"]
)
def delete_payroll_data(id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM payroll_data WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(
        url_for("payroll_data")
    )

@app.route(
    "/payroll_data/edit/<int:id>",
    methods=["GET", "POST"]
)
def edit_payroll_data(id):

    conn = get_connection()

    if request.method == "POST":

       conn.execute(
           """
           UPDATE payroll_data
           SET employee_id=?, salary=?, performance_score=?, department=?, bonus_percent=?, bonus_amount=?, scholarship=?, tax=?, net_salary=?, performance_grade=?, promotion=?, reward=?, experience_level=?
           WHERE id = ?
           """,
           (request.form.get("employee_id"), request.form.get("salary"), request.form.get("performance_score"), request.form.get("department"), request.form.get("bonus_percent"), request.form.get("bonus_amount"), request.form.get("scholarship"), request.form.get("tax"), request.form.get("net_salary"), request.form.get("performance_grade"), request.form.get("promotion"), request.form.get("reward"), request.form.get("experience_level"), id)
       )

       conn.commit()
       conn.close()

       return redirect(
          url_for("payroll_data")
       )

    row = conn.execute(
        "SELECT * FROM payroll_data WHERE id = ?",
        (id,)
    ).fetchone()

    
    employee_master_options = conn.execute(
        "SELECT employee_id FROM employee_master"
    ).fetchall()


    conn.close()

    return render_template(
        "payroll_data_edit.html",
        row=row
        ,
        employee_master_options=employee_master_options

    )


if __name__ == "__main__":

    init_db()

    app.run(debug=True)
