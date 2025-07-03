import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            batch = []
            # Loop 1: Fetch rows and build batches
            for row in cursor:
                batch.append({
                    "user_id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "age": row[3]
                })
                if len(batch) >= batch_size:
                    yield batch
                    batch = []
            # Yield any remaining rows
            if batch:
                yield batch
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error streaming users in batches: {e}")

def batch_processing(batch_size):
    # Loop 2: Iterate over batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 3: Filter users over 25 in each batch
        for user in batch:
            if user["age"] > 25:
                print(user)
