# FINAL Custom Context Manager
# Open a database and automatically close connection when exiting
# To-Do:
#   - Proper docstring
#   - Proper error handling


import sqlite3
import pandas as pd

class SQLiteDatabaseHandler():

  SQL = ""
  SQLobj = ''
  debug = False

  def __init__(self, db_name: str, *args: str, debug = False ) -> tuple:
    self.db_name = db_name
    self.debug = debug
    self.SQL = args
  
  def __enter__(self):
    self.conn = sqlite3.connect(self.db_name)
    self.cur = self.conn.cursor()
    self.cur.execute('''PRAGMA foreign_keys = ON;''')
    self.fkey_status = self.cur.execute('''PRAGMA foreign_keys;''').fetchall()
    if self.debug == True:
      print(f'Foreign Key referencial integrity is set to: {self.fkey_status[0][0]}')
    if self.SQL == ():
      if self.debug == True:
        print("No SQL command executed. Returning cursor object")
      return self.cur, self.conn
    for item in self.SQL:
      if self.debug == True:
        print(f'Executing SQL command. Returning SQL query result:\nSTART-->>>\n{self.SQL[0]}\n<<<--- END\n')
      return self.cur.execute(item), [header[0] for header in self.cur.description]
  
  def __exit__(self,exc_type,exc_value, exc_traceback):
    self.cur.close()
    print("Cursor closed")

def main():

  # Example queries:

  SQL1 = '''
  SELECT ProductName, CompanyName, SUM(OI.UnitPrice*OI.Quantity) as Total
  FROM Product P, Supplier S, OrderItem OI
  WHERE P.Id = OI.ProductID
    AND S.Id = P.SupplierID
    AND P.IsDiscontinued = 1
  GROUP BY ProductName, CompanyName
  ;'''


  SQL2 = '''
    SELECT ProductName, [Supplier].CompanyName, SUM(OrderItem.UnitPrice*OrderItem.Quantity) as Total
    FROM [OrderItem]
    INNER JOIN [Product]
      ON [OrderItem].ProductId = [Product].Id
    INNER JOIN [Supplier]
      ON Supplier.Id = [Product].SupplierId
    WHERE [Product].IsDiscontinued = 1
    GROUP BY [Product].ProductName, [Supplier].CompanyName
    ORDER BY Total
  ;'''

  # Using the context manager by using cursor object returned by the context manager. Allows easier use of of Pandas. Debug info = OFF
  with SQLiteDatabaseHandler("NW2020-test.db") as my_db_obj:
    pd_obj = pd.read_sql_query(SQL1, my_db_obj[1])
    print(pd_obj)

  print()

  SQL3 = '''
    PRAGMA table_info(Supplier)
  ;'''

  # Using the context manager by passing the SQL query directly to the context manager. Output is passed to Pandas dataframe with a little clunky syntax. Debug info = ON\n")
  with SQLiteDatabaseHandler("NW2020-test.db", SQL2) as my_db_obj:
    od_obj_output = pd.DataFrame([item for item in my_db_obj[0]], columns=my_db_obj[1])
    print(od_obj_output)

if __name__ == "__main__":
  main()
