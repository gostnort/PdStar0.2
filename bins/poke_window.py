import json
import threading
import keyboard_simulate
import argparse
from pynput.keyboard import Controller as key_controller
from handle_sy import SY
from handle_se import SE
from handle_pd import PD
import functions
'''
input:string,string,float,bol
input example: 'c:\\users','983/984/01JUN/02JUN/PEK',0.7,True
'''
class RequestData():
    COMMAND_END_MARK = '\n===END===\n'
    ARRIVAL_END_MARK = '\n===ARRIVAL_END===\n'
    DEPARTURE_END_MARK = '\n===DEPARTURE_END===\n'

    def __init__(self, JsonFolder, FlightInfo, CommandPending, Debug=False):
        super().__init__()
        with open(JsonFolder + r'\briefing_command.json','r') as file:
            json_structure = json.load(file)
        split_values = FlightInfo.split('/')
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
        self.commands=self.__fill_placeholders(json_structure,values)
        self.bol_debug = Debug
        self.command_pending_time=CommandPending
        self.run()

    def run(self):
        event1=threading.Event()
        event2=threading.Event()
        listener_start=keyboard_simulate.ClickListener(event1)
        listener_start.start()
        # Wait for the first click event
        event1.wait()
        listener_loop = keyboard_simulate.ClickListener(event2)
        listener_loop.start()
        print(listener_loop.click_position)
        bol_stop_listerner = False
        bol_stop_listerner = self.__send_arrival_commands(listener_loop)
        if not bol_stop_listerner:
            bol_stop_listerner = self.__send_departure_commands(listener_loop)
        event2.wait()
        print(listener_loop.click_position)
        listener_loop.join()
        listener_loop.event.clear()
        
    # Function to replace placeholders
    def __fill_placeholders(self, obj, values):
        if isinstance(obj, str):
            # Replace placeholders in the string
            for key, value in values.items():
                obj = obj.replace(f"${{{key}}}", value)
            return obj
        elif isinstance(obj, list):
            # Recursively handle lists
            return [self.__fill_placeholders(item, values) for item in obj]
        elif isinstance(obj, dict):
            # Recursively handle dictionaries
            return {key: self.__fill_placeholders(value, values) for key, value in obj.items()}
        return obj

    def __send_arrival_commands(self,listener):
        for key in self.commands['arrival_section'][0]:
            if listener.click_position == None:
                        bol_stop_pages = False
                        for stop_key in self.commands['stop_turn_page']:
                            if stop_key == key:
                                bol_stop_pages = True
                        if bol_stop_pages:
                            if self.bol_debug:
                                keyboard_simulate.SendCommand(self.commands['arrival_section'][0][key],
                                                            self.command_pending_time)
                                keyboard_simulate.SendString(self.COMMAND_END_MARK)
                            else:
                                keyboard_simulate.SendCommand(self.commands['arrival_section'][0][key],
                                                            self.command_pending_time,True)
                                keyboard_simulate.SendString(self.COMMAND_END_MARK,True,False)
                        else:
                            keyboard_simulate.SendCommand(self.commands['arrival_section'][0][key],
                                                        self.command_pending_time,False)
                            keyboard_simulate.SendCommand('PF1'
                                                        ,self.command_pending_time)
                            keyboard_simulate.SendString(self.COMMAND_END_MARK,
                                                        0,
                                                        True,
                                                        False)
            else:
                return True
        if self.bol_debug:
            keyboard_simulate.SendString(self.ARRIVAL_END_MARK,
                                            0,
                                            False,
                                            True)
        else:
            keyboard_simulate.SendString(self.ARRIVAL_END_MARK,
                                            0,
                                            True,
                                            True)
        return False
        

    def __send_departure_commands(self,listener):
        for key in self.commands['departure_section'][0]:
                    if listener.click_position == None:
                        bol_stop_pages = False
                        for stop_key in self.commands['stop_turn_page']:
                            if stop_key == key:
                                bol_stop_pages = True
                        if bol_stop_pages:
                            if self.bol_debug:
                                keyboard_simulate.SendCommand(self.commands['departure_section'][0][key],
                                                            self.command_pending_time)
                                keyboard_simulate.SendString(self.COMMAND_END_MARK)
                            else:
                                keyboard_simulate.SendCommand(self.commands['departure_section'][0][key],
                                                            self.command_pending_time,True)
                                keyboard_simulate.SendString(self.COMMAND_END_MARK,True,False)
                        else:
                            keyboard_simulate.SendCommand(self.commands['departure_section'][0][key],
                                                        0.3,False)
                            keyboard_simulate.SendCommand('PL1'
                                                        ,self.command_pending_time,True)
                            keyboard_simulate.SendString(self.COMMAND_END_MARK,
                                                        0,
                                                        True,
                                                        True)
                    else:
                        return True
        if self.bol_debug:
            keyboard_simulate.SendString(self.DEPARTURE_END_MARK,
                                            0,
                                            False,
                                            True)
        else:
            keyboard_simulate.SendString(self.DEPARTURE_END_MARK,
                                            0,
                                            True,
                                            True)
        return False

class HandleData():
    END_MARK = '===END==='
    ARRIVAL_MARK='===ARRIVAL_END=== '
    def __init__(self,FilePath,Arrival):
        super().__init__()
        txt_list = functions.ReadTxt2List(FilePath)
        self.arrival_set=[]
        self.departure_set=[]
        tmp_str = ''
        bol_arrival = True
        for line in txt_list:
            if line.find(self.ARRIVAL_MARK) != -1:
                bol_arrival = False
            if line.find(self.END_MARK) == -1:
                tmp_str=tmp_str + line
                continue
            if bol_arrival:
                self.arrival_set.append(tmp_str)
                tmp_str = ''
            else:
                self.departure_set.append(tmp_str)
                tmp_str = ''
        self.arrival = Arrival
        self.arrival_leg=''
        self.arrival_seat_configuration=''
        self.arrival_ac_reg=''
        self.arrival_pax_break_down=''
        self.arrival_blocked_seats=''
        self.__get_arrival_data() #It would clear data after processing.
        self.__get_departure_data()

    def __get_arrival_data(self):
        for index,command in enumerate(self.arrival_set):
            if command.find('SY:') != -1:
                my_sy=SY(command,self.arrival)
                self.arrival_ac_reg=my_sy.ac_reg
                self.arrival_leg=my_sy.leg
                self.arrival_pax_break_down=my_sy.checked
                self.arrival_seat_configuration=my_sy.seat_configuration
                self.arrival_set[index] = ''
                continue
            if command.find('SE:') != -1:
                my_se=SE(command,'X')
                print(command)
                self.arrival_blocked_seats=my_se.combination_seats
                print(self.arrival_blocked_seats)
                self.arrival_set[index] = ''
                continue
        
    def __get_departure_data(self):
        for command in self.departure_set:
            if command.find('PD:') != -1:
                pd=PD()
                list_command = functions.String2List(command)
                pd.GetLastCount(list_command)


def main():
    parser = argparse.ArgumentParser(description="PD start")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    #RequestData(r'C:\Users\Admin\Downloads\PdStar0.2-main\resources',r'818/818/01JUN/01JUN/IAD',0.5,args.debug)
    HandleData(r'C:\Users\gostn\OneDrive\桌面\eterm\qqqqq.txt','IAD')
if __name__ == "__main__":
    main()