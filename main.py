import random
from datetime import date, timedelta

import psycopg2
from faker import Faker
from psycopg2.extras import execute_values


DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "1"
DB_PORT = "5432"

ROWS_COUNT = 10_000

fake = Faker()


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )


def insert_clients(cursor):
    statuses = ["active", "inactive"]

    clients = []
    for _ in range(ROWS_COUNT):
        clients.append((
            fake.first_name(),
            fake.last_name(),
            random.choice(statuses)
        ))

    query = """
        INSERT INTO clients (first_name, last_name, status)
        VALUES %s
    """

    execute_values(cursor, query, clients)
    print(f"Inserted {ROWS_COUNT} rows into clients")


def insert_products(cursor):
    categories = ["Electronics", "Clothes", "Books", "Food", "Sport"]

    products = []
    for _ in range(ROWS_COUNT):
        products.append((
            fake.word().capitalize(),
            random.choice(categories),
            round(random.uniform(10, 1000), 2)
        ))

    query = """
        INSERT INTO products (product_name, category, price)
        VALUES %s
    """

    execute_values(cursor, query, products)
    print(f"Inserted {ROWS_COUNT} rows into products")


def insert_orders(cursor):
    start_date = date(2023, 1, 1)

    orders = []
    for _ in range(ROWS_COUNT):
        random_days = random.randint(0, 700)
        orders.append((
            random.randint(1, ROWS_COUNT),
            random.randint(1, ROWS_COUNT),
            start_date + timedelta(days=random_days),
            random.randint(1, 5)
        ))

    query = """
        INSERT INTO orders (client_id, product_id, order_date, quantity)
        VALUES %s
    """

    execute_values(cursor, query, orders)
    print(f"Inserted {ROWS_COUNT} rows into orders")


def main():
    connection = get_connection()
    cursor = connection.cursor()

    insert_clients(cursor)
    insert_products(cursor)
    insert_orders(cursor)

    connection.commit()

    cursor.close()
    connection.close()

    print("Data inserted successfully")


if __name__ == "__main__":
    main()