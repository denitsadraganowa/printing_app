import sqlite3

def create_users_table():
    # Define your SQLite database file path (this creates a new SQLite DB if it doesn't exist)
    database = 'my_database.db'  # Use your database file name or path
    
    try:
        # Connect to the SQLite database (it will create the DB if it doesn't exist)
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        # SQL statement to create the Users table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS Users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL UNIQUE,
            PasswordHash TEXT NOT NULL,
            Email TEXT,
            FirstName TEXT,
            LastName TEXT,
            CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
            UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """

        # Execute the SQL command
        cursor.execute(create_table_sql)
        connection.commit()
        print("Users table created successfully.")
    except Exception as e:
        print(f"Error creating Users table: {e}")
    finally:
        # Close the connection
        connection.close()

def create_collections_table():
    # Define your SQLite database file path (this creates a new SQLite DB if it doesn't exist)
    database = 'my_database.db'  # Use your database file name or path
    
    try:
        # Connect to the SQLite database (it will create the DB if it doesn't exist)
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        # SQL statement to create the Collections table
        create_collections_table_sql = """
        CREATE TABLE IF NOT EXISTS Collections (
            CollectionID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL UNIQUE
        );
        """

        # Execute the SQL command
        cursor.execute(create_collections_table_sql)
        connection.commit()
        print("Collections table created successfully.")
    except Exception as e:
        print(f"Error creating Collections table: {e}")
    finally:
        # Close the connection
        connection.close()

def create_images_table():
    # Define your SQLite database file path (this creates a new SQLite DB if it doesn't exist)
    database = 'my_database.db'  # Use your database file name or path
    
    try:
        # Connect to the SQLite database (it will create the DB if it doesn't exist)
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        # SQL statement to create the Images table
        create_images_table_sql = """
        CREATE TABLE IF NOT EXISTS Images (
            ImageID INTEGER PRIMARY KEY AUTOINCREMENT,
            ImagePath TEXT NOT NULL,
            CollectionID INTEGER,
            FOREIGN KEY (CollectionID) REFERENCES Collections (CollectionID)
        );
        """

        # Execute the SQL command
        cursor.execute(create_images_table_sql)
        connection.commit()
        print("Images table created successfully.")
    except Exception as e:
        print(f"Error creating Images table: {e}")
    finally:
        # Close the connection
        connection.close()

def create_all_tables():
    # Create all tables
   
    create_collections_table()
    create_images_table()

# Call the function to create all tables
create_all_tables()
