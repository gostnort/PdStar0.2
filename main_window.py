import os
import argparse
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PySide6.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QTextEdit
from PySide6.QtWidgets import QHBoxLayout, QLabel, QRadioButton, QCheckBox
from PySide6.QtWidgets import QFrame, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from bins.handle_pd import pd_properties
import bins.functions as functions
import bins.keyboard_simulate as keyboard_simulate
import threading
import json

class MainWindow(QMainWindow):
    __BUTTON_WIDTH=100

    def __init__(self, args):
        super().__init__()
        venv_path=os.path.dirname(os.getcwd())
        '''
        if(r'.venv' not in venv_path):
            print(venv_path)
            print('Run this project in virtual environment folder \'.venv\'')
            QMessageBox.warning(self,'Warning', 
                                venv_path + "\nThis project msut run in the virtual environment that named the folder \'.venv\' \nStart the python.exe in \'Scripts\' folder calling of this main_window.")
            return
            '''
        root_path=os.getcwd()
        resource_path = root_path + r'\resources'

        with open(resource_path + r"\main_window.json", "r") as file:
            config = json.load(file)
        self.setWindowTitle(config['window_title'])
        self.resize(config['main_window_width'], config['main_window_height'])  # Set initial window size to 600x400 pixels
        self.setMinimumSize(config['main_window_min_width'], config['main_window_min_height'])  # Set minimum window size to 200x200 pixels
        
        # Set window icon
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "resources/pds.ico")
        self.setWindowIcon(QIcon(icon_path))

        # Set taskbar icon
        app_icon = QIcon(icon_path)
        self.setWindowIcon(app_icon)

        # Create a label and some radio buttons.
        self.radio_label = QLabel("Select a following function:")
        self.pd_radio = QRadioButton("PD")
        self.pd_text=QLineEdit("*")
        self.pd_text.setStyleSheet("border: none;")
        self.pending_time_text=QLineEdit(str(config['pending_time_value']))
        self.pending_time_text.setFixedWidth(config['QLineEdit_short_width'])
        self.pending_time_text.setStyleSheet("QLineEdit { background-color: #CCCCCC; color: #444444; border:none;}")
        self.dup_name_check=QCheckBox('Dup Names')
        self.dup_seats_check=QCheckBox('Dup Seats')
        self.default_radio = QRadioButton("Default")
        self.flight_inout=QLineEdit("984")
        self.flight_inout.setFixedWidth(config['QLineEdit_short_width'])
        self.flight_inout.setStyleSheet("border: none;")
        self.pd_radio.setChecked(True)
        self.dup_name_check.setChecked(True)
        self.pn_times_label = QLabel('Times of \'>PN1⏎\'')
        #self.pn_times_label.setFixedWidth(100)
        self.pn_times_edit = QLineEdit()
        self.pn_times_edit.setText(str(config['pn_times_value']))
        self.pn_times_edit.setFixedWidth(config['QLineEdit_short_width'])
        self.pn_times_edit.setStyleSheet("border: none;")
        
        # Create button and QLineEdit for file path
        self.file_button = QPushButton("Open...")
        self.file_button.clicked.connect(self.open_file_dialog)

        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        self.file_path_edit.setStyleSheet("border: none;")
        
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
        
        # Create 'Pick' button.
        self.pick_button = QPushButton('Poke eTerm')
        self.pick_button.setFixedWidth(self.__BUTTON_WIDTH)
        self.pick_button.clicked.connect(lambda:self.pick_logic())

        # Create a QHBoxLayout for the rows
        first_row_layout = QHBoxLayout()
        first_row_layout.addWidget(self.radio_label)
        
        second_row_layout = QHBoxLayout()
        second_row_layout.addWidget(self.pd_radio)
        second_row_layout.addWidget(self.pd_text)
        second_row_layout.addWidget(self.pn_times_label)
        second_row_layout.addWidget(self.pn_times_edit)
        
        third_row_layout = QHBoxLayout()      
        third_row_left=QHBoxLayout()
        third_row_left.addWidget(self.default_radio)
        third_row_left.addWidget(self.flight_inout)
        third_row_left.addStretch()# Add stretch to push widgets to the left
        third_row_left.setAlignment(Qt.AlignmentFlag.AlignLeft)
        third_row_layout.addLayout(third_row_left)

        third_row_right=QHBoxLayout()
        third_row_right.addWidget(self.pending_time_text)
        third_row_right.addWidget(self.pick_button)
        third_row_right.setAlignment(Qt.AlignmentFlag.AlignRight)
        third_row_layout.addLayout(third_row_right)

        forth_row_layout = QHBoxLayout()
        forth_row_layout.addWidget(self.file_button)
        forth_row_layout.addWidget(self.file_path_edit)

        fifth_row_layout=QHBoxLayout()
        fifth_row_layout.addWidget(self.dup_name_check)
        fifth_row_layout.addWidget(self.dup_seats_check)
        fifth_row_layout.addWidget(self.run_button)
        fifth_row_layout.addStretch()

        # Create a QVBoxLayout for the main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(first_row_layout)
        main_layout.addLayout(second_row_layout)
        main_layout.addLayout(third_row_layout)
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        main_layout.addLayout(forth_row_layout)
        main_layout.addLayout(fifth_row_layout)
        main_layout.addWidget(self.result_text_edit)
        
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
        pd.GetConflict(pd_text,self.dup_name_check.isChecked(),self.dup_seats_check.isChecked())
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

    def pick_logic(self):
        command_pending=float(self.pending_time_text.text())
        try:
            times=int(self.pn_times_edit.text())+1
        except ValueError:
            return
        if self.pd_radio.isChecked:
            event1=threading.Event()
            event2=threading.Event()
            listener_start=keyboard_simulate.ClickListener(event1)
            listener_start.start()
            # Wait for the first click event
            event1.wait()
            command_string=('PD'+self.pd_text.text())
            PD_thread=keyboard_simulate.SendKeys(command_string,command_pending)
            PD_thread.start()
            PD_thread.join()
            #PD_thread.send_print_keys()
            listener_loop = keyboard_simulate.ClickListener(event2)
            listener_loop.start()
            for i in range(1,times):
                if listener_loop.click_position == None:
                    PN1_thread=keyboard_simulate.SendKeys('PN1',command_pending)
                    PN1_thread.start()
                    PN1_thread.join()
                    #PN1_thread.send_print_keys()
                else:
                    event2.wait()
                    listener_loop.join()
                    listener_loop.event.clear()
                    break
            
        
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