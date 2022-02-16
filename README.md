# Context_Manager_For_SQLite
A custom context manager for connecting and opening a cursor to a SQLite database.

Sample database is as provided by Prof. Johan van Niekerk to the "Programming databases" course at Noroff University College 2022.

# Purpose

Autmotatically close a cursor connection using Pythons 'with ...' statement.
All connections enforce referential integrity.

# Background info:

The class takes 1 required attribute parameter.
It then returns 2 kinds of tuple depending if the optional SQL query is provided when the context managers was called.

  - Without SQL statement:
    - (SQLite3 cursor object, SQLite connection object)
    - SQL statements can then be inserted to the object returned by the context manager
  - With SQL statement:
    - (SQLite cursor execute object, cursor.description return value)
    - Any results obtained by the SQL statenebt provided will be returned as an object.
    - The object is an iterable set of tuples, a tuple for each row of data returned by the database.

# Disclaimer

Use at your own peril. Open for code comments, corrections or improvements.
