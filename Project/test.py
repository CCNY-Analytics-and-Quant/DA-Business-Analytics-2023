import pyodbc

server = 'johndroescher.com'
database = 'sum_2023'
username = 'DENISSEBEATO99'
password = 'CCny24021299'
driver= '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM pizza_types;")

row = cursor.fetchone()
for x in row:
    print(x)

cursor.close()