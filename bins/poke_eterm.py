import json
import threading
import keyboard_simulate
import argparse
from pynput.keyboard import Controller as key_controller
import handle_sy
'''
input:string,string,float,bol
input example: 'c:\\users','983/984/01JUN/02JUN/PEK',0.7,True
'''
def briefing_logic(json_folder_path,flight_info,command_pending,debug):
    with open(json_folder_path + r'\briefing_command.json','r') as file:
        json_structure = json.load(file)
    split_values = flight_info.split('/')
    # Assign the split values to respective variables
    arrival_flight_number = split_values[0]
    departure_flight_number = split_values[1]
    arrival_flight_date = split_values[2]
    departure_flight_date = split_values[3]
    arrival = split_values[4]
    values = {
        "arrival_flight_number": arrival_flight_number,
        "arrival_date": arrival_flight_date,
        "arrival": arrival,
        "departure_flight_number":departure_flight_number,
        "departure_date":departure_flight_date,
        "ac_reg":""
    }
    commands=fill_placeholders(json_structure,values)
    
    event1=threading.Event()
    event2=threading.Event()
    listener_start=keyboard_simulate.ClickListener(event1)
    listener_start.start()
    # Wait for the first click event
    event1.wait()
    listener_loop = keyboard_simulate.ClickListener(event2)
    listener_loop.start()
    if listener_loop.click_position == None:
        send_arrival_commands(commands,command_pending,debug)

        send_departure_commands(commands,command_pending,debug)
    else:
        event2.wait()
        listener_loop.join()
        listener_loop.event.clear()
    

# Function to replace placeholders
def fill_placeholders(obj, values):
    if isinstance(obj, str):
        # Replace placeholders in the string
        for key, value in values.items():
            obj = obj.replace(f"${{{key}}}", value)
        return obj
    elif isinstance(obj, list):
        # Recursively handle lists
        return [fill_placeholders(item, values) for item in obj]
    elif isinstance(obj, dict):
        # Recursively handle dictionaries
        return {key: fill_placeholders(value, values) for key, value in obj.items()}
    return obj

def send_arrival_commands(commands_in_json,command_pending,debug):
    keyboard=key_controller()
    for key in commands_in_json['arrival_section'][0]:
        command_thread=keyboard_simulate.SendKeys(commands_in_json['arrival_section'][0][key],command_pending)
        command_thread.start()
        command_thread.join()
        command_thread=keyboard_simulate.SendKeys('PF1',command_pending)
        command_thread.start()
        command_thread.join()
        keyboard.type('\n===END===\n')
        if not debug:
            command_thread.send_print_keys()

def send_departure_commands(commands_in_json,command_pending,debug):
    keyboard=key_controller()
    for key in commands_in_json['departure_section'][0]:
        command_thread=keyboard_simulate.SendKeys(commands_in_json['departure_section'][0][key],command_pending)
        command_thread.start()
        command_thread.join()
        command_thread=keyboard_simulate.SendKeys('PL',command_pending)
        command_thread.start()
        command_thread.join()
        keyboard.type('\n===END===\n')
        if not debug:
            command_thread.send_print_keys()

def get_arrival_data(file_path):
    pass


def main():
    parser = argparse.ArgumentParser(description="PD start")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    briefing_logic(r'C:\Users\gostn\我的Github库\PdStar0.2\resources',r'983/984/01JUN/02JUN/PEK',0.7,args.debug)
if __name__ == "__main__":
    main()