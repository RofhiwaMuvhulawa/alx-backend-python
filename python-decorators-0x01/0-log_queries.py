import sqlite3
import functools
import logging
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the query from the first argument
        query = args[0] if args else "Unknown query"
        # Log the query with timestamp
        logging.info(f"Executing SQL query: {query}")
        try:
            # Execute the original function
            result = func(*args, **kwargs)
            logging.info(f"Query executed successfully")
            return result
        except Exception as e:
            # Log any errors that occur during query execution
            logging.error(f"Query failed: {str(e)}")
            raise
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
if __name__ == "__main__":
    try:
        users = fetch_all_users(query="SELECT * FROM users")
        print("Retrieved users:", users)
    except Exception as e:
        print(f"Error: {str(e)}")
