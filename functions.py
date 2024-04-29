def ReadTxt2String(txt_file_path):
    txtObj = open(txt_file_path,'rt')
    txtContent = txtObj.read()
    txtObj.close()
    return txtContent

def ReadTxt2List(txt_file_path):
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