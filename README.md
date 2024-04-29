# PD command and analysis

**Duplicate seats and names are completed. 'Poke eTerm', 'Default' and 'Times of PN1' do not start yet.**

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