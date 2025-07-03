Python Generators for Efficient Data Processing
Project Overview
This project demonstrates the use of Python generators to efficiently handle large datasets, focusing on memory-efficient data processing and real-world streaming scenarios. The core functionality includes a Python script (seed.py) that sets up a MySQL database, creates a table, populates it with data from a CSV file, and provides a generator to stream database rows one by one.
Learning Objectives

Master Python generators for iterative, memory-efficient data processing.
Handle large datasets using batch processing and lazy loading.
Simulate real-world data streaming scenarios.
Optimize performance for aggregate calculations on large datasets.
Integrate Python with SQL databases for robust data management.

Requirements

Python 3.x
MySQL Server (running locally or accessible)
mysql-connector-python library (pip install mysql-connector-python)
CSV file (user_data.csv) with columns for user_id, name, email, and age
Basic knowledge of SQL, Python generators, and Git/GitHub
Git for version control

Setup Instructions

Install Dependencies:
pip install mysql-connector-python


Set Up MySQL:

Ensure MySQL is installed and running.
Update the database credentials in seed.py (e.g., host, user, password) to match your MySQL configuration.


Prepare CSV File:

Place the user_data.csv file in the project directory with the format:user_id,name,email,age
<uuid>,<name>,<email>,<age>




Run the Setup Script:

Execute 0-main.py to create the ALX_prodev database, user_data table, and populate it with CSV data:python3 0-main.py





Project Structure

seed.py: Contains functions to connect to MySQL, create the database and table, insert data from CSV, and a generator (stream_rows) to stream database rows.
0-main.py: Test script to verify database setup and data insertion.
user_data.csv: Sample CSV file with user data (not included; provide your own).
README.md: This file, documenting the project.

Usage
To stream rows from the user_data table using the generator:
from seed import connect_to_prodev, stream_rows

connection = connect_to_prodev()
if connection:
    for row in stream_rows(connection):
        print(row)  # Process each row (e.g., user_id, name, email, age)
    connection.close()

Key Functions in seed.py

connect_db(): Connects to the MySQL server.
create_database(connection): Creates the ALX_prodev database.
connect_to_prodev(): Connects to the ALX_prodev database.
create_table(connection): Creates the user_data table with user_id (UUID, primary key, indexed), name (VARCHAR), email (VARCHAR), and age (DECIMAL).
insert_data(connection, csv_file): Inserts data from user_data.csv into the table.
stream_rows(connection): Generator function to yield rows from user_data one by one.

Example Output
Running 0-main.py might produce:
connection successful
Table user_data created successfully
Database ALX_prodev is present
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ...]

Notes

The stream_rows generator is memory-efficient, ideal for large datasets as it yields rows one at a time.
Ensure user_data.csv exists in the project directory before running 0-main.py.
Adjust MySQL credentials in seed.py if needed.
The project uses INSERT IGNORE to prevent duplicate entries during data insertion.

Version Control

Use Git for version control.
Push your code to a GitHub repository for submission:git add .
git commit -m "Add Python generators project"
git push origin main



License
This project is for educational purposes and is not licensed for commercial use.
