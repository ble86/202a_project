# Training Scripts

The four Python scripts in this directory describe the process of collecting the raw sensor data and outputting it to a csv, cleaning the csv file, mapping the data to a new range values, and processing those new values to separate them into a CSV format expected by Edge Impulse Studio for model creation.

## data_collection.py
This file is used to collect raw keypress sensor data and output it to a CSV.

Perform the following steps to run this:
- Ensure that the suggested virtual environment has been set up as written in the software/ directory
- Follow the instructions in software/embedded/README.md to flash the ESP32 with the corresponding C code to perform sensor reading
- Change line 12 in data_collection.py to set the file reference for the serial port used by your computer to communicate with the embedded device (Linux/Mac method of referring to devices)
- Connect the USB cable from the remote keyboard to your personal computer. This will act as your new standard input source for the program
- Execute the command
```
python3 data_collection.py
```
- One by one hit a single key on the keyboard used for sampling, leaving some time between key presses. The data will be recorded continuously for approximately one second every time a key is hit.
- Quit the program by hitting the 'Ctrl' key
- The script should output a file data.csv in the data folder of this project.

## clean_data.py
This file is used to take the output CSV, where all information for multiple keypresses are written in one column, and clean it such that each keypress is written into an individual row, and each sensor value in time is written in a new column.

Perform the following steps to run this:
- Ensure that collect_data.py has been run to generate raw CSV data
- Execute the command 
```
python3 clean_data.py
```
- The script should output a file clean_data.csv in the data folder of this project.

## map_data.py
This file is used to take the cleaned CSV, and map each 12-bit sensor value to an 8-bit value and subtract a DC offset value of 50 from each value(empirically discovered).

Perform the following steps to run this:
- Ensure that collect_data.py and clean_data.py has been run to generate clean CSV data
- Execute the command 
```
python3 map_data.py
```
- The script should output a file mapped_data.csv in the data folder of this project.

## data_processing.py
This file is used to take the mapped CSV, containing data for each keypress, and separating the data to be samples associated for a preset localization cluster for each key.

The mapping of key to localization cluster can be found on line 15 of the file.

Edge Impulse Studio expects a single test sample with multiple sensor values to be in the following format:

timestamp,sensor1,sensor2,sensor3

0,sensor1[0],sensor2[0],sensor3[0]

2,sensor1[2],sensor2[2],sensor3[2]

etc.

It also expects data CSV files to be named in the following format

classification_label.unique-id.csv

This script handles taking the mapped sensor data and reassociating each keypress to an individual CSV file following the expected Edge Impulse format.

Perform the following steps to run this:
- Ensure that collect_data.py and clean_data.py, and map_data.py has been run to generate mapped CSV data
- Execute the command 
```
python3 data_processing.py
```
- The script should output multiple CSV files in the data/ei_clusters folder of this project in the format described above