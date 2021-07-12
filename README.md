# Tests: SQL Queries in Assignment 2 (CSCC43 Summer 2021)

This project allows you to test the SQL Queries part of Assignment 2 (CSCC43 Summer 2021) using Python's [`unittest`](https://docs.python.org/3/library/unittest.html) framework. Feel free to add any tests in `test/`.

## Requirements

Before running tests, install [`Pipenv`](https://pipenv.pypa.io/en/latest/) and then run `pipenv install` from the project directory.

## Follow these steps to get tests working

### Step 1: Enter Shell

```
pipenv shell
```

### Step 2: Add your queries

In `test/test_q1.py` to `test/test_q7.py`, update `query` instance variable in each test case with the query you want to test.

### Step 3: Configure PostgreSQL

#### Step 3(a): Set up a PostgreSQL database instance

First, set up a PostgreSQL database. On Docker, you can simply spin up a container:

```
docker run -p 5433:5432 -e POSTGRES_PASSWORD=Password@123 -d postgres 
```

#### Step 3(b): Run `a2DDL.sql`

Run the Data Definition Language queries in your PostgreSQL console.

#### Step 3(c): Configure PostgreSQL database details

Update `db = peewee.PostgresqlDatabase(...` in `test/utils/database.py` with the appropriate credentials of your PostgreSQL instance.

### Step 4: Run the tests

Repeat this step to check if all views have been dropped.

```
python -m unittest
```
