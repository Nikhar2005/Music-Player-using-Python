import mysql.connector

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Replace with your MySQL server host
            user="root",       # Replace with your MySQL username
            password="",       # Replace with your MySQL password
            database="music_db"
        )
        print("Connected to the database successfully!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None