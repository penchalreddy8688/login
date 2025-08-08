import sqlite3

def get_db_connection(): #Dependency-compatible DB connection
    conn = sqlite3.connect("users.db",  check_same_thread=False)  #Setting check_same_thread=False disables this thread-safety check. This allows the database connection object to be shared and used by multiple threads within the same process.
    conn.row_factory = sqlite3.Row   #The statement conn.row_factory = sqlite3.Row in Python's sqlite3 module is used to change the way rows are returned when you fetch results from an SQLite database.
    try:
        yield conn  #yield(generator) will let FastAPI manage the cleanup .The yield keyword pauses generator function execution and the value of the expression following the yield keyword is returned to the generator's caller
    finally:
        conn.close()  # ensures connection is closed automatically


def init_db(): # Initialization function (run once when app starts)
    conn = sqlite3.connect("users.db")  # no need to use get_db_connection here
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()  # Run DB setup at import time
   