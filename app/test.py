import pyodbc

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=localhost;'
                      'DATABASE=restauracjadb;'
                      'Trusted_Connection=yes')

print("Połączono z bazą danych!")