import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select All Example")
        self.setGeometry(100, 100, 400, 200)

        # Create a QLineEdit widget
        self.flight_inout = QLineEdit(self)
        self.flight_inout.setText('123456789')
        self.flight_inout.setGeometry(50, 50, 300, 30)
        self.flight_inout.setObjectName("flight_in_out")

    def showEvent(self, event):
        super().showEvent(event)
        print('show event')
        self.flight_inout.selectAll()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
