"""
Database migration script to add password_hash column to users table
Run this script once to update your existing database schema
"""
import sqlite3
import os

# Get the database path
db_path = '/media/server/SQL_ALCHEMY_AND_FLUSK/instance/app.db'

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    print("No migration needed - database will be created with correct schema on first run")
    exit(0)

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if password_hash column already exists
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'password_hash' in columns:
        print("✓ password_hash column already exists - no migration needed")
    else:
        print("Adding password_hash column to users table...")

        # Add the password_hash column
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash VARCHAR(256)")

        # Check if there are existing users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        if user_count > 0:
            print(f"⚠ Warning: Found {user_count} existing users without passwords")
            print("  These users will need to be deleted or have passwords set manually")
            print("  You may want to back up user data before proceeding")

        conn.commit()
        print("✓ Migration completed successfully!")
        print("\nNext steps:")
        print("1. Install required packages: pip install flask flask-sqlalchemy")
        print("2. Run the Flask app: python index.py")

except sqlite3.Error as e:
    print(f"✗ Migration failed: {e}")
    conn.rollback()
finally:
    conn.close()
