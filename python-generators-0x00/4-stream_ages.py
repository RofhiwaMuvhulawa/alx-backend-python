import seed
from decimal import Decimal

def stream_user_ages():
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:
            yield row[0]
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error streaming ages: {e}")

def calculate_average_age():
    total = Decimal('0')
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    if count == 0:
        print("No users found")
    else:
        average = total / count
        print(f"Average age of users: {average}")

if __name__ == "__main__":
    calculate_average_age()
