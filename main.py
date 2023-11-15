from random import random
import psycopg2
import random
from datetime import date, timedelta
# SQL statements to create tables
create_database_statement = "CREATE DATABASE masterdb;"

create_statements = {
    'content_repository': """
        CREATE TABLE IF NOT EXISTS content_repository (
            content_id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            genre VARCHAR(255),
            duration INTERVAL
        );
    """,
    'user_profiles': """
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255),
            email VARCHAR(255),
            subscription_status BOOLEAN
        );
    """,
    'streaming_metadata': """
        CREATE TABLE IF NOT EXISTS streaming_metadata (
            metadata_id SERIAL PRIMARY KEY,
            content_id INTEGER REFERENCES content_repository(content_id),
            bit_rates VARCHAR(255),
            server_locations VARCHAR(255),
            network_conditions VARCHAR(255)
        );
    """,
    'authentication': """
        CREATE TABLE IF NOT EXISTS authentication (
            user_id INTEGER REFERENCES user_profiles(user_id) PRIMARY KEY,
            credential VARCHAR(255),
            access_permission VARCHAR(255)
        );
    """,
    'geolocation': """
        CREATE TABLE IF NOT EXISTS geolocation (
            user_id INTEGER PRIMARY KEY REFERENCES user_profiles(user_id),
            user_geolocation_data VARCHAR(255),
            server_locations VARCHAR(255)
        );
    """,
    'billing': """
        CREATE TABLE IF NOT EXISTS billing (
            billing_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES user_profiles(user_id),
            payment_information VARCHAR(255),
            subscription_details VARCHAR(255)
        );
    """,
    'content_recommendations': """
        CREATE TABLE IF NOT EXISTS content_recommendations (
            recommendation_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES user_profiles(user_id),
            user_preferences VARCHAR(255),
            viewing_history INTEGER REFERENCES content_repository(content_id)
        );
    """,
    'user_preferences': """
        CREATE TABLE IF NOT EXISTS user_preferences (
            user_id INTEGER REFERENCES user_profiles(user_id),
            genre_pref VARCHAR(255),
            PRIMARY KEY (user_id, genre_pref)
        );
    """,
    'viewing_history': """
        CREATE TABLE IF NOT EXISTS viewing_history (
            user_id INTEGER REFERENCES user_profiles(user_id),
            content_id INTEGER REFERENCES content_repository(content_id),
            PRIMARY KEY (user_id, content_id)
        );
    """,
    'logging': """
        CREATE TABLE IF NOT EXISTS logging (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES user_profiles(user_id),
            system_metrics VARCHAR(255),
            gender VARCHAR(255),
            ip_address VARCHAR(255)
        );
    """,
    'server_locations': """
        CREATE TABLE IF NOT EXISTS server_locations (
            server_id SERIAL PRIMARY KEY,
            server_location VARCHAR(255)
        );
    """,
}

# Function to create tables in the database
def create_tables(connection_params):
    conn = None
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        for table, statement in create_statements.items():
            cursor.execute(statement)
        conn.commit()
        cursor.close()
    except Exception as error:
        print(f"Error: {error}")
        if conn is not None:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()

# Function to insert data into a specified table
def insert_data(connection_params, table_name, columns, values):
    conn = None
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in values])})"
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
    except Exception as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

# Function to delete data from a specified table based on a condition
def delete_data(connection_params, table_name, condition=None):
    conn = None
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        sql = f"DELETE FROM {table_name}"
        if condition:
            sql += f" WHERE {condition}"
        cursor.execute(sql)
        conn.commit()
        cursor.close()
    except Exception as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

# Function to delete all data from all tables
def delete_all_data(connection_params):
    conn = None
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        tables_in_order = [
            'logging', 'viewing_history', 'content_recommendations', 
            'billing', 'geolocation', 'authentication', 
            'streaming_metadata', 'user_profiles', 'content_repository'
        ]
        for table in tables_in_order:
            cursor.execute(f"DELETE FROM {table}")
        conn.commit()
        cursor.close()
    except Exception as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

# Function to create the database
def create_database(connection_params):
    conn = None
    try:
        # Connect to the default 'postgres' database to create a new database
        conn = psycopg2.connect(
            dbname='postgres',  # This should be 'postgres', not the new database name
            user=connection_params['user'],
            password=connection_params['password'],
            host=connection_params['host'],
            port=connection_params['port']
        )
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{connection_params['dbname']}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(create_database_statement)
            print(f"Database {connection_params['dbname']} created successfully.")
        else:
            print(f"Database {connection_params['dbname']} already exists.")
        cursor.close()
    except Exception as error:
        print(f"Error creating database: {error}")
    finally:
        if conn is not None:
            conn.close()

# Function to create tables in the new database
def create_tables(connection_params):
    conn = None
    try:
        # Connect to the new database to create tables
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        for table, statement in create_statements.items():
            cursor.execute(statement)
        conn.commit()
        cursor.close()
    except Exception as error:
        print(f"Error creating tables: {error}")
        if conn is not None:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()

# Connection parameters for the default 'postgres' database
default_connection_params = {
    'user': 'user',
    'password': 'password',
    'host': 'localhost',
    'port': '5440'
}

# Placeholder for connection parameters
connection_params = {
    'dbname': 'masterdb',
    'user': 'user',
    'password': 'password',
    'host': 'localhost',
    'port': '5440'
}


if __name__ == "__main__":
    create_database(default_connection_params)
    print("done database")
    create_tables(connection_params)
    print("done tables")