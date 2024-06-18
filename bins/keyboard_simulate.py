import threading
from pynput.mouse import Listener
from pynput.mouse import Controller as mouse_controller
from pynput.keyboard import Controller as key_controller
from pynput.keyboard import Key
from pynput.mouse import Button
import input_enter as input_enter
import time
class ClickListener(threading.Thread):
    def __init__(self,event):
        super().__init__()
        self.click_position = None
        self.event = event
        self.listener = Listener(on_click=self.on_click)

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.click_position = (x, y)
            self.event.set()  # Set the event to notify the main thread
            return False  # Stop listener

    def run(self):
        with Listener(on_click=self.on_click) as listener:
            listener.join()

    def stop(self):
        self.listener.stop()

    def left_click(self):
        mouse_controller().click(Button.left,1)
        return self.click_position

class SendKeys(threading.Thread):
    def __init__(self):
        super().__init__()
        self.keyboard = key_controller()
        self.mouse = mouse_controller()

    def __send_escape_keys(self):
        self.keyboard.press(Key.esc)
        self.keyboard.release(Key.esc)

    def send_print_keys(self,SleepTime=0):
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('p')
            self.keyboard.release('p')
        time.sleep(SleepTime)
        
    def send_clear_screen(self,SleepTime=0):
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('a')
            self.keyboard.release('a')
        time.sleep(SleepTime)

    def __send_num_enter(self):
        input_enter.PressKey(input_enter.ENTER,input_enter.INPUT_KEYBOARD,input_enter.KEYEVENTF_EXTENDEDKEY)
        time.sleep(0.1)
        input_enter.ReleaseKey(input_enter.ENTER,input_enter.INPUT_KEYBOARD)
        time.sleep(self.COMMAND_SLEEP_TIME)

    def __send_f12_enter(self):
        self.keyboard.press(Key.f12)
        self.keyboard.release(Key.f12)

    def run_enter(self,Command,SleepTime):
        self.__send_escape_keys()
        self.keyboard.type(Command)
        self.__send_num_enter()
        time.sleep(SleepTime)

    def run_f12(self,Command,SleepTime):
        self.__send_escape_keys()
        self.keyboard.type(Command)
        self.__send_f12_enter()
        time.sleep(SleepTime)

    def send_string(self,text,SleepTime):
        self.keyboard.type(text)
        time.sleep(SleepTime)

def SendCommand(Command,SleepTime=0,BolPrint=False,BolClear=True):
    if BolClear:
        clear_screen_thread = SendKeys()
        clear_screen_thread.send_clear_screen(SleepTime)
        clear_screen_thread.start()
        clear_screen_thread.join()
    command_thread=SendKeys()
    command_thread.run_f12(Command,SleepTime)
    command_thread.start()
    command_thread.join()
    if BolPrint:
        print_thread=SendKeys()
        print_thread.send_print_keys(SleepTime)
        print_thread.start()
        print_thread.join()


def SendString(Text,SleepTime=0,BolPrint=False,BolClear=True):
    if BolClear:
        clear_screen_thread = SendKeys()
        clear_screen_thread.send_clear_screen(SleepTime)
        clear_screen_thread.start()
        clear_screen_thread.join()
    command_thread=SendKeys()
    command_thread.send_string(Text,SleepTime)
    command_thread.start()
    command_thread.join()
    if BolPrint:
        print_thread=SendKeys()
        print_thread.send_print_keys(SleepTime)
        print_thread.start()
        print_thread.join()
    


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
        
    
    
        
