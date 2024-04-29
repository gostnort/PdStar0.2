import threading
from pynput.mouse import Listener, Button
from pynput.mouse import Controller as mouse_controller
from pynput.keyboard import Controller as key_controller
from pynput.keyboard import Key
import input_enter

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

class SendKeys():
    keyboard=key_controller()
    mouse=mouse_controller()

    def send_string_to_window(self,string, position=None):
        """
        Send a string to the window at the specified position.
        """
        if position:
            self.mouse.press(Button.left)
        self.keyboard.type(string)

    def send_print_keys(self):
        with self.keyboard.pressed(Key.shift):
            self.keyboard.press('9')
            self.keyboard.release('9')
        print('ctrl+9')

    def send_num_enter(self):
        input_enter.PressKey(input_enter.ENTER,input_enter.INPUT_KEYBOARD,input_enter.KEYEVENTF_EXTENDEDKEY)
        input_enter.ReleaseKey(input_enter.ENTER,input_enter.INPUT_KEYBOARD)

if __name__ == "__main__":
    # Start your application here
    
    # Start a separate thread to wait for left click event
    click_listener = ClickListener()

    # If a click was detected, send 'PN1' to the window at the clicked position
    print(f"Left click detected at position: {click_listener.click_position}")
    op=SendKeys()
    op.send_string_to_window('hello world')
    op.send_print_keys()
    op.send_num_enter()
