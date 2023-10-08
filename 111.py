import pyodbc
 
coon = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-4EJQ0G73;DATABASE=MRP;UID=sa;PWD=1234567890Wyx')
cursor=coon.cursor()
 
cursor.execute("SELECT * FROM MRP")
row=cursor.fetchone() 
row1=cursor.fetchall()
print(row)
print(row1)
