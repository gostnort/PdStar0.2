import re
class SY():
    def __init__(self,SyContent,BolTransit):
        super().__init__()
        self.ac_type=''
        self.ac_reg=''
        self.ret_minus_id=''
        self.gate=''
        self.leg=''
        self.bdt=''
        self.__sy_content = SyContent
        self.__bol_transit=BolTransit
        self.__run()

    def __run(self):
        last_index = self.__get_ac_type()
        last_index = self.__get_gate(last_index)
        last_index = self.__get_bdt(last_index)
        last_index = self.__get_leg(last_index)
        last_index = self.__get_ret_minus_id(last_index)

    def __get_ac_type(self):
        try:
            pattern=re.compile(r'\sTCI\s')
            match=re.search(pattern,self.__sy_content)
            last_index=match.end()
            pattern=re.compile(r'\d{3}/.*?/B\d{4}')
            match=re.search(pattern,self.__sy_content[last_index:])
            self.ac_type=match.group(0)
            split_ac_type=self.ac_type.split('/')
            self.ac_reg=split_ac_type[2]
            return match.end()
        except ValueError as e:
            print("__get_ac_type() has an error.\n",e)
            return 0
        
    def __get_gate(self,last_index):
        try:
            pattern=re.compile(r'\sGTD/.*?\s')
            match=re.search(pattern,self.__sy_content[last_index:])
            self.gate=match.group(0)
            self.gate=self.gate.split('/')[1]
            return match.end()
        except ValueError as e:
            print("__get_gate() has an error.\n",e)
            return 0
        
    def __get_bdt(self,last_index):
        try:
            pattern=re.compile(r'BDT\d{4}')
            match=re.search(pattern,self.__sy_content[last_index:])
            self.bdt=match.group(0)[3:]
            return match.end()
        except ValueError as e:
            print("__get_bdt() has an error.\n",e)
            return 0
    
    def __get_leg(self,last_index):
        try:
            pattern=re.compile(r'\*[A-Z]{6}\sR')
            match=re.search(pattern,self.__sy_content[last_index:])
            self.leg=match.group(0)[1:7]
            return match.end()
        except ValueError as e:
            print("__get_leg() has an error.\n",e)
            return 0
    
    def __get_ret_minus_id(self,last_index):
        try:
            pattern=re.compile(r'\s{3}SA\d+(/\d+)*')
            match=re.search(pattern,self.__sy_content[last_index:])
            id=match.group(0)
            id=id.lstrip()[2:]
            id_split=id.split('/')
            pattern=re.compile(r'\s{3}RET\d+(/\d+)*')
            match=re.search(pattern,self.__sy_content[match.end():])
            ret=match.group(0)
            ret=ret.lstrip()[3:]
            ret_split=ret.split('/')
            for index in range(0,len(ret_split)):
                if self.ret_minus_id != '':
                    self.ret_minus_id = self.ret_minus_id + '/'
                self.ret_minus_id = self.ret_minus_id + str(int(ret_split[index])-int(id_split[index]))
            return match.end()
        except ValueError as e:
            print("__get_ret_minus_id() has an error.\n",e)
            return 0
        
import functions
def main():
    sy_content=functions.ReadTxt2String(r'C:\Users\gostn\OneDrive\桌面\eterm\sy_direct.txt')
    sy=SY(sy_content,False)
    print(sy.ac_reg,sy.ac_type,sy.bdt,sy.gate,sy.leg,sy.ret_minus_id)
if __name__ == "__main__":
    main()