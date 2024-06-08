from bins.handle_sy import SY
class GetPD():
    def __init__(self,PdCommand) -> None:
        super().__init__()
        self.__pd_command=PdCommand
        self.__sy_command='sy'
        # 假设有两种PD指令。 1，‘PD*,NACC’ 2，‘PD CA123/01JUN*PEK'
        if any(char.isdigit() for c in self.__pd_command):
            space_index = self.__pd_command.find(' ')
            asterisk_index=self.__pd_command.find('*')
            core_str=self.__pd_command[space_index:asterisk_index]
            self.__sy_command='sy' + core_str

