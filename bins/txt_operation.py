import os
import time
def ReadTxt2String(txt_file_path)->str:
    txtObj = open(txt_file_path,'rt')
    txtContent = txtObj.read()
    txtObj.close()
    return txtContent

def ReadTxt2List(txt_file_path)->list:
    """
    Read the lines of a text file into a list.

    Args:
        txt_file_path (str): The path to the text file.

    Returns:
        list: A list containing the lines of the text file.
    """
    try:
        with open(txt_file_path, 'rt') as txtObj:
            txtContent = txtObj.readlines()
        return txtContent
    except FileNotFoundError:
        print(f"Error: File '{txt_file_path}' not found.")
        return []
    
def String2List(MultilineString):
    # Use splitlines() to split the string into a list of lines
    return MultilineString.splitlines()

def List2String(Lines):
    return '\n'.join(Lines)

def AppendText(TxtPath,Text):
    end_time = time.time() + 1  # 1 second from now
    while time.time() < end_time:
        if os.access(TxtPath, os.W_OK):
            try:
                with open(TxtPath, 'a') as file:
                    file.write(Text + '\n')
                    break
            except IOError as e:
                print(f"Error writing to file: {e}. Retrying in 100ms...")
        else:
            print(f"{TxtPath} file is locked by another program, retrying in 100ms...")
        time.sleep(0.1)  # sleep for 100ms
    else:
        print("Could not write to file after 1 second.")

def main():
    AppendText(r'C:\Users\gostn\my_github\pdstar0.2\resources\qqqqq.txt','A')

if __name__ == '__main__':
    main()