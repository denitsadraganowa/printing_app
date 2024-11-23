import sys
from PyQt5.QtWidgets import QApplication,QFileDialog,QGridLayout,QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QMainWindow, QStackedWidget, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from main import ImageGridApp
from PyQt5.QtCore import QSize

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sqlite3
import msal
import pyodbc
import bcrypt
def connect_to_database():
    try:
        connection = sqlite3.connect('my_database.db')  # SQLite database file
        print("Connection successful!")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

import sqlite3
class LoginWindow(QWidget):
    
    
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - MV | Printing Software")
        self.setGeometry(150, 150, 1200, 900)
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout()
        
       

        title = QLabel("Log in")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.setAlignment(Qt.AlignCenter)
        

        
        
      
        

        
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter your username")
        
        layout.addWidget(self.username_input)
     
       
        self.password_label = QLineEdit(self)
        self.password_label.setEchoMode(QLineEdit.Password)
        self.password_label.setPlaceholderText("Enter your password")
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_label)




        #self.password_label = QLabel("Password:")
        #self.password_input = QLineEdit(self)
        #self.password_input.setEchoMode(QLineEdit.Password)
        #self.password_input.setPlaceholderText("Enter your password")
        
       
        self.login_button = QPushButton("Log in", self)
         # Replace with the actual path
        self.login_button.setFixedHeight(40)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        
        self.setStyleSheet("""
            QWidget {
                background-color: #01589f;
            }
            QLabel {
                width:40px;
                font-size: 32px;
                color: #ffffff;
                margin-bottom: 20px;
            }
            QLineEdit {
                font-size: 18px;
                background-color: white;
                color: black;
                border-radius: 20px;
                padding: 10px;
                margin: 10px 20px;
            }
           
        """)
        

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_label.text()

        
        connection = connect_to_database()
        if not connection:
            QMessageBox.critical(self, "Database Error", "Failed to connect to the database.")
            return

       
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT PasswordHash FROM Users WHERE Username = ?", (username,))
            result = cursor.fetchone()

            if result:
                hashed_password = result[0]

                # Compare hashed passwords using bcrypt
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    self.main_window = MainWindow(username)
                    self.main_window.show()
                    self.close()
                else:
                    QMessageBox.critical(self, "Login Failed", "Invalid username or password.")
            else:
                QMessageBox.critical(self, "Login Failed", "Invalid username or password.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        finally:
            connection.close()
def load_collections_from_db(database_path):
    collections = []
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        # Fetch CollectionID and Name from the Collections table
        cursor.execute("SELECT CollectionID, Name FROM Collections")
        collections_data = cursor.fetchall()

        # Iterate over the fetched collections
        for collection_id, collection_name in collections_data:
            collection = {"id": collection_id, "name": collection_name, "images": []}

            # Fetch the images for the collection
            cursor.execute("SELECT ImagePath FROM Images WHERE CollectionID = ?", (collection_id,))
            images_data = cursor.fetchall()

            for (image_path,) in images_data:  
                collection["images"].append({
                    "path": image_path,
                })

            collections.append(collection)

    except Exception as e:
        print(f"Error loading collections: {e}")
    finally:
        if connection:
            connection.close()

    return collections


collections = load_collections_from_db("my_database.db")


class CollectionButton(QPushButton):
    def __init__(self, collection, image_collections, parent=None):
        super().__init__(collection['name'], parent)
        self.setGeometry(1000, 1000, 1000, 8000)
        self.collection_name = collection['name']
        self.image_collections = image_collections
        self.collection_id = collection['id']
        
        if collection['images']:
           
            pixmap = QPixmap(collection['images'][0]["path"])
            self.setIcon(QIcon(pixmap))
            self.setIconSize(pixmap.rect().size())

       
        self.setFixedSize(300, 300)
        self.setStyleSheet("""
            QPushButton {
                background-color:white;
                color: black;
                font-size: 16px;
                font-weight: bold;
                border-radius: 15px;
                border: 2px solid #01589f;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
            QPushButton:pressed {
                background-color: #e8e8e8;
            }
        """)

        self.clicked.connect(self.open_collection_screen)
        delete_button = QPushButton("Delete", self)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #be3228;
                color: white;
                font-size: 12px;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        delete_button.setGeometry(200, 250, 80, 40)  # Position it below the main button
        delete_button.clicked.connect(self.delete_collection)

    def delete_collection(self):
        """
        Delete the collection from the database and remove the button from the UI.
        """
        try:
            connection = connect_to_database()
            cursor = connection.cursor()

            print(self.collection_id)
            cursor.execute("DELETE FROM Images WHERE CollectionID = ?", (self.collection_id,))
           
            cursor.execute("DELETE FROM Collections WHERE CollectionID = ?", (self.collection_id,))
            connection.commit()

           
            self.deleteLater()

            QMessageBox.information(self, "Success", "Collection deleted successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while deleting the collection: {e}")
        finally:
            if connection:
                connection.close()

    def open_collection_screen(self):
    # Retrieve the collection data based on the selected collection name
     collection_data = next((col for col in self.image_collections if col['name'] == self.collection_name), None)
     if collection_data:
        # Pass both the images and the Collection ID to the ImageGridApp
        collection_screen = ImageGridApp(collection_data["images"])
        collection_screen.show()



class AdminUsersWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("All Users - Admin View")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout(self)

        title = QLabel("All Registered Users")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        try:
            connection = connect_to_database()
            cursor = connection.cursor()

            # Fetch all user data
            cursor.execute("SELECT Username, FirstName, LastName, CreatedAt FROM Users")
            users = cursor.fetchall()

            # Display user data
            for user in users:
                user_label = QLabel(f"Username: {user[0]} | First name: {user[1]} | Last name: {user[2]} | Created at: {user[3]}")
                user_label.setStyleSheet("font-size: 14px; margin: 5px 0;")
                layout.addWidget(user_label)
        except Exception as e:
            error_label = QLabel(f"Error loading users: {e}")
            error_label.setStyleSheet("color: red; font-size: 14px;")
            layout.addWidget(error_label)
        finally:
            if connection:
                connection.close()

class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("MV | Printing Software")
        self.setGeometry(100, 100, 1200, 800)  # Set a larger default window size


        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.stacked_widget = QStackedWidget(self)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.stacked_widget)
        logout_button = QPushButton(self)
        logout_button.setIcon(QIcon("images/logout.jpeg"))  # Replace with the path to your icon file
        logout_button.setIconSize(QSize(32, 32))  # Adjust the size of the icon
        logout_button.setStyleSheet("""
    QPushButton {
        background-color: white;
        border-radius: 15px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: black;
    }
""")
        logout_button.clicked.connect(self.handle_logout)  # Connect to the logout handler
        if self.username == "admin1":
            admin_button = QPushButton("View All Users", self)
            admin_button.setStyleSheet("""
                QPushButton {
                    background-color: #be3228;
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #ff9800;
                }
            """)
            admin_button.clicked.connect(self.open_admin_window)
            self.central_layout.addWidget(admin_button)

        
        
        self.init_collection_screen()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #01589f;
            }
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 20px;
                text-align: center;
            }
            QVBoxLayout, QHBoxLayout {
                margin: 0;
                padding: 0;
            }
            QScrollArea {
                background-color: #ffffff;
                border-radius: 10px;
                padding: 10px;
            }
        """)
    def open_admin_window(self):
        """
        Open a new window showing all user information.
        """
        self.admin_window = AdminUsersWindow()
        self.admin_window.show()

    def handle_logout(self):
        """
        Handle logout by closing the MainWindow and showing the LoginWindow.
        """
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
    
    def init_collection_screen(self):
     collection_screen = QWidget()
     layout = QVBoxLayout()

     title = QLabel("Collections")
     title.setAlignment(Qt.AlignCenter)
     layout.addWidget(title)

     new_collection_button = QPushButton("Create New Collection", self)
     new_collection_button.setStyleSheet("""
        QPushButton {
            background-color: #be3228;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #be3228;
        }
    """)
     new_collection_button.clicked.connect(self.create_new_collection)
     layout.addWidget(new_collection_button)

     scroll_area = QScrollArea(self)
     scroll_area.setWidgetResizable(True)  # Enable resizing
     scroll_widget = QWidget()
     grid_layout = QGridLayout(scroll_widget)  # Create a grid layout
     grid_layout.setSpacing(20)  # Set spacing between buttons
     grid_layout.setContentsMargins(10, 10, 10, 10)  # Add margins for aesthetics

     # Dynamically add collection buttons to the grid
     for i, collection in enumerate(collections):
        collection_button = CollectionButton(collection, collections)
        row, col = divmod(i, 3)  # Calculate row and column indices for 3 columns
        grid_layout.addWidget(collection_button, row, col)

     scroll_widget.setLayout(grid_layout)
     scroll_area.setWidget(scroll_widget)
     layout.addWidget(scroll_area)

     collection_screen.setLayout(layout)
     self.stacked_widget.addWidget(collection_screen)

    def create_new_collection(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Create New Collection")
        dialog.setGeometry(150, 150, 400, 300)
        dialog_layout = QVBoxLayout(dialog)

        name_input = QLineEdit(dialog)
        name_input.setPlaceholderText("Enter collection name")
        dialog_layout.addWidget(name_input)

        select_images_button = QPushButton("Add Images", dialog)
        selected_images = []

        def select_images():
            images, _ = QFileDialog.getOpenFileNames(
                self, "Select Images", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
            )
            if images:
                selected_images.extend(images)

        select_images_button.clicked.connect(select_images)
        dialog_layout.addWidget(select_images_button)

        create_button = QPushButton("Create Collection", dialog)

        def create_collection():
            collection_name = name_input.text().strip()
            if collection_name:
                # Save to database
                try:
                    connection = connect_to_database()
                    cursor = connection.cursor()

                    # Insert collection
                    cursor.execute("INSERT INTO Collections (Name) VALUES (?)", (collection_name,))
                    connection.commit()
                    collection_id = cursor.lastrowid

                   
                    for image_path in selected_images:
                        cursor.execute("INSERT INTO Images (CollectionID, ImagePath) VALUES (?, ?)",
                                       (collection_id, image_path))
                    connection.commit()

                  
                    global collections
                    collections = load_collections_from_db("my_database.db")
                    self.init_collection_screen()
                    QMessageBox.information(self, "Success", "New collection created successfully.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred: {e}")
                finally:
                    connection.close()
                dialog.accept()
            else:
                QMessageBox.warning(self, "Input Error", "Please enter a collection name.")

        create_button.clicked.connect(create_collection)
        dialog_layout.addWidget(create_button)

        dialog.exec_()
    def show_collection_screen(self, collection_screen):
        self.stacked_widget.addWidget(collection_screen)
        self.stacked_widget.setCurrentWidget(collection_screen)




if __name__ == "__main__":
    app = QApplication(sys.argv)

   
    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())
