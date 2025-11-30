import mysql.connector
from database import engine

# Connect to MySQL directly to add missing columns
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sohan@9761",
    database="college_db"
)
cursor = conn.cursor()

try:
    # Check if the table exists
    cursor.execute("SHOW TABLES LIKE 'users'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        print("Users table exists, checking columns...")
        
        # Check existing columns
        cursor.execute("DESCRIBE users")
        columns = [column[0] for column in cursor.fetchall()]
        print(f"Existing columns: {columns}")
        
        # Add missing columns if they don't exist
        if 'is_active' not in columns:
            print("Adding 'is_active' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE")
            print("✓ Added 'is_active' column")
        
        if 'created_at' not in columns:
            print("Adding 'created_at' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("✓ Added 'created_at' column")
        
        if 'updated_at' not in columns:
            print("Adding 'updated_at' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP")
            print("✓ Added 'updated_at' column")
        
        conn.commit()
        print("✅ Users table updated successfully!")
        
        # Show final table structure
        cursor.execute("DESCRIBE users")
        final_columns = cursor.fetchall()
        print("\nFinal table structure:")
        for column in final_columns:
            print(f"  - {column[0]} ({column[1]})")
    else:
        print("Users table doesn't exist. Creating it...")
        # Create table directly with SQL
        create_table_sql = """
        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_email (email)
        )
        """
        cursor.execute(create_table_sql)
        conn.commit()
        print("✅ Users table created successfully!")

except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
