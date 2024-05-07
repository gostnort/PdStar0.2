# PD command and analysis

## Install/Update

Download this project, and extract to a new folder.

### Build an virtual environment

In the project folder(where the README.md is), run the following commands

```
python -m venv .venv

.venv/scripts/activate

pip install -r requirements.txt
```

### Update the Shortcut

1. Right click the 'Run.lnk' to open its property.

0. Change the 'target' to ``Current_folder_absolute_path\.venv\Scripts\pythonw.exe "Current_folder_absolute_path\main_window.py"``

0. Change the 'start' to ``Current_folder_absolute_path\.venv\Scripts``

0. The icon is in the 'resources' folder, if you like.

## How to use

### The Upper Portion

#### Option of PD

1. Output the command of 'PD'. The default value is just an asterisk'*'. You can add options like:
    ```
      818/./*/IAD,ACC
    *,NACC
    ```
0. Output how many times of 'PN1' after the 'PD' command.

#### Option of Default

(Not completed yet)

#### The Button of 'Poke'

The gray text box is the command pending time in each output. The unit is Second. Commands must wait more than '0.5' second according to the average mensuring. If the network latancy is higher than 500ms, it can up to '0.7', or other number you prefer to.

Using the left button pokes the black screen directly after you clicked this button. Clicking the left button at **anywhere again could cancel** the 'PN1' output.

### The Lower Portion

1. The 'Open...' button will open a Windows dialog window for selecting a '.txt' file. This file shall contain the required results from 'PD'

0. Checked 'Dup Names' will show duplicate names in the file.

0. Checked 'Dup Seats' will show duplicate seats in the file.

0. 'Run' will print the rusult in the big text box.