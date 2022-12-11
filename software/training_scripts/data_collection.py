from serial import Serial
import numpy as np
import os
import sys
import keyboard
import csv
import matplotlib.pyplot as plt
import time
import struct

BAUD_RATE = 921600
ESP32_PORT = ''
ESP32_DATA_WINDOW = 20
ESP32_TIMEOUT = 1


CURR_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(CURR_FOLDER, '../data')
OUTPUT_FILE = os.path.join(DATA_FOLDER, 'data.csv')
ESP_SER = Serial(port=ESP32_PORT, baudrate=BAUD_RATE, timeout=ESP32_TIMEOUT)
f=open(OUTPUT_FILE,'ab')

def plotter(Y):
    # x axis values
    x = []
    y = []
    for i in range(len(Y)):
        x.append(i)
        y.append(int(Y[i]))
    # plotting the points 
    plt.plot(x, y)
    
    # naming the x axis
    plt.xlabel('x - axis')
    # naming the y axis
    plt.ylabel('y - axis')
    plt.ylim(0, 200)
    
    # giving a title to my graph
    plt.title('Yayyy... A graph!')
    
    # function to show the plot
    plt.show()                

def wait_for_key_press():
    #print("Waiting to read key")
    press = keyboard.read_key()
    down = True
    while(True):
        if down:
            down = False
        else:
            # Stupid hack because read_key is registering both rising and falling edge
            # Should actually be an non issue but leaving this logic in case code gets faster or key edges are buffered
            return press

def append_to_csv(press, frame):
    print("Appending " + str(len(frame)) + " lines to csv")
    frame.insert(0, press)
    frame.insert(0, 'Key')
    frame.append('\n')
    
    np.savetxt(f, frame, delimiter=",", fmt="% s")



key_arr = []
def print_key_count(press):
    count = 0
    key_arr.append(press)
    key_arr.sort()
    old_item = ''
    for item in key_arr:
        if(item != old_item):
            print(item +" : "+ str(key_arr.count(item)) )
            old_item = item
    print("")    

def read_esp32():
    sample_arr = []
    sensor1_arr = []
    ESP_SER.reset_input_buffer()
    frame = ESP_SER.readline()[:-2]
    ESP_SER.reset_input_buffer()
    print("I recieved %d bytes" %(len(frame)))
    if(len(frame) == 8192):
        print("I recieved a valid frame")
        for i in range(0,len(frame)-4, 4):
            sample = frame[i:i+4]
            sample = struct.unpack('f', sample)
            sample_arr.append(sample[0])
#        for i in range(0, len(sample_arr), 4):
#            sensor1_arr.append(sample_arr[i])
#        plotter(sensor1_arr)
        return sample_arr
    else:
        print("I had junk in my serial buffer")
        return None

if __name__ == '__main__':
    print("Data Collection Tool Begin")
    #esp_ser = Serial(port=ESP32_PORT, baudrate=BAUD_RATE, timeout=ESP32_TIMEOUT)
    
    while(True):
        key = wait_for_key_press()
        if(key == 'ctrl'):
            f.close()
            sys.exit(0)
        else:
            if(key == '\u2212'):
                key = '-'
            sensor_frame = read_esp32()
            if(sensor_frame != None):
                print_key_count(key)
                append_to_csv(key, sensor_frame)
