import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QDesktopWidget
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt


class Homepage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sign Language Interpreter")
        self.setFixedSize(600, 400)
        self.center()

        # Set background color
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#f0f8ff"))  # Light blue background
        self.setPalette(palette)

        # Layout
        layout = QVBoxLayout()

        # Styling for text
        title_font = QFont("Arial", 20, QFont.Bold)
        info_font = QFont("Arial", 12)

        # Title Label
        title_label = QLabel("Sign Language Interpreter")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)

        # Information Label
        info_label = QLabel(
            "Welcome to the Sign Language Interpreter app.\nThis app helps translate sign language into text for better communication.")
        info_label.setFont(info_font)
        info_label.setAlignment(Qt.AlignCenter)

        # Get Started Button
        self.get_started_button = QPushButton("Get Started")
        self.get_started_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.get_started_button.setStyleSheet("""
            QPushButton {
                background-color: #5cb85c;
                color: white;
                padding: 15px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
            QPushButton:pressed {
                background-color: #398439;
            }
        """)
        self.get_started_button.clicked.connect(self.open_login)

        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(info_label)
        layout.addWidget(self.get_started_button)

        # Reduce spacing and add padding
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(layout)

    def center(self):
        """Centers the window on the screen."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_login(self):
        from login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Homepage()
    window.show()
    sys.exit(app.exec_())
