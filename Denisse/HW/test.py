import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

server = 'johndroescher.com'
database = 'sum_2023'
username = 'DENISSEBEATO99'
password = 'CCny24021299'
driver= '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM pizza_types;")

row = cursor.fetchone()
df =  pd.DataFrame({'Pizza Type' : row[0],'Pizza Name' : [5]},index=[0])

print(df)

df.plot(x="Pizza Type", y="Pizza Name", kind="bar")
plt.show()

cursor.close()