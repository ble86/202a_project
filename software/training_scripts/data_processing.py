import csv
import numpy as np
import os

SENSOR_SAMPLE = 512*4
SAMPLES_PER_SENSOR = 512

CURR_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(CURR_FOLDER, '../data')
INPUT_FILE = os.path.join(DATA_FOLDER, 'newer_mapped_data.csv')
OUTPUT_FOLDER = os.path.join(DATA_FOLDER, 'ei_clusters')

def convert_to_ei_clusters(labels, data):
    # No Numbers, No punctuation, K & L remapped, space on its own
    SETS = {
        'alpha': ['q','w','e','r'],
        'bravo': ['a','s','d','z','x','c'],
        'charlie': ['f','g','v','b'],
        'delta': ['t','y','u','i'],
        'echo': ['h','j','n','m'],
        'foxtrot': ['o','p','k','l'],
        'space': ['space'],
        'backspace': ['backspace']
    }
    n_samples = data.shape[0]
    for key in SETS:
        sample_counter = 0
        for i in range(n_samples):
            if labels[i] not in SETS[key]: 
                continue
            sample_data = [['timestamp', 'mic0', 'mic1', 'mic2', 'mic3']]
            file_name = f'{OUTPUT_FOLDER}/{key}.sample{sample_counter}.csv'
            mic0_data = data[i][0:1*SAMPLES_PER_SENSOR]
            mic1_data = data[i][1*SAMPLES_PER_SENSOR:2*SAMPLES_PER_SENSOR]
            mic2_data = data[i][2*SAMPLES_PER_SENSOR:3*SAMPLES_PER_SENSOR]
            mic3_data = data[i][3*SAMPLES_PER_SENSOR:4*SAMPLES_PER_SENSOR]
            for j in range(SAMPLES_PER_SENSOR):
                sample_data.append([j*2, mic0_data[j], mic1_data[j], mic2_data[j], mic3_data[j]])
            with open(file_name, 'w') as f:
                # using csv.writer method from CSV package
                write = csv.writer(f)
                write.writerows(sample_data)
            sample_counter += 1

if __name__ == '__main__':
    with open(INPUT_FILE,'r') as dest_f:
        data_iter = csv.reader(dest_f,
                            delimiter = ',', quotechar='"')
        labels = []
        data = []
        for row in data_iter:
            if row[0] == ';':
                labels.append('semicolon')
            elif row[0] == '.':
                labels.append('period')
            elif row[0] == '/':
                labels.append('backslash')
            else:
                labels.append(row[0])
            data.append(row[1:])
    label_array = np.asarray(labels)
    data_array = np.asarray(data, dtype=float)
    convert_to_ei_clusters(label_array, data_array)