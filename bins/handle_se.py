from functions import ReadTxt2String

class SE:
    def __init__(self,SeFilePath,Symbol):
        super().__init__()
        self.__se_content=ReadTxt2String(SeFilePath)
        self.individual_seats=[]
        self.combination_seats=[]
        self.GetListOfSymbol(Symbol)

    def __combination_seats(self):
        seats=[]
        for seat in reversed(self.individual_seats):
            current_row=seat[:2]
            bol_found = False
            for i in range(0,len(seats)):
                exsit_row=seats[i][:2]
                if current_row == exsit_row:
                    seats[i]=seats[i] + seat[-1]
                    bol_found = True
                    break
            if not bol_found:
                seats.append(seat)
        return seats

    def __sort_by_row(self):
        sorted_list = sorted(self.combination_seats, key=lambda x: int(x[:2]))
        return sorted_list

    def GetListOfSymbol(self,Symbol):
        lines = self.__se_content.split('\n')
        columns = {}
        coordinates = {}
        # 先找有数据的列，并整理列号。
        digit10=0
        for i, char in enumerate(lines[2]):
            if char.isdigit():
                if lines[1][i].isdigit():
                    digit10=int(lines[1][i]) * 10
                column_number = int(char) + digit10
                columns[i] = column_number

        # 跳过前两行，根据已有的列号，找每行内的非数字，非空格，非回车。
        # 然后逆向查找前面的字母，且这个字母所在列的第一行是一个字母。
        # 写入座位号。
        for i, line in enumerate(lines):
            if i > 2 and len(line) > 4:
                for key in columns:
                    char = line[key]
                    if not char.isdigit() and not char.isspace() and char != '\n':
                        for n in range(key-1,1,-1):
                            if line[n].isalpha() and lines[1][n].isalpha():
                                coordinates[f"{columns[key]}{line[n]}"]=char
                                break

        # Find the coordinates where the character is the Symbol
        for key, char in coordinates.items():
            if char == Symbol:
                self.individual_seats.append(key)

        self.combination_seats = self.__combination_seats()
        self.combination_seats = self.__sort_by_row()

se=SE(r'C:\Users\gostn\OneDrive\桌面\eterm\se.txt','X')
print(se.individual_seats)
print(se.combination_seats)