import json
import os
from collections import Counter

# File used for permanent employee data storage
FILE_NAME = "employees.json"


# -------------------- FILE HANDLING FUNCTIONS --------------------

def load_employees():
    """
    Load employee records from employees.json.

    If the file does not exist, create it automatically.
    If the file contains invalid/corrupted JSON, return an empty list safely.
    """
    if not os.path.exists(FILE_NAME):
        # Create an empty JSON file if it does not exist
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            employees = json.load(file)

            # The saved data should always be a list
            if isinstance(employees, list):
                return employees

            print("\nWarning: Invalid data format found in employees.json.")
            print("Starting with an empty employee list.")
            return []

    except json.JSONDecodeError:
        print("\nWarning: employees.json contains corrupted or invalid JSON.")
        print("Starting with an empty employee list.")
        return []

    except OSError as error:
        print(f"\nError reading employee file: {error}")
        return []


def save_employees(employees):
    """
    Save employee records to employees.json.
    This function is called after add, update, and delete operations.
    """
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(employees, file, indent=4)

    except OSError as error:
        print(f"\nError saving employee data: {error}")


# -------------------- VALIDATION FUNCTIONS --------------------

def get_non_empty_input(message):
    """Keep asking until the user enters a non-empty value."""
    while True:
        value = input(message).strip()

        if value:
            return value

        print("This field cannot be empty. Please try again.")


def get_valid_salary(message):
    """Get a valid non-negative salary from the user."""
    while True:
        salary_input = input(message).strip()

        try:
            salary = float(salary_input)

            if salary < 0:
                print("Salary cannot be negative. Please enter a valid amount.")
            else:
                return salary

        except ValueError:
            print("Invalid salary. Please enter a numeric value.")


def find_employee_by_id(employees, employee_id):
    """Return an employee dictionary matching the given ID, or None."""
    for employee in employees:
        if employee["id"].lower() == employee_id.lower():
            return employee

    return None


# -------------------- DISPLAY FUNCTIONS --------------------

def print_employee(employee):
    """Display details of one employee."""
    print("-" * 45)
    print(f"Employee ID  : {employee['id']}")
    print(f"Name         : {employee['name']}")
    print(f"Department   : {employee['department']}")
    print(f"Designation  : {employee['designation']}")
    print(f"Salary       : {employee['salary']:.2f}")
    print(f"Performance  : {employee['performance']}")
    print("-" * 45)


def print_employee_list(employees):
    """Display a list of employees in table format."""
    if not employees:
        print("\nNo employee records found.")
        return

    print("\n" + "=" * 105)
    print(
        f"{'ID':<15}"
        f"{'Name':<23}"
        f"{'Department':<18}"
        f"{'Designation':<20}"
        f"{'Salary':<14}"
        f"{'Performance'}"
    )
    print("=" * 105)

    for employee in employees:
        print(
            f"{employee['id']:<15}"
            f"{employee['name']:<23}"
            f"{employee['department']:<18}"
            f"{employee['designation']:<20}"
            f"{employee['salary']:<14.2f}"
            f"{employee['performance']}"
        )

    print("=" * 105)


# -------------------- EMPLOYEE CRUD FUNCTIONS --------------------

def add_employee(employees):
    """Add a new employee and save the record permanently."""
    print("\n--- Add Employee ---")

    while True:
        employee_id = get_non_empty_input("Enter Employee ID: ")

        if find_employee_by_id(employees, employee_id):
            print("This Employee ID already exists. Please enter a unique ID.")
        else:
            break

    employee_name = get_non_empty_input("Enter Employee Name: ")
    department = get_non_empty_input("Enter Department: ")
    designation = get_non_empty_input("Enter Designation: ")
    salary = get_valid_salary("Enter Salary: ")
    performance = get_non_empty_input("Enter Performance: ")

    new_employee = {
        "id": employee_id,
        "name": employee_name,
        "department": department,
        "designation": designation,
        "salary": salary,
        "performance": performance
    }

    employees.append(new_employee)
    save_employees(employees)

    print("\nEmployee added successfully.")


def view_all_employees(employees):
    """Display all employee records."""
    print("\n--- All Employees ---")
    print_employee_list(employees)


def update_employee(employees):
    """Update an existing employee and save the changes."""
    print("\n--- Update Employee ---")

    employee_id = get_non_empty_input("Enter Employee ID to update: ")
    employee = find_employee_by_id(employees, employee_id)

    if employee is None:
        print("Employee not found.")
        return

    print("\nCurrent Employee Details:")
    print_employee(employee)

    print("Leave a field blank to keep its current value.")

    new_name = input(f"New Name [{employee['name']}]: ").strip()
    new_department = input(f"New Department [{employee['department']}]: ").strip()
    new_designation = input(f"New Designation [{employee['designation']}]: ").strip()
    new_salary = input(f"New Salary [{employee['salary']:.2f}]: ").strip()
    new_performance = input(f"New Performance [{employee['performance']}]: ").strip()

    # Update only the fields where the user entered a new value
    if new_name:
        employee["name"] = new_name

    if new_department:
        employee["department"] = new_department

    if new_designation:
        employee["designation"] = new_designation

    if new_salary:
        try:
            salary_value = float(new_salary)

            if salary_value >= 0:
                employee["salary"] = salary_value
            else:
                print("Salary cannot be negative. Existing salary was kept.")

        except ValueError:
            print("Invalid salary entered. Existing salary was kept.")

    if new_performance:
        employee["performance"] = new_performance

    save_employees(employees)
    print("\nEmployee updated successfully.")


def delete_employee(employees):
    """Delete an employee by ID and save the changes."""
    print("\n--- Delete Employee ---")

    employee_id = get_non_empty_input("Enter Employee ID to delete: ")
    employee = find_employee_by_id(employees, employee_id)

    if employee is None:
        print("Employee not found.")
        return

    print("\nEmployee to be deleted:")
    print_employee(employee)

    confirmation = input("Are you sure you want to delete this employee? (yes/no): ").strip().lower()

    if confirmation == "yes":
        employees.remove(employee)
        save_employees(employees)
        print("Employee deleted successfully.")
    else:
        print("Delete operation cancelled.")


# -------------------- SEARCH FUNCTIONS --------------------

def search_by_id(employees):
    """Search for one employee using Employee ID."""
    employee_id = get_non_empty_input("Enter Employee ID: ")
    employee = find_employee_by_id(employees, employee_id)

    if employee is None:
        print("Employee not found.")
    else:
        print("\nEmployee Found:")
        print_employee(employee)


def search_by_name(employees):
    """Search employees by full or partial name, ignoring letter case."""
    name = get_non_empty_input("Enter full or partial employee name: ").lower()

    matching_employees = [
        employee for employee in employees
        if name in employee["name"].lower()
    ]

    print_employee_list(matching_employees)


def search_by_department(employees):
    """Search employees by department, ignoring letter case."""
    department = get_non_empty_input("Enter department name: ").lower()

    matching_employees = [
        employee for employee in employees
        if department in employee["department"].lower()
    ]

    print_employee_list(matching_employees)


def search_by_salary(employees):
    """Search employees using salary conditions."""
    if not employees:
        print("No employee records available.")
        return

    while True:
        print("\nSalary Search Options")
        print("1. Exact Salary")
        print("2. Salary Greater Than")
        print("3. Salary Less Than")
        print("4. Salary Range")
        print("5. Back to Search Menu")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            salary = get_valid_salary("Enter exact salary: ")

            matching_employees = [
                employee for employee in employees
                if employee["salary"] == salary
            ]

            print_employee_list(matching_employees)

        elif choice == "2":
            salary = get_valid_salary("Enter salary amount: ")

            matching_employees = [
                employee for employee in employees
                if employee["salary"] > salary
            ]

            print_employee_list(matching_employees)

        elif choice == "3":
            salary = get_valid_salary("Enter salary amount: ")

            matching_employees = [
                employee for employee in employees
                if employee["salary"] < salary
            ]

            print_employee_list(matching_employees)

        elif choice == "4":
            minimum_salary = get_valid_salary("Enter minimum salary: ")
            maximum_salary = get_valid_salary("Enter maximum salary: ")

            if minimum_salary > maximum_salary:
                print("Minimum salary cannot be greater than maximum salary.")
                continue

            matching_employees = [
                employee for employee in employees
                if minimum_salary <= employee["salary"] <= maximum_salary
            ]

            print_employee_list(matching_employees)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


def search_employee_menu(employees):
    """Display the Search Employee submenu."""
    while True:
        print("\n--- Search Employee ---")
        print("1. Search by Employee ID")
        print("2. Search by Employee Name")
        print("3. Search by Salary")
        print("4. Search by Department")
        print("5. Back to Main Menu")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            search_by_id(employees)

        elif choice == "2":
            search_by_name(employees)

        elif choice == "3":
            search_by_salary(employees)

        elif choice == "4":
            search_by_department(employees)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


# -------------------- SALARY COMPARISON FUNCTIONS --------------------

def salary_comparison(employees):
    """Compare salaries and show highest, lowest, and average salary."""
    if not employees:
        print("\nNo employee records available for salary comparison.")
        return

    print("\n--- Salary Comparison ---")
    print("1. Compare Salaries of Two Employees")
    print("2. Show Highest-Paid Employee")
    print("3. Show Lowest-Paid Employee")
    print("4. Show Average Salary")
    print("5. Back to Main Menu")

    choice = input("Enter your choice (1-5): ").strip()

    if choice == "1":
        first_id = get_non_empty_input("Enter first Employee ID: ")
        second_id = get_non_empty_input("Enter second Employee ID: ")

        first_employee = find_employee_by_id(employees, first_id)
        second_employee = find_employee_by_id(employees, second_id)

        if first_employee is None or second_employee is None:
            print("One or both Employee IDs were not found.")
            return

        first_salary = first_employee["salary"]
        second_salary = second_employee["salary"]
        salary_difference = abs(first_salary - second_salary)

        print("\nSalary Comparison Result")
        print(f"{first_employee['name']} ({first_employee['id']}): {first_salary:.2f}")
        print(f"{second_employee['name']} ({second_employee['id']}): {second_salary:.2f}")
        print(f"Salary Difference: {salary_difference:.2f}")

        if first_salary > second_salary:
            print(f"{first_employee['name']} has the higher salary.")
        elif second_salary > first_salary:
            print(f"{second_employee['name']} has the higher salary.")
        else:
            print("Both employees have the same salary.")

    elif choice == "2":
        highest_paid = max(employees, key=lambda employee: employee["salary"])

        print("\nHighest-Paid Employee:")
        print_employee(highest_paid)

    elif choice == "3":
        lowest_paid = min(employees, key=lambda employee: employee["salary"])

        print("\nLowest-Paid Employee:")
        print_employee(lowest_paid)

    elif choice == "4":
        average_salary = sum(employee["salary"] for employee in employees) / len(employees)
        print(f"\nAverage Employee Salary: {average_salary:.2f}")

    elif choice == "5":
        return

    else:
        print("Invalid choice. Please enter a number from 1 to 5.")


# -------------------- EMPLOYEE STATISTICS --------------------

def employee_statistics(employees):
    """Display overall employee statistics."""
    if not employees:
        print("\nNo employee records available for statistics.")
        return

    total_employees = len(employees)
    salaries = [employee["salary"] for employee in employees]

    average_salary = sum(salaries) / total_employees
    highest_salary = max(salaries)
    lowest_salary = min(salaries)

    # Counter counts repeated values automatically
    department_count = Counter(
        employee["department"] for employee in employees
    )

    performance_count = Counter(
        employee["performance"] for employee in employees
    )

    print("\n--- Employee Statistics ---")
    print(f"Total Number of Employees: {total_employees}")
    print(f"Average Salary            : {average_salary:.2f}")
    print(f"Highest Salary            : {highest_salary:.2f}")
    print(f"Lowest Salary             : {lowest_salary:.2f}")

    print("\nEmployees by Department:")
    for department, count in department_count.items():
        print(f"- {department}: {count}")

    print("\nEmployees by Performance Level:")
    for performance, count in performance_count.items():
        print(f"- {performance}: {count}")


# -------------------- MAIN PROGRAM --------------------

def main():
    """
    Main function of the Employee Management System.
    Employee records are loaded when the application starts.
    """
    employees = load_employees()

    print("=" * 45)
    print("     EMPLOYEE MANAGEMENT SYSTEM")
    print("=" * 45)

    while True:
        print("\nMain Menu")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Salary Comparison")
        print("7. Employee Statistics")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_employee(employees)

        elif choice == "2":
            view_all_employees(employees)

        elif choice == "3":
            search_employee_menu(employees)

        elif choice == "4":
            update_employee(employees)

        elif choice == "5":
            delete_employee(employees)

        elif choice == "6":
            salary_comparison(employees)

        elif choice == "7":
            employee_statistics(employees)

        elif choice == "8":
            print("\nThank you for using the Employee Management System.")
            print("All changes have been saved to employees.json.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


# This runs the main program only when this file is executed directly
if __name__ == "__main__":
    main()