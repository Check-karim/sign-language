import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDesktopWidget, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import mysql.connector

class SignupWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sign Up")
        self.setFixedSize(400, 350)
        self.center()

        # Layout
        layout = QVBoxLayout()

        # Styling
        label_font = QFont("Arial", 10)
        input_font = QFont("Arial", 9)
        title_font = QFont("Arial", 16, QFont.Bold)

        # Title
        self.title_label = QLabel("Sign Language Interpreter")
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)

        # User Name
        self.user_id_label = QLabel("User Name")
        self.user_id_label.setFont(label_font)
        self.user_id_input = QLineEdit()
        self.user_id_input.setFont(input_font)
        self.user_id_input.setStyleSheet("padding: 5px; border-radius: 5px; border: 1px solid gray;")
        self.user_id_input.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Password
        self.password_label = QLabel("Password")
        self.password_label.setFont(label_font)
        self.password_input = QLineEdit()
        self.password_input.setFont(input_font)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 5px; border-radius: 5px; border: 1px solid gray;")
        self.password_input.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Confirm Password
        self.confirm_password_label = QLabel("Confirm Password")
        self.confirm_password_label.setFont(label_font)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setFont(input_font)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("padding: 5px; border-radius: 5px; border: 1px solid gray;")
        self.confirm_password_input.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Signup button
        self.signup_button = QPushButton("SIGN UP")
        self.signup_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.signup_button.setStyleSheet("""
            QPushButton {
                background-color: #5cb85c;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
            QPushButton:pressed {
                background-color: #398439;
            }
        """)
        self.signup_button.clicked.connect(self.signup)

        # Go Back to Homepage button
        self.homepage_button = QPushButton("Go Back to Homepage")
        self.homepage_button.setFont(QFont("Arial", 9))
        self.homepage_button.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
            QPushButton:pressed {
                background-color: #ac2925;
            }
        """)
        self.homepage_button.clicked.connect(self.open_homepage)

        # Already have an account? (Login button)
        self.login_button = QPushButton("Already have an account? Login")
        self.login_button.setFont(QFont("Arial", 9))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #0275d8;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #025aa5;
            }
            QPushButton:pressed {
                background-color: #01447e;
            }
        """)
        self.login_button.clicked.connect(self.open_login)

        # Adding widgets to layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.user_id_label)
        layout.addWidget(self.user_id_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.signup_button)
        layout.addWidget(self.login_button)
        layout.addWidget(self.homepage_button)

        # Reduce spacing
        layout.setSpacing(10)
        self.setLayout(layout)

    def center(self):
        """Centers the window on the screen."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def signup(self):
        username = self.user_id_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return

        # Connect to MySQL database
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # replace with your MySQL root password
                database="sign"  # replace with your database name
            )
            cursor = conn.cursor()

            # Check if the username is unique
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result:
                QMessageBox.warning(self, "Error", "Username already exists. Please choose another.")
                return

            # Insert the new user
            cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()

            QMessageBox.information(self, "Success", "User registered successfully")

            # Close the signup window and open the login window
            self.open_login()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def open_homepage(self):
        from homepage import Homepage
        self.homepage_window = Homepage()
        self.homepage_window.show()
        self.close()

    def open_login(self):
        from login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

# Define a global session variable to store the logged-in username
session = {"username": None}

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setFixedSize(400, 350)
        self.center()

        # Layout
        layout = QVBoxLayout()

        # Styling
        label_font = QFont("Arial", 10)
        input_font = QFont("Arial", 9)
        title_font = QFont("Arial", 16, QFont.Bold)

        # Title
        self.title_label = QLabel("Sign Language Interpreter")
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)

        # User ID
        self.user_id_label = QLabel("USER NAME")
        self.user_id_label.setFont(label_font)
        self.user_id_input = QLineEdit()
        self.user_id_input.setFont(input_font)
        self.user_id_input.setStyleSheet("padding: 5px; border-radius: 5px; border: 1px solid gray;")
        self.user_id_input.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Password
        self.password_label = QLabel("Password")
        self.password_label.setFont(label_font)
        self.password_input = QLineEdit()
        self.password_input.setFont(input_font)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 5px; border-radius: 5px; border: 1px solid gray;")
        self.password_input.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Login button
        self.login_button = QPushButton("LOGIN")
        self.login_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #5cb85c;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
            QPushButton:pressed {
                background-color: #398439;
            }
        """)
        self.login_button.clicked.connect(self.login)

        # Go Back to Homepage button
        self.homepage_button = QPushButton("Go Back to Homepage")
        self.homepage_button.setFont(QFont("Arial", 9))
        self.homepage_button.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
            QPushButton:pressed {
                background-color: #ac2925;
            }
        """)
        self.homepage_button.clicked.connect(self.open_homepage)

        # Sign Up button for users without an account
        self.signup_button = QPushButton("Don't have an account? Sign up")
        self.signup_button.setFont(QFont("Arial", 9))
        self.signup_button.setStyleSheet("""
            QPushButton {
                background-color: #0275d8;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #025aa5;
            }
            QPushButton:pressed {
                background-color: #01447e;
            }
        """)
        self.signup_button.clicked.connect(self.open_signup)

        # Adding widgets to layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.user_id_label)
        layout.addWidget(self.user_id_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.signup_button)
        layout.addWidget(self.homepage_button)

        # Reduce spacing
        layout.setSpacing(10)
        self.setLayout(layout)

    def center(self):
        """Centers the window on the screen."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login(self):
        username = self.user_id_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return

        # Connect to MySQL database
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # replace with your MySQL root password
                database="sign"  # replace with your database name
            )
            cursor = conn.cursor()

            # Check if the username and password match a record in the database
            cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()

            if result:
                # Store the username in session
                session["username"] = username

                QMessageBox.information(self, "Success", "Login successful!")
                self.open_user_dashboard(username)
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")
        finally:
            if conn:
                cursor.close()
                conn.close()

    def open_homepage(self):
        from homepage import Homepage
        self.homepage_window = Homepage()
        self.homepage_window.show()
        self.close()

    def open_signup(self):
        self.signup_window = SignupWindow()
        self.signup_window.show()
        self.close()

    def open_user_dashboard(self, username):
        from userDashboard import UserDashboard
        self.dashboard_window = UserDashboard(username)
        self.dashboard_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignupWindow()
    window.show()
    sys.exit(app.exec_())
