
seed = __import__('seed')


def paginate_users(batch_size, offset):
    """Fetch a batch of users from the database"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def stream_users_in_batches(batch_size):
    """Generator that yields batches of users from the database"""
    offset = 0
    while True:
        batch = paginate_users(batch_size, offset)
        if not batch:
            break
        yield batch
        offset += batch_size


def batch_processing(batch_size):
    """Processes and prints users over the age of 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
