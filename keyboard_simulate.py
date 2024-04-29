import threading
from pynput.mouse import Listener, Button
from pynput.mouse import Controller as mouse_controller
from pynput.keyboard import Controller as key_controller
from pynput.keyboard import Key
import input_enter
import time
class ClickListener(threading.Thread):
    def __init__(self):
        super().__init__()
        self.click_position = None
        self.run()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.click_position = (x, y)
            return False  # Stop listener

    def run(self):
        with Listener(on_click=self.on_click) as listener:
            listener.join()

class SendKeys(threading.Thread):
    __COMMAND_SLEEP_TIME=0.75
    def __init__(self,command,position=None):
        super().__init__()
        self.keyboard = key_controller()
        self.mouse = mouse_controller()
        self.command=command
        self.position=position

    def __send_string_to_window(self):
        """
        Send a string to the window at the specified position.
        """
        if self.position:
            self.mouse.press(Button.left)
        self.keyboard.type(self.command)

    def __send_escape_keys(self):
        self.keyboard.press(Key.esc)
        self.keyboard.release(Key.esc)

    def send_print_keys(self):
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('p')
            self.keyboard.release('p')
        time.sleep(self.__COMMAND_SLEEP_TIME)

    def __send_num_enter(self):
        input_enter.PressKey(input_enter.ENTER,input_enter.INPUT_KEYBOARD,input_enter.KEYEVENTF_EXTENDEDKEY)
        time.sleep(0.1)
        input_enter.ReleaseKey(input_enter.ENTER,input_enter.INPUT_KEYBOARD)
        time.sleep(self.__COMMAND_SLEEP_TIME)

    def __send_f12_enter(self):
        self.keyboard.press(Key.f12)
        self.keyboard.release(Key.f12)

    def run(self):
        self.__send_escape_keys()
        self.__send_string_to_window()
        self.__send_num_enter()
        time.sleep(self.__COMMAND_SLEEP_TIME)

    def run_f12(self):
        self.__send_escape_keys()
        self.__send_string_to_window()
        self.__send_f12_enter()
        time.sleep(self.__COMMAND_SLEEP_TIME)

if __name__ == "__main__":
    # Start a separate thread to wait for left click event
    click_listener = ClickListener()
    #print(f"Left click detected at position: {click_listener.click_position}")
    for i in range(1,5):
        command_thread=SendKeys('PN1')
        command_thread.start()
        command_thread.join()
        command_thread.send_print_keys()
        
