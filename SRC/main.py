import os  
import pymssql

try:
    conn = pymssql.connect(
        server=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=1433,
    )

    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()

    print("\n CONEXÃO BEM-SUCEDIDA")
    print("SQL Server:", row[0])

    conn.close()

except Exception as e:
    print("\n FALHA NA CONEXÃO")
    print(type(e).__name__, "→", e)