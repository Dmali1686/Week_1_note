import os
import psycopg2
from psycopg2 import sql

# Get DB credentials from environment variables or use default
DB_NAME = os.getenv("DB_NAME", "postgres") # Usually default database is postgres
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")

# Function to get database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST
        )
        return conn
    except Exception as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        print("Please ensure PostgreSQL is running and credentials are correct.")
        return None

# Initialize database table
def init_db():
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL
                )
            ''')
        conn.commit()
        conn.close()

# Initialize DB on startup
init_db()

while True:
    print("\n")
    print("=== My PostgreSQL Notes App ===")
    print("1. Add a note")
    print("2. View all notes")
    print("3. Exit")
    
    choice = input("Choose an option (1, 2, or 3): ")

    if choice == "1":
        new_note = input("Enter your note: ")
        
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                # Basic SQL INSERT query
                cur.execute("INSERT INTO notes (content) VALUES (%s)", (new_note,))
            conn.commit()
            conn.close()
            print("✅ Note saved successfully to PostgreSQL!")

    elif choice == "2":
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                # Basic SQL SELECT query
                cur.execute("SELECT id, content FROM notes")
                saved_notes = cur.fetchall()
            conn.close()
            
            if saved_notes:
                print("\n--- Your Saved Notes ---")
                for note_id, content in saved_notes:
                    print(f"[{note_id}] {content}")
                print("------------------------")
            else:
                print("❌ No notes found. Try adding one first!")

    elif choice == "3":
        print("Goodbye! Your notes are safely stored in PostgreSQL.")
        break

    else:
        print("❌ Invalid choice. Please try again.")
