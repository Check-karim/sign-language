import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDesktopWidget, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import mysql.connector

class UserDashboard(QWidget):
    def __init__(self, username):
        super().__init__()

        self.username = username

        self.setWindowTitle("User Dashboard")
        self.setFixedSize(400, 350)
        self.center()

        # Layout
        layout = QVBoxLayout()

        # Styling
        title_font = QFont("Arial", 16, QFont.Bold)

        # Welcome message
        self.welcome_label = QLabel(f"Welcome, {username}!")
        self.welcome_label.setFont(title_font)
        self.welcome_label.setAlignment(Qt.AlignCenter)

        # Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
            QPushButton:pressed {
                background-color: #ac2925;
            }
        """)
        self.logout_button.clicked.connect(self.logout)

        # Adding widgets to layout
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.logout_button)

        # Reduce spacing
        layout.setSpacing(10)
        self.setLayout(layout)

    def center(self):
        """Centers the window on the screen."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def logout(self):
        username = None  # Clear the session
        self.open_login()

    def open_login(self):
        from login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
