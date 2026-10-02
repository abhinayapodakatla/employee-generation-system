from flask import Flask, render_template, request, redirect, flash
import json
import os
import sqlite3
app = Flask(__name__)

app.secret_key = "employee-management-secret-key"

FILE_NAME = "employees.json"
DATABASE = "database.db"


def get_db_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


def create_table():
    def get_db_connection():

        connection = sqlite3.connect(DATABASE)

        connection.row_factory = sqlite3.Row

        return connection


def create_table():

    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            salary REAL NOT NULL,
            department TEXT NOT NULL,
            performance TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()


def migrate_json_to_database():

    if not os.path.exists(FILE_NAME):
        return

    try:

        with open(FILE_NAME, "r") as file:
            employees = json.load(file)

        connection = get_db_connection()

        for employee in employees:

            connection.execute("""
                INSERT OR IGNORE INTO employees
                (id, name, salary, department, performance)
                VALUES (?, ?, ?, ?, ?)
            """, (
                employee["id"],
                employee["name"],
                employee["salary"],
                employee["department"],
                employee["performance"]
            ))

        connection.commit()

        connection.close()

        print("Employee data migrated to database successfully!")

    except Exception as error:

        print("Migration error:", error)
    return connection


def load_employees():

    connection = get_db_connection()

    employees = connection.execute("""
        SELECT * FROM employees
    """).fetchall()

    connection.close()

    return employees


def save_employees(employees):
    with open(FILE_NAME, "w") as file:
        json.dump(employees, file, indent=4)


@app.route("/")
def home():

    employees = load_employees()

    total_employees = len(employees)

    # Calculate average salary
    if employees:
        total_salary = sum(employee["salary"] for employee in employees)
        average_salary = total_salary / total_employees
    else:
        average_salary = 0

    # Count departments
    departments = set()

    for employee in employees:
        departments.add(employee["department"])

    total_departments = len(departments)

    # Count employees by department
    department_counts = {}

    for employee in employees:
        department = employee["department"]

        if department not in department_counts:
            department_counts[department] = 0

        department_counts[department] += 1

    # Calculate salary by department
    department_salary = {}

    for employee in employees:
        department = employee["department"]

        if department not in department_salary:
            department_salary[department] = 0

        department_salary[department] += employee["salary"]

    return render_template(
        "index.html",
        employees=employees,
        total_employees=total_employees,
        average_salary=average_salary,
        total_departments=total_departments,
        department_counts=department_counts,
        department_salary=department_salary,
        search_performed=False
    )

# ---------------- ADD EMPLOYEE ----------------
@app.route("/add", methods=["POST"])
def add_employee():

    employee_id = request.form["employee_id"].strip()
    name = request.form["name"].strip()
    salary = request.form["salary"].strip()
    department = request.form["department"].strip()
    performance = request.form["performance"].strip()

    # Empty field validation
    if not employee_id or not name or not salary or not department:

        flash("All fields are required!", "error")

        return redirect("/")

    # Salary validation
    try:

        salary = float(salary)

    except ValueError:

        flash("Salary must be a valid number!", "error")

        return redirect("/")

    # Salary must be greater than 0
    if salary <= 0:

        flash("Salary must be greater than 0!", "error")

        return redirect("/")

    # Connect to database
    connection = get_db_connection()

    # Check duplicate ID
    existing_employee = connection.execute(
        "SELECT id FROM employees WHERE LOWER(id) = LOWER(?)",
        (employee_id,)
    ).fetchone()

    if existing_employee:

        connection.close()

        flash("Employee ID already exists!", "error")

        return redirect("/")

    # Insert employee into database
    connection.execute("""
        INSERT INTO employees
        (id, name, salary, department, performance)
        VALUES (?, ?, ?, ?, ?)
    """, (
        employee_id,
        name,
        salary,
        department,
        performance
    ))

    connection.commit()

    connection.close()

    flash("Employee added successfully!", "success")

    return redirect("/")

# ---------------- SEARCH EMPLOYEE ----------------
@app.route("/search")
def search():

    search_type = request.args.get("search_type")
    search_value = request.args.get("search_value", "").strip()

    connection = get_db_connection()

    # Search employees
    if search_type == "id":

        employees = connection.execute(
            "SELECT * FROM employees WHERE LOWER(id) LIKE LOWER(?)",
            (f"%{search_value}%",)
        ).fetchall()

    elif search_type == "name":

        employees = connection.execute(
            "SELECT * FROM employees WHERE LOWER(name) LIKE LOWER(?)",
            (f"%{search_value}%",)
        ).fetchall()

    elif search_type == "department":

        employees = connection.execute(
            "SELECT * FROM employees WHERE LOWER(department) LIKE LOWER(?)",
            (f"%{search_value}%",)
        ).fetchall()

    elif search_type == "salary":

        try:
            salary = float(search_value)

            employees = connection.execute(
                "SELECT * FROM employees WHERE salary = ?",
                (salary,)
            ).fetchall()

        except ValueError:
            employees = []

    else:
        employees = []

    # Get all employees for dashboard
    all_employees = connection.execute(
        "SELECT * FROM employees"
    ).fetchall()

    connection.close()

    # Dashboard calculations
    total_employees = len(all_employees)

    if all_employees:
        total_salary = sum(employee["salary"] for employee in all_employees)
        average_salary = total_salary / total_employees
    else:
        average_salary = 0

    departments = set()

    for employee in all_employees:
        departments.add(employee["department"])

    total_departments = len(departments)

    # Employees by department
    department_counts = {}

    for employee in all_employees:

        department = employee["department"]

        if department not in department_counts:
            department_counts[department] = 0

        department_counts[department] += 1

    # Salary by department
    department_salary = {}

    for employee in all_employees:

        department = employee["department"]

        if department not in department_salary:
            department_salary[department] = 0

        department_salary[department] += employee["salary"]

    return render_template(
        "index.html",
        employees=employees,
        total_employees=total_employees,
        average_salary=average_salary,
        total_departments=total_departments,
        department_counts=department_counts,
        department_salary=department_salary,
        search_performed=True
    )
    # ---------------- SALARY COMPARISON ----------------

@app.route("/compare")
def compare_salary():

    employee1_id = request.args.get("employee1")
    employee2_id = request.args.get("employee2")

    connection = get_db_connection()

    employee1 = connection.execute(
        "SELECT * FROM employees WHERE id = ?",
        (employee1_id,)
    ).fetchone()

    employee2 = connection.execute(
        "SELECT * FROM employees WHERE id = ?",
        (employee2_id,)
    ).fetchone()

    employees = connection.execute(
        "SELECT * FROM employees"
    ).fetchall()

    connection.close()

    difference = None

    if employee1 and employee2:

        difference = abs(
            employee1["salary"] - employee2["salary"]
        )

    return render_template(
        "compare.html",
        employees=employees,
        employee1=employee1,
        employee2=employee2,
        difference=difference
    )


# ---------------- EDIT EMPLOYEE ----------------

@app.route("/edit/<employee_id>")
def edit_employee(employee_id):

    connection = get_db_connection()

    employee = connection.execute(
        "SELECT * FROM employees WHERE id = ?",
        (employee_id,)
    ).fetchone()

    connection.close()

    if employee is None:
        return "Employee not found"

    return render_template(
        "edit.html",
        employee=employee
    )


# ---------------- UPDATE EMPLOYEE ----------------
@app.route("/update/<employee_id>", methods=["POST"])
def update_employee(employee_id):

    name = request.form["name"].strip()
    salary = request.form["salary"].strip()
    department = request.form["department"].strip()
    performance = request.form["performance"].strip()

    # Empty field validation
    if not name or not salary or not department:

        flash("All fields are required!", "error")

        return redirect(f"/edit/{employee_id}")

    # Salary validation
    try:

        salary = float(salary)

    except ValueError:

        flash("Salary must be a valid number!", "error")

        return redirect(f"/edit/{employee_id}")

    # Salary must be greater than 0
    if salary <= 0:

        flash("Salary must be greater than 0!", "error")

        return redirect(f"/edit/{employee_id}")

    # Connect to database
    connection = get_db_connection()

    # Update employee
    result = connection.execute("""
        UPDATE employees
        SET name = ?,
            salary = ?,
            department = ?,
            performance = ?
        WHERE id = ?
    """, (
        name,
        salary,
        department,
        performance,
        employee_id
    ))

    connection.commit()

    connection.close()

    # Check whether employee existed
    if result.rowcount == 0:

        flash("Employee not found!", "error")

        return redirect("/")

    flash("Employee updated successfully!", "success")

    return redirect("/")

# ---------------- DELETE EMPLOYEE ----------------

@app.route("/delete/<employee_id>")
def delete_employee(employee_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM employees WHERE id = ?",
        (employee_id,)
    )

    connection.commit()

    connection.close()

    flash("Employee deleted successfully!", "success")

    return redirect("/")


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":

    create_table()

    migrate_json_to_database()

    app.run(debug=True)