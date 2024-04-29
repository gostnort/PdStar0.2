import os
import argparse
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PySide6.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QTextEdit
from PySide6.QtWidgets import QHBoxLayout, QLabel, QRadioButton
from PySide6.QtGui import QIcon

class MainWindow(QMainWindow):

    def __init__(self, args):
        super().__init__()
        self.setWindowTitle("PD Start 0.1")
        self.resize(600, 400)  # Set initial window size to 600x400 pixels
        self.setMinimumSize(200, 200)  # Set minimum window size to 200x200 pixels
        
        # Set window icon
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "resources/pds.ico")
        self.setWindowIcon(QIcon(icon_path))

        # Set taskbar icon
        app_icon = QIcon(icon_path)
        self.setWindowIcon(app_icon)

        # Create a label and some radio buttons.
        self.radio_label = QLabel("Select a following function:")
        self.radio1 = QRadioButton("PD*")
        self.radio2 = QRadioButton("Default")
        self.pick_window = QPushButton('Pick')
        self.radio1.setChecked(True)
        
        # Create button and QLineEdit for file path
        self.button = QPushButton("Open...")
        self.button.clicked.connect(self.open_file_dialog)

        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        
        # Create QTextEdit for result output
        self.result_text_edit = QTextEdit()

        # Set font size of result_text_edit to 11pt
        font = self.result_text_edit.font()
        font.setPointSize(11)# default is 10pt.
        self.result_text_edit.setFont(font)

        # Create "Run" button
        self.run_button = QPushButton("Run")
        self.run_button.setFixedWidth(100)  # Set width to 100 pixels
        self.run_button.clicked.connect(lambda: self.run_logic(args))
        
        # Create a QHBoxLayout for the rows
        first_row_layout = QHBoxLayout()
        first_row_layout.addWidget(self.radio_label)
        first_row_layout.addWidget(self.radio1)
        first_row_layout.addWidget(self.radio2)
        first_row_layout.addWidget(self.pick_window)
        second_row_layout = QHBoxLayout()
        second_row_layout.addWidget(self.button)
        second_row_layout.addWidget(self.file_path_edit)

        # Create a QVBoxLayout for the main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(first_row_layout)
        main_layout.addLayout(second_row_layout)
        main_layout.addWidget(self.result_text_edit)
        main_layout.addWidget(self.run_button)
        
        # Create a central widget to hold the main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)")
        if file_path:
            self.file_path_edit.setText(file_path)

    def run_logic(self,args):
        return

def main():
    parser = argparse.ArgumentParser(description="PD start")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    # Create the application
    app = QApplication([])
    window = MainWindow(args)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()