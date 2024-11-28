import sqlite3;
import bcrypt;
def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
def insert_user(username, password_hash, email, first_name, last_name):
    database = 'my_database.db'  
    
    try:
        hashed_password = hash_password(password_hash)
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        collection_id=1
        #imagepath="C:\Users\DenitsaD\OneDrive - Copaco DC B.V\Bureaublad\work\marian\printing_app\venv\images\account.jpeg"
        insert_sql = """
        INSERT INTO Users (Username, PasswordHash, Email, FirstName, LastName)
        VALUES (?, ?, ?, ?, ?);
        """
       
        #cursor.execute("INSERT INTO Collections (Name) VALUES (?)", ("Collection 3",))


       # cursor.execute("INSERT INTO Images (ImagePath, CollectionID) VALUES (?, ?)", (imagepath, collection_id))

        
        cursor.execute(insert_sql, (username, hashed_password, email, first_name, last_name))
        connection.commit()
        print("User inserted successfully.")
        
    except Exception as e:
        print(f"Error inserting user: {e}")
    finally:
        
        connection.close()


insert_user("user1", "user1", "user@gmail.com", "Denitsa", "Draganova")
