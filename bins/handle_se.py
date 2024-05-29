from functions import ReadTxt2String

class SE:
    def __init__(self,SeFilePath):
        super().__init__()
        self.__se_content=ReadTxt2String(SeFilePath)
        self.x_seats=[]
        self.run()

    def run(self):
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

        # Find the coordinates where the character is 'X'
        for key, char in coordinates.items():
            if char == 'X':
                self.x_seats.append(key)

se=SE(r'C:\Users\gostn\OneDrive\桌面\eterm\se.txt')
print(se.x_seats)