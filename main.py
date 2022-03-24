#!/usr/bin/env python3
import PySimpleGUI as sg
import tempfile
import subprocess
import os
import sys
from pathlib import Path

layout = [
    [sg.Text('Please press the red button...')],
    [sg.Text('', key='output')],
    [sg.Button('Click Me!', button_color='red', key='redbutton')] 
]

window = sg.Window('Call an external script', layout)

# this is the directory for the mounted image from the binary created by nuitka
basedir = Path(__file__).parent

# create a temporary directory with the lifetime of the with-statement
with tempfile.TemporaryDirectory() as tmp:
    tmpdir = Path(tmp)
    # create a dynamically generated module in the temporary directory
    dynamically_created_module = tmpdir / "dynamic_module.py"
    dynamically_created_module.write_text(
'''
print("imported dynamic module")

def surprise():
    print("Nobody expects the Spanish Inquisition!")
'''
    )

    # set the PYTHONPATH to include both the temporary directory and the modules directory with the static module
    ENV = {'PYTHONPATH': os.pathsep.join((tmp, str(basedir / 'modules')))}
    ENV.update(os.environ)

    # main loop
    while True:
        # read events from window
        event, values = window.read()
        if event == sg.WIN_CLOSED :  # end loop if user closes window
            break
        elif event == 'redbutton':  # actions if the red button is pressed
            window['redbutton'].update(disabled=True)  # disable the button while the script is running
            command = ['python3', 'external_program.py', '--run-python', basedir / 'datei.py']
            try:
                s = subprocess.run(command, env=ENV, text=True, check=True, capture_output=True)
            except subprocess.CalledProcessError as err:
                print(err.stdout, file=sys.stdout)
            else:
                window['output'].update(s.stdout)  # write the text obtained by the subprocess into the output text box
            window['redbutton'].update(disabled=False)  # reenable the button
    
    window.close()
