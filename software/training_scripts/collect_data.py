import serial
import numpy as np
import pandas as pd
import signal
from pathlib import Path
import os
import sys
import re

BAUD_RATE = 115200
ESP32_PORT = ''
KEYBOARD_PORT = ''
ESP32_DATA_WINDOW = 32
ESP32_TIMEOUT = 3

OUTPUT_FILE = 'training_data.csv'

data = []

def exit_handler(signum, frame):
    cols = [(f'{i}[{j}]') for i in range(4) for j in range(ESP32_DATA_WINDOW)]
    cols.insert(0, 'Key')
    index = [i for i in range(len(data))]
    df = pd.DataFrame(data=data, cols=cols, index=index)

    data_collection_folder = Path.cwd().parent.joinpath('data_collection')
    if not data_collection_folder.exists():
        os.mkdir(data_collection_folder)
    output_file = data_collection_folder.joinpath(OUTPUT_FILE)

    df.to_csv(output_file, index=False)
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_handler)
    esp_ser = serial.Serial(port=ESP32_PORT, baudrate=BAUD_RATE, timeout=ESP32_TIMEOUT)
    kb_ser = serial.Serial(port=KEYBOARD_PORT, baudrate=BAUD_RATE, timeout=0)
    data_counter = 0
    mic0_data = []
    mic1_data = []
    mic2_data = []
    mic3_data = []
    last_press = 0

    while True:
        vib_string = esp_ser.readline()
        press = kb_ser.read(1)
        if press != 0 and data_counter == 0:
            data_counter = ESP32_DATA_WINDOW
            last_press = press
        
        if data_counter > 0:
            numbers = re.findall( r'0x[0-9a-f]{4}', vib_string)
            vib_data = list(map(lambda x: int(x, base=16), numbers))
            mic0_data.append(vib_data[0])
            mic1_data.append(vib_data[1])
            mic2_data.append(vib_data[2])
            mic3_data.append(vib_data[3])
            if data_counter == 1:
                final_data = mic0_data + mic1_data + mic2_data + mic3_data
                final_data.insert(0, last_press)
                data.append(final_data)
            data_counter -= 1


                



