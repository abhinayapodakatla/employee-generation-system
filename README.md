# Employee Management System

A beginner-friendly **Employee Management System** built with **Python, Flask, and SQLite**.
The application provides a web-based interface to manage employee information, search employees, compare salaries, and view department statistics.

## 🚀 Features

* Add new employees
* Edit employee information
* Delete employees
* Search employees by:

  * Employee ID
  * Name
  * Department
  * Salary
* Salary comparison between employees
* Average salary calculation
* Department statistics
* Employee-by-department chart
* Salary-by-department chart
* SQLite database integration
* Responsive web interface
* Flash messages for user feedback

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **SQLite**
* **HTML5**
* **CSS3**
* **Jinja2**

## 📁 Project Structure

```text
employee-generation-system/
│
├── app.py
├── employee_management.py
├── employees.json
├── .gitignore
│
├── static/
│   └── style.css
│
└── templates/
    ├── compare.html
    ├── dashboard.html
    ├── edit.html
    ├── index.html
    └── login.html
```

## ⚙️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/abhinayapodakatla/employee-generation-system.git
```

### 2. Open the project folder

```bash
cd employee-generation-system
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install Flask

```bash
pip install flask
```

### 6. Run the application

```bash
python app.py
```

### 7. Open in your browser

```text
http://127.0.0.1:5000
```

## 🗄️ Database

The application uses **SQLite** for persistent employee data storage.

The SQLite database file is generated locally when the application runs and is excluded from Git tracking.

## 📊 Main Modules

### Employee Management

Users can add, edit, update, and delete employee records.

### Search

Employees can be searched using ID, name, department, or salary.

### Salary Comparison

The application allows users to compare the salaries of two employees and view the salary difference.

### Dashboard

The dashboard provides employee statistics and department-based visualizations.

## 🎯 Project Objective

The objective of this project is to build a practical employee management application while learning:

* Python programming
* Flask web development
* SQLite database operations
* CRUD operations
* HTML/CSS frontend development
* Data searching and filtering
* Basic data visualization
* Git and GitHub project management

## 👨‍💻 Author

**Abhinaya Podakatla**

B.Tech CSE (AI/ML) Student

---

⭐ If you find this project useful, feel free to explore the repository.
