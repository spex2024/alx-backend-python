
"""
4-stream_ages.py
Compute average age using generator for memory efficiency
"""

import random

def stream_user_ages():
    """
    Generator that yields user ages one by one.
    In real-world use, this could stream from a file, database, or API.
    """
    # Simulating large data stream with random ages
    for _ in range(1000000):  # Simulate 1 million users
        yield random.randint(18, 90)  # Age between 18 and 90


def calculate_average_age():
    """
    Consumes the generator to compute average age without loading entire data into memory.
    """
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total / count
        print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()
