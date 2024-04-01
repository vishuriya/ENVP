import sqlite3
def database_conn():
    conn = sqlite3.connect('LOGSQAS.db')
    cursor = conn.cursor()
    return cursor,conn