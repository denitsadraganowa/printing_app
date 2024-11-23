import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from firstpage import MainWindow  # Assuming MainWindow is defined in firstpage.py

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login - MV | Printing Software")
        self.setGeometry(400, 200, 400, 300)  # Set the size and position of the login window
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Please Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        # Username field
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("padding: 10px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Password field
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide the password input
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setStyleSheet("padding: 10px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("Login", self)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        """Check the credentials and open the main app if correct."""
        username = self.username_input.text()
        password = self.password_input.text()

        # Hardcoded correct credentials for demo purposes
        correct_username = "admin"
        correct_password = "password123"

        if username == correct_username and password == correct_password:
            # Successful login, open the main window
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()  # Close the login window after success
        else:
            # Login failed, show error message
            QMessageBox.critical(self, "Login Failed", "Invalid username or password. Please try again.")


# Main app logic
# Main app logic
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Debug: Check if login window is created properly
    print("Showing LoginWindow...")  # Debug line
    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())

