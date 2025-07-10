import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.conn, self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()

# Example usage with SELECT query
if __name__ == "__main__":
    try:
        with DatabaseConnection('users.db') as (conn, cursor):
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            print("Query results:", results)
    except Exception as e:
        print(f"Error: {str(e)}")
