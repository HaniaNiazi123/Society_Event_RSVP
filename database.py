import sqlite3
import os


def create_database():
    base_folder = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(base_folder, "events.db")

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            location TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rsvps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            student_name TEXT NOT NULL,
            email TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
    """)

    connection.commit()
    connection.close()

    print("Database and tables created successfully!")


if __name__ == "__main__":
    create_database()