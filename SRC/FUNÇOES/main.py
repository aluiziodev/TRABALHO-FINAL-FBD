import os  
import pymssql 
import consultas as cons
import playlist as pl

def getConnection():
    return pymssql.connect(
        server=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=1433,
    )



try:
    conn = getConnection()

    cursor = conn.cursor()
    pl.manutençaoPlaylist(cursor, conn)


    conn.close()

except Exception as e:
    print("\n FALHA NA CONEXÃO")
    print(type(e).__name__, "→", e)