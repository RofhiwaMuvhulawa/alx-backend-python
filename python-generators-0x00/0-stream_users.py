import mysql.connector
from mysql.connector import Error

def stream_users():
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            # Single loop to yield rows as dictionaries
            for row in cursor:
                yield {
                    "user_id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "age": row[3]
                }
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error streaming users: {e}")
