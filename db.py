import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect('chat_assistant.db')
cursor = connection.cursor()

# Drop tables if they already exist (for testing purposes)
cursor.execute("DROP TABLE IF EXISTS Employees;")
cursor.execute("DROP TABLE IF EXISTS Departments;")

# Create Employees table
cursor.execute('''
    CREATE TABLE Employees (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Department TEXT NOT NULL,
        Salary INTEGER NOT NULL,
        Hire_Date TEXT NOT NULL
    );
''')

# Create Departments table
cursor.execute('''
    CREATE TABLE Departments (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Manager TEXT NOT NULL
    );
''')

# ✅ FIX: `executemany()` requires a second argument (a list of tuples)
employees_data = [
    ('Alice', 'Sales', 50000, '2021-01-15'),
    ('Bob', 'Engineering', 70000, '2020-06-10'),
    ('Charlie', 'Marketing', 60000, '2022-03-20')
]

departments_data = [
    ('Sales', 'Alice'),
    ('Engineering', 'Bob'),
    ('Marketing', 'Charlie')
]

cursor.executemany('''
    INSERT INTO Employees (Name, Department, Salary, Hire_Date) 
    VALUES (?, ?, ?, ?);
''', employees_data)

cursor.executemany('''
    INSERT INTO Departments (Name, Manager) 
    VALUES (?, ?);
''', departments_data)

# Commit changes and close connection
connection.commit()
connection.close()

print("✅ Database initialized successfully!")