# Python Generators Project

## About the Project

This project explores advanced usage of Python generators to efficiently handle large datasets, process data in batches, and simulate real-world scenarios involving live updates and memory-efficient computations. The tasks focus on leveraging Python’s `yield` keyword to implement generators that provide iterative access to data, promoting optimal resource utilization and improving performance in data-driven applications.

## Learning Objectives

By completing this project, you will:

- **Master Python Generators:** Learn to create and utilize generators for iterative data processing, enabling memory-efficient operations.
- **Handle Large Datasets:** Implement batch processing and lazy loading to work with extensive datasets without overloading memory.
- **Simulate Real-world Scenarios:** Develop solutions to simulate live data updates and apply them to streaming contexts.
- **Optimize Performance:** Use generators to calculate aggregate functions like averages on large datasets, minimizing memory consumption.
- **Apply SQL Knowledge:** Use SQL queries to fetch data dynamically, integrating Python with databases for robust data management.

## Requirements

- Proficiency in Python 3.x
- Understanding of `yield` and Python’s generator functions
- Familiarity with SQL and database operations (MySQL and SQLite)
- Basic knowledge of database schema design and data seeding
- Ability to use Git and GitHub for version control and submission

---

## Tasks

### 0. Getting Started with Python Generators

**Objective:** Create a generator that streams rows from an SQL database one by one.

- Set up a MySQL database `ALX_prodev` with a `user_data` table.
- Populate the database with sample data from `user_data.csv`.
- Implement functions to connect, create database/table, and insert data.
- **File:** `seed.py`

### 1. Generator that Streams Rows from an SQL Database

**Objective:** Create a generator that streams rows from the `user_data` table one by one using `yield`.

- Implement `stream_users()` to fetch rows as dictionaries.
- Use only one loop.
- **File:** `0-stream_users.py`

### 2. Batch Processing Large Data

**Objective:** Create a generator to fetch and process data in batches.

- Implement `stream_users_in_batches(batch_size)` to fetch rows in batches.
- Implement `batch_processing(batch_size)` to filter users over the age of 25.
- Use no more than three loops.
- **File:** `1-batch_processing.py`

### 3. Lazy Loading Paginated Data

**Objective:** Simulate fetching paginated data using a generator for lazy loading.

- Implement `lazy_paginate(page_size)` to fetch pages only when needed.
- Use only one loop and the provided `paginate_users` function.
- **File:** `2-lazy_paginate.py`

### 4. Memory-Efficient Aggregation with Generators

**Objective:** Use a generator to compute a memory-efficient aggregate function (average age).

- Implement `stream_user_ages()` to yield user ages one by one.
- Calculate the average age without loading the entire dataset into memory.
- Use no more than two loops and do not use SQL `AVERAGE`.
- **File:** `4-stream_ages.py`

### 5. Manual Review

- Ensure all requirements are met and code is well-documented.
- **Directory:** `python-generators-0x00`

---

## Repository Structure

```
alx-backend-python/
└── python-generators-0x00/
    ├── seed.py
    ├── 0-stream_users.py
    ├── 1-batch_processing.py
    ├── 2-lazy_paginate.py
    ├── 4-stream_ages.py
    └── README.md
```

---

## Usage

- Follow the prototypes and instructions in each task.
- Use the provided main files to test your implementations.
- Ensure your code is efficient and adheres to the constraints (loops, memory usage).

---

