
class pd_properties():
    __Pd_item_list=[]
    __Pd_text=[]
    bol_name=False
    NameMessage=[]
    bol_seat=False
    SeatMessage=[]
    ErrorMessage=[]
    DebugMessage=[]

    def run(self,pd_text,bol_name=False,bol_seat=False):
        self.__Pd_item_list.clear()
        self.__Pd_text.clear()
        self.NameMessage.clear()
        self.SeatMessage.clear()
        self.ErrorMessage.clear()
        self.DebugMessage.clear()
        self.bol_name=False
        self.bol_seat=False
        index=str(pd_text).find('1.')
        if index == 0:
            return self.__Pd_item_list
        self.__Pd_text = pd_text.copy()
        self.__Pd_text = self.__RegularityPd()
        self.__FillOutContents()
        if bol_name:
            self.bol_name=self.__check_duplicate_names()
        if bol_seat:
            self.bol_seat=self.__check_duplicate_seats()

    def __SeprateFirstLine(self, first_line_text):
        try:
            sn=first_line_text[0:3]
            pax_name=first_line_text[6:21]
            pax_name=pax_name.rstrip().lstrip()
            pax_name=pax_name.replace('+','')
            bn=first_line_text[28:31]
            pax_seat=first_line_text[33:37]
            pax_seat=pax_seat.rstrip()
            pax_cls=first_line_text[40]
            self.DebugMessage.append(sn+' | '+pax_name+' | '+bn+' | '+pax_seat+' | '+pax_cls)
            return sn,pax_name,bn,pax_seat,pax_cls
        except:
            self.ErrorMessage.append("An Error occured of "+first_line_text)
        return False
    
    def __RegularityPd(self):
        regularity_pd=[]
        for line in self.__Pd_text:
            if line.find('>') == -1:
                regularity_pd.append(line)
        return regularity_pd
    
    def __FillOutContents(self):
        for pd in self.__Pd_text:
            if pd.find('.') != -1:
                pd_split=self.__SeprateFirstLine(pd)
                new_item = {}  # Create a new dictionary for each item
                new_item['sn'] = pd_split[0]
                new_item['name'] = pd_split[1]
                new_item['bn'] = pd_split[2]
                new_item['seat'] = pd_split[3]
                new_item['cls'] = pd_split[4]
                self.__Pd_item_list.append(new_item)

    def __check_duplicate_names(self):
        for item in self.__Pd_item_list:
            sn,name='',''
            for other in self.__Pd_item_list:
                if item['name'] == other['name'] and item['sn'] != other['sn']:
                    sn=item['sn']
                    name=item['name']
                    self.NameMessage.append('PR'+sn+'PD name is '+name)
                    break
        return len(self.NameMessage) != 0


    def __check_duplicate_seats(self):
        for item in self.__Pd_item_list:
            if len(item['seat']) == 0:
                continue
            sn,seat='',''
            for other in self.__Pd_item_list:
                if item['seat'] == other['seat'] and item['sn'] != other['sn']:
                    sn=item['sn']
                    seat=item['seat']
                    self.SeatMessage.append('PR'+sn+'PD seat assigned '+seat)
                    break
        return len(self.SeatMessage) != 0