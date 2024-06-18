from handle_sy import SY
from keyboard_simulate import SendCommand
import json
class GetPD():
    def __init__(self,PdCommand,ResourcesPath) -> None:
        super().__init__()
        self.__pd_command=PdCommand
        self.__sy_command='sy'
        # 假设有两种PD指令。 1，‘PD*,NACC’ 2，‘PD CA123/01JUN*PEK'
        if any(char.isdigit() for c in self.__pd_command):
            space_index = self.__pd_command.find(' ')
            asterisk_index=self.__pd_command.find('*')
            core_str=self.__pd_command[space_index:asterisk_index]
            self.__sy_command='sy' + core_str
        self.__resources=ResourcesPath
        with open(self.__resources,'r') as file:
            config=json.load(file)
        self.__txt_path=config['default_path']

    def PrintCommands(self):
        pass
