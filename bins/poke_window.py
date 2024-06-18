import json
import threading
from keyboard_simulate import SendCommand,SendString,ClickListener
import argparse
from handle_sy import SY
from handle_se import SE
from handle_pd import PD
from txt_operation import ReadTxt2List, AppendText
import re
from handle_bnd import BND
from handle_av import AV
from write_xlxs import FillOut
from datetime import datetime

'''
input:string,string,float,bol
input example: 'c:\\users','983/984/01JUN/02JUN/PEK/B2045',0.7,True
'''
class GetBriefingJson():
    def __init__(self, JsonFolder:str, FlightInfo:str):
        super().__init__()
        self.__josn_folder = JsonFolder
        with open(JsonFolder + r'\briefing_command.json','r') as file:
            self.Json_structure = json.load(file)
        split_values = FlightInfo.split('/')
        # Assign the split values to respective variables
        arrival_flight_number = split_values[0]
        departure_flight_number = split_values[1]
        arrival_flight_date = split_values[2]
        departure_flight_date = split_values[3]
        arrival = split_values[4]
        try:
            ac_reg = split_values[5]
        except:
            ac_reg = ''
        self.Values = {
            "arrival_flight_number": arrival_flight_number,
            "arrival_date": arrival_flight_date,
            "arrival": arrival,
            "departure_flight_number":departure_flight_number,
            "departure_date":departure_flight_date,
            "ac_reg":ac_reg
        }
        self.Commands = self.Fill_placeholders(self.Json_structure,self.Values)

    
        # Function to replace placeholders
    def Fill_placeholders(self, obj, values):
        if isinstance(obj, str):
            # Replace placeholders in the string
            for key, value in values.items():
                obj = obj.replace(f"${{{key}}}", value)
            return obj
        elif isinstance(obj, list):
            # Recursively handle lists
            return [self.Fill_placeholders(item, values) for item in obj]
        elif isinstance(obj, dict):
            # Recursively handle dictionaries
            return {key: self.Fill_placeholders(value, values) for key, value in obj.items()}
        return obj


class RequestData():
    COMMAND_END_MARK = '\n===END===\n'
    ARRIVAL_END_MARK = '\n===ARRIVAL_END===\n'
    DEPARTURE_END_MARK = '\n===DEPARTURE_END===\n'

    def __init__(self,JsonPath,FlightInfo,CommandPending, Debug=False):
        super().__init__()
        self.__json_path = JsonPath
        self.__config=GetBriefingJson(JsonPath,FlightInfo)
        self.Commands = self.__config.Commands
        self.__bol_debug = Debug
        self.__command_pending_time=CommandPending
        self.run()

    def run(self):
        event1=threading.Event()
        event2=threading.Event()
        listener_start=ClickListener(event1)
        listener_start.start()
        # Wait for the first click event
        event1.wait()
        listener_loop = ClickListener(event2)
        listener_loop.start()
        bol_stop_listerner = False
        bol_stop_listerner = self.__send_arrival_commands(listener_loop)
        pd=ProcessData(self.Commands)
        pd.Get_arrival_data()
        # Add the ac_reg to reset the self.Commands.
        ac_reg=pd.arrival_ac_reg
        self.__config.Values['ac_reg']=ac_reg
        self.Commands=self.__config.Fill_placeholders(self.__config.Json_structure,self.__config.Values)
        if not bol_stop_listerner:
            bol_stop_listerner = self.__send_departure_commands(listener_loop)
        pd.Get_departure_data()
        pd.WiteXlsx(self.__json_path)
        listener_loop.left_click()
        listener_loop.stop()
        listener_loop.join()
        event2.wait()
        listener_loop.event.clear()

    def __send_arrival_commands(self,listener):
        for key in self.Commands['arrival_section'][0]:
            if listener.click_position == None:
                        bol_stop_pages = False
                        for stop_key in self.Commands['stop_turn_page']:
                            if stop_key == key:
                                bol_stop_pages = True
                        if bol_stop_pages:
                            if self.__bol_debug:
                                SendCommand(self.Commands['arrival_section'][0][key],
                                            self.__command_pending_time,
                                            False,False)
                                SendString(self.COMMAND_END_MARK,
                                           False,False)
                            else:
                                SendCommand(self.Commands['arrival_section'][0][key],
                                            self.__command_pending_time,
                                            True)
                                SendString(self.COMMAND_END_MARK,
                                           True,
                                           False)
                        else:
                            if self.__bol_debug:
                                SendCommand(self.Commands['arrival_section'][0][key],
                                            self.__command_pending_time,
                                            False,False)
                                SendCommand('PF1',
                                            self.__command_pending_time,
                                            False,False)
                                SendString(self.COMMAND_END_MARK,
                                            0,
                                            False,False)
                            else:
                                SendCommand(self.Commands['arrival_section'][0][key],
                                            self.__command_pending_time,
                                            False)
                                SendCommand('PF1',
                                            self.__command_pending_time)
                                SendString(self.COMMAND_END_MARK,
                                            0,
                                            True,
                                            False)
            else:
                return True
        AppendText(self.Commands['default_path'],
                   self.ARRIVAL_END_MARK)
        return False
        

    def __send_departure_commands(self,listener):
        for key in self.Commands['departure_section'][0]:
                    if listener.click_position == None:
                        bol_stop_pages = False
                        for stop_key in self.Commands['stop_turn_page']:
                            if stop_key == key:
                                bol_stop_pages = True
                        if bol_stop_pages:
                            if self.__bol_debug:
                                SendCommand(self.Commands['departure_section'][0][key],
                                            self.__command_pending_time,False,False)
                                SendString(self.COMMAND_END_MARK,False,False)
                            else:
                                SendCommand(self.Commands['departure_section'][0][key],
                                            self.__command_pending_time,
                                            True)
                                SendString(self.COMMAND_END_MARK,
                                           True,
                                           False)
                        else:
                            if self.__bol_debug:
                                SendCommand(self.Commands['departure_section'][0][key],
                                            self.__command_pending_time,
                                            False,False)
                                SendCommand('PL1',self.__command_pending_time,
                                            False,False)
                                SendString(self.COMMAND_END_MARK,
                                            0,
                                            False,False)
                            else:   
                                SendCommand(self.Commands['departure_section'][0][key],
                                            self.__command_pending_time,
                                            False)
                                SendCommand('PL1',self.__command_pending_time,True)
                                SendString(self.COMMAND_END_MARK,
                                            0,
                                            True,
                                            True)
                    else:
                        return True
        AppendText(self.Commands['default_path'],
                   self.DEPARTURE_END_MARK)
        return False

class ProcessData():
    END_MARK = '===END==='
    ARRIVAL_MARK='===ARRIVAL_END=== '
    def __init__(self,BriefCommands):
        super().__init__()
        txt_list = ReadTxt2List(BriefCommands['default_path'])
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

    def Get_arrival_data(self):
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
        
    def Get_departure_data(self):
        for command in self.departure_set:
            if command.find('PD:') != -1:
                pd=PD(command)
                count = pd.GetLastCount()
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
    args.debug = True # Not necessary while running in the terminal.
    request_data=RequestData(r'C:\Users\gostn\my_github\PdStar0.2\resources',
                             r'818/818/01JUN/01JUN/IAD',
                             0.5,
                            args.debug)
    ProcessData(request_data.Commands)
if __name__ == "__main__":
    main()