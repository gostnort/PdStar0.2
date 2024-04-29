import os
import argparse
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PySide6.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QTextEdit
from PySide6.QtWidgets import QHBoxLayout, QLabel, QRadioButton, QCheckBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from handle_pd import pd_properties
import functions

class MainWindow(QMainWindow):
    __BUTTON_WIDTH=100

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
        self.pd_radio = QRadioButton("PD*")
        self.dup_name_check=QCheckBox('Dup Names')
        self.dup_seats_check=QCheckBox('Dup Seats')
        self.default_radio = QRadioButton("Default")
        self.pick_window = QPushButton('Poke eTerm')
        self.pick_window.setFixedWidth(self.__BUTTON_WIDTH)
        self.pd_radio.setChecked(True)
        self.dup_name_check.setChecked(True)
        self.pn_times_label = QLabel('Times of \"PN1\"')
        self.pn_times_label.setFixedWidth(100)
        self.pn_times_edit = QLineEdit()
        self.pn_times_edit.setText('20')
        self.pn_times_edit.setFixedWidth(50)
        
        # Create button and QLineEdit for file path
        self.file_button = QPushButton("Open...")
        self.file_button.clicked.connect(self.open_file_dialog)

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
        self.run_button.setFixedWidth(self.__BUTTON_WIDTH)  # Set width to 100 pixels
        self.run_button.clicked.connect(lambda: self.run_logic(args))
        
        # Create a QHBoxLayout for the rows
        first_row_layout = QHBoxLayout()
        first_row_layout.addWidget(self.radio_label)
        second_row_layout = QHBoxLayout()
        second_row_layout.addWidget(self.pd_radio)
        second_row_layout.addWidget(self.default_radio)
        second_row_layout.addWidget(self.pick_window)
        third_row_layout = QHBoxLayout()
        third_row_layout.addWidget(self.dup_name_check)
        forth_row_layout = QHBoxLayout()  
        forth_row_layout.addWidget(self.dup_seats_check)
        fifth_row_layout = QHBoxLayout()
        fifth_row_layout.addWidget(self.pn_times_label)
        fifth_row_layout.addWidget(self.pn_times_edit)
        fifth_row_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sixth_row_layout = QHBoxLayout()
        sixth_row_layout.addWidget(self.file_button)
        sixth_row_layout.addWidget(self.file_path_edit)

        # Create a QVBoxLayout for the main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(first_row_layout)
        main_layout.addLayout(second_row_layout)
        main_layout.addLayout(third_row_layout)
        main_layout.addLayout(forth_row_layout)
        main_layout.addLayout(fifth_row_layout)
        main_layout.addLayout(sixth_row_layout)
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
        self.result_text_edit.clear()
        if args.debug:
            self.result_text_edit.append("Debug mode enabled")
        file_path = self.file_path_edit.text()
        pd_text=functions.ReadTxt2List(file_path)
        pd=pd_properties()
        pd.run(pd_text,self.dup_name_check.isChecked(),self.dup_seats_check.isChecked())
        if len(pd.ErrorMessage) != 0:
            for line in pd.ErrorMessage:
                self.result_text_edit.append(line)
        if args.debug:
            for line in pd.DebugMessage:
                self.result_text_edit.append(line)
        if self.dup_name_check.isChecked():
            if pd.bol_name:
                for line in pd.NameMessage:
                    self.result_text_edit.append(line)
        if self.dup_seats_check.isChecked():
            if pd.bol_seat:
                for line in pd.SeatMessage:
                    self.result_text_edit.append(line)

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