import json
import threading
import keyboard_simulate
import argparse
from handle_sy import SY
from handle_se import SE
from handle_pd import PD
import functions
import re
from handle_bnd import BND
from handle_av import AV
from write_xlxs import FillOut
from datetime import datetime

'''
input:string,string,float,bol
input example: 'c:\\users','983/984/01JUN/02JUN/PEK',0.7,True
'''
class GetBriefingJson():
    def __init__(self, JsonFolder, FlightInfo):
        super().__init__()
        self.__josn_folder = JsonFolder
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
        self.Commands = self.__fill_placeholders(json_structure,values)

    
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
    
    def ProcessAndSave(self):
        pd=ProcessData(self.Commands,r'C:\Users\gostn\OneDrive\桌面\eterm\qqqqq.txt')
        pd.WiteXlsx(self.__josn_folder)

class RequestData():
    COMMAND_END_MARK = '\n===END===\n'
    ARRIVAL_END_MARK = '\n===ARRIVAL_END===\n'
    DEPARTURE_END_MARK = '\n===DEPARTURE_END===\n'

    def __init__(self,BriefCommands,CommandPending, Debug=False):
        self.commands=BriefCommands
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

class ProcessData():
    END_MARK = '===END==='
    ARRIVAL_MARK='===ARRIVAL_END=== '
    def __init__(self,BriefCommands,CommandsFilePath,):
        super().__init__()
        txt_list = functions.ReadTxt2List(CommandsFilePath)
        self.commands=BriefCommands
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
        self.arrival_flight_number=''
        self.arrival_leg=''
        self.departure_flight_number=''
        self.departure_leg=''
        self.departure_flight_date=''
        self.arrival_seat_configuration=''
        self.departure_etd=''
        self.departure_eta=''
        self.arrival_ac_reg=''
        self.departure_boarding_time=''
        self.arrival_pax_break_down=''
        self.departure_pax_break_down=''
        self.departure_gate=''
        self.special={}
        self.comment={}
        self.__get_arrival_data() #It would clear data after processing.
        self.__get_departure_data()

    def __get_arrival_data(self):
        for index,command in enumerate(self.arrival_set):
            if command.find('SY:') != -1:
                my_sy=SY(command,self.commands['arrival'])
                self.arrival_ac_reg=my_sy.ac_reg
                self.arrival_leg=my_sy.leg
                tmp_list=my_sy.checked.split('/')
                total=0
                for n in tmp_list:
                    total = total + int(n)
                self.arrival_pax_break_down=my_sy.checked + '=' + str(total)
                self.arrival_seat_configuration=my_sy.seat_configuration
                self.arrival_flight_number=my_sy.flight
                self.arrival_set[index] = ''
                continue
            if command.find('SE:') != -1:
                my_se=SE(command,'X')
                str_block_seats=','.join(my_se.combination_seats)
                self.comment['Inbound_Block']=str_block_seats
                self.arrival_set[index] = ''
                continue
        
    def __get_departure_data(self):
        for command in self.departure_set:
            if command.find('PD:') != -1:
                pd=PD()
                list_command = functions.String2List(command)
                count = pd.GetLastCount(list_command)
                key = self.__get_pd_special_key(command)
                if count!=0:
                    self.special[key]=count
            if 'BND:' in command:
                bnd=BND(command).numbers
                if bnd != '':
                    for key in self.commands['departure_section'][0]:
                        value=self.commands['departure_section'][0][key]
                        if 'BND' in value:
                            new_key=key[8:]
                            self.special[new_key]=bnd
                            break
            if 'AV:' in command:
                av=AV(command)
                self.departure_etd=av.Etd
                self.departure_eta=av.Eta
            if 'SY:' in command:
                sy=SY(command)
                self.departure_gate=sy.gate
                self.departure_boarding_time=sy.bdt
                tmp_list=sy.ret_minus_id.split('/')
                total = 0
                for n in tmp_list:
                    total = total + int(n)
                self.departure_pax_break_down=sy.ret_minus_id + '=' + str(total)
                self.departure_flight_number=sy.flight
                self.departure_flight_date=sy.flight_date 
                self.departure_leg=sy.leg

    def __get_pd_special_key(self,command):
        for key in self.commands['departure_section'][0]:
            if 'special_' in key:
                input_command=str(self.commands['departure_section'][0][key]).upper()
                pattern=re.compile(input_command[:2]+':.'+input_command[2:])
                if pattern.search(command):
                    return key[8:]
                
    def WiteXlsx(self,JsonPath):
        xlsx=FillOut(JsonPath)
        xlsx.WriteArrivalFlight(self.arrival_flight_number)
        xlsx.WriteArrivalLeg(self.arrival_leg)
        xlsx.WriteDepartureFlight(self.departure_flight_number)
        xlsx.WriteDepartureLeg(self.departure_leg)
        xlsx.WriteDepartureDate(self.departure_flight_date)
        xlsx.WriteArrivalSeatConfiguration(self.arrival_seat_configuration)
        xlsx.WriteDepartureEtd(self.departure_etd)
        xlsx.WriteDepartureEta(self.departure_eta)
        xlsx.WriteArricalAc(self.arrival_ac_reg)
        xlsx.WriteDepartureBdt(self.departure_boarding_time)
        xlsx.WriteArrivalPax(self.arrival_pax_break_down)
        xlsx.WriteDeparturePax(self.departure_pax_break_down)
        xlsx.WriteDepartureGate(self.departure_gate)
        xlsx.WriteComments(self.comment)
        xlsx.WriteSpecials(self.special)
        current_time = datetime.now().time()
        # Convert the current time to a long integer
        time_long = int(current_time.strftime("%H%M%S"))
        xlsx.save_copy(self.arrival_flight_number 
                       +'.'+self.departure_flight_number
                       +'.'+self.departure_flight_date
                       + '-'+str(time_long) + '.xlsx')

def main():
    parser = argparse.ArgumentParser(description="PD start")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    GetData=GetBriefingJson(r'C:\Users\gostn\我的Github库\PdStar0.2\resources',r'818/818/01JUN/01JUN/IAD')
    #RequestData(briefing_commands, 0.5,args.debug)
    GetData.ProcessAndSave()
if __name__ == "__main__":
    main()