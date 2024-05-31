import threading
from pynput.mouse import Listener
from pynput.mouse import Controller as mouse_controller
from pynput.keyboard import Controller as key_controller
from pynput.keyboard import Key
import input_enter as input_enter
import time
class ClickListener(threading.Thread):
    def __init__(self,event):
        super().__init__()
        self.click_position = None
        self.event = event

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.click_position = (x, y)
            self.event.set()  # Set the event to notify the main thread
            return False  # Stop listener

    def run(self):
        with Listener(on_click=self.on_click) as listener:
            listener.join()

class SendKeys(threading.Thread):
    def __init__(self,command,pending):
        super().__init__()
        self.keyboard = key_controller()
        self.mouse = mouse_controller()
        self.COMMAND=command
        self.COMMAND_SLEEP_TIME=pending

    def __send_escape_keys(self):
        self.keyboard.press(Key.esc)
        self.keyboard.release(Key.esc)

    def send_print_keys(self):
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('p')
            self.keyboard.release('p')
        time.sleep(self.COMMAND_SLEEP_TIME)

    def send_clear_screen(self):
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('a')
            self.keyboard.release('a')
        time.sleep(self.COMMAND_SLEEP_TIME)

    def __send_num_enter(self):
        input_enter.PressKey(input_enter.ENTER,input_enter.INPUT_KEYBOARD,input_enter.KEYEVENTF_EXTENDEDKEY)
        time.sleep(0.1)
        input_enter.ReleaseKey(input_enter.ENTER,input_enter.INPUT_KEYBOARD)
        time.sleep(self.COMMAND_SLEEP_TIME)

    def __send_f12_enter(self):
        self.keyboard.press(Key.f12)
        self.keyboard.release(Key.f12)

    def run(self):
        self.__send_escape_keys()
        self.keyboard.type(self.COMMAND)
        self.__send_num_enter()
        time.sleep(self.COMMAND_SLEEP_TIME)

    def run_f12(self):
        self.__send_escape_keys()
        self.keyboard.type(self.COMMAND)
        self.__send_f12_enter()
        time.sleep(self.COMMAND_SLEEP_TIME)

if __name__ == "__main__":
    # Create separate event objects for each listener
    event1 = threading.Event()
    event2 = threading.Event()
    # Start the first listener
    click_listener1 = ClickListener(event1)
    click_listener1.start()
    # Wait for the first click event
    event1.wait()
    print(f"Left click detected at position: {click_listener1.click_position}")
    # Start the second listener
    click_listener2 = ClickListener(event2)
    click_listener2.start()
    for i in range(1,5):
        if click_listener2.click_position == None:
            command_thread=SendKeys('PN1')
            command_thread.start()
            command_thread.join()
            #command_thread.send_print_keys()
        else:
            event2.wait()
            print("The mouse click again at: ", click_listener2.click_position)
            click_listener2.join()
            click_listener2.event.clear()
            break
        
    
    
        
