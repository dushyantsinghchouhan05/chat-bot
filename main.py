import sqlite3
import re
import streamlit as st
from datetime import datetime

# Configure Streamlit page
st.set_page_config(page_title="Employee Assistant", layout="wide")

# Sidebar instructions
st.sidebar.header("Usage Guide")
st.sidebar.write("""
    Example queries:
    - "List all employees in the [Department] department."
    - "Who manages the [Department] department?"
    - "Show employees hired after [YYYY-MM-DD]."
    - "Display the highest-paid employee."
    - "What is the total salary expenditure for [Department]?"
""")

# Function to execute queries

def run_query(sql, params=()):
    with sqlite3.connect("chat_assistant.db") as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

# Helper functions

def get_department(text):
    match = re.search(r"in the (\w+) department", text, re.IGNORECASE)
    return match.group(1) if match else None

def get_date(text):
    match = re.search(r"after (\d{4}-\d{2}-\d{2})", text)
    return match.group(1) if match else None

def valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Query processing logic
def handle_query(user_input):
    if not user_input:
        return "No input detected. Please enter a query."
    
    if "List all employees in the" in user_input:
        department = get_department(user_input)
        if not department:
            return "Specify a department."
        
        data = run_query("SELECT Name FROM Employees WHERE Department = ?", (department,))
        return f"Employees in {department}: {', '.join(row[0] for row in data)}" if data else f"No employees found in {department}."
    
    elif "Who manages the" in user_input:
        department = get_department(user_input)
        if not department:
            return "Specify a department."
        
        data = run_query("SELECT Manager FROM Departments WHERE Name = ?", (department,))
        return f"Manager of {department}: {data[0][0]}" if data else "Department not found."
    
    elif "Show employees hired after" in user_input:
        date = get_date(user_input)
        if not date or not valid_date(date):
            return "Invalid date format. Use YYYY-MM-DD."
        
        data = run_query("SELECT Name FROM Employees WHERE Hire_Date > ?", (date,))
        return f"Employees hired after {date}: {', '.join(row[0] for row in data)}" if data else "No employees found."
    
    elif "Display the highest-paid employee" in user_input:
        data = run_query("SELECT Name, Salary, Department FROM Employees ORDER BY Salary DESC LIMIT 1")
        return f"Highest-paid employee: {data[0][0]} ({data[0][2]}), Salary: ${data[0][1]:,.2f}" if data else "No salary data available."
    
    elif "total salary expenditure for" in user_input:
        department = get_department(user_input)
        if not department:
            return "Specify a department."
        
        data = run_query("SELECT SUM(Salary) FROM Employees WHERE Department = ?", (department,))
        return f"Total salary expense for {department}: ${data[0][0]:,.2f}" if data and data[0][0] else f"No data for {department}."
    
    return "Query not recognized. Please rephrase."

# Streamlit UI
st.title("📊 Employee Insights Assistant")
st.write("Ask about employees, departments, salaries, and more!")

# User query input
user_query = st.text_area("Enter your query:", height=150)

if user_query:
    with st.spinner("Fetching results..."):
        output = handle_query(user_query)
    st.markdown(f"### Response:\n{output}")
