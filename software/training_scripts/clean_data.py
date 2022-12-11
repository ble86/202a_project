import csv
import numpy as np
import os

CURR_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(CURR_FOLDER, '../data')
INPUT_FILE = os.path.join(DATA_FOLDER, 'data.csv')
OUTPUT_FILE = os.path.join(DATA_FOLDER, 'clean_data.csv')

SENSOR_SAMPLE = 512*4

if __name__ == '__main__':
    clean_data = []
    with open(INPUT_FILE) as csvfile:
        og_csv = csv.reader(csvfile, delimiter=' ', quotechar='|')
        clean_row = []
        for row in og_csv:
            if len(row) == 0:
                continue
            elif row[0] == 'Key':
                clean_data.append(clean_row)
                clean_row = []
            else:
                clean_row.append(row[0])
    clean_data.pop(0)
    four_sensor_data = []
    for row in clean_data:
        if len(row) > SENSOR_SAMPLE + 1:
            print("Long Row")
        if len(row) >= SENSOR_SAMPLE + 1:
            four_sensor_data.append(row[0:SENSOR_SAMPLE+1])
    with open(OUTPUT_FILE, 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(four_sensor_data)