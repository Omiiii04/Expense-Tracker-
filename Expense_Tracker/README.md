# Expense Tracker

## Description
The Expense Tracker is a simple web application built using Flask and MySQL. It allows users to manage their expenses by tracking transactions. The project is designed to be run locally and is suitable for learning purposes.

## Features
- User registration and authentication
- Transaction management (add, view, and delete transactions)
- Basic user roles and permissions

## Technologies Used
- **Python**: Programming language for backend logic
- **Flask**: Web framework for building the application
- **MySQL**: Database for storing user and transaction data
- **pymysql**: Python library for interacting with MySQL

## Set Up the Database
1. Open MySQL:
    ```bash
    mysql -u root -p
    ```
    Note: Make sure the user is root. If you use a custom password, change the `app.config['MYSQL_PASSWORD']` in `app.py` to your MySQL root password.

2. Create the database and tables:
    ```sql
    CREATE DATABASE simple_expense_tracker;
    USE simple_expense_tracker;

    CREATE TABLE app_users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    );

    CREATE TABLE user_expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        description VARCHAR(255) NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        date_added DATE NOT NULL,
        FOREIGN KEY (user_id) REFERENCES app_users(id) ON DELETE CASCADE
    );
    ```

## Clone the Repository
```bash
git clone https://github.com/Kanishka-User/Expense_Tracker.git
cd expense-tracker
```

## Set up the Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate
```

## Run the Application
```bash
python app.py
```
