# Data

This folder contains CSV files containing keypress data used for model training and testing for this project.

data.csv contains raw keypress data recorded from our ESP32 setup, where all data is written in one column.

clean_data.csv contains keypress data cleaned to a fixed number of sensor samples for each keypress, and each keypress occupying its own row, and each sensor value in time occupying its own column in that row.

mapped_data.csv contains the 12-bit keypress data from clean_data.csv remapped to an 8-bit value with a DC value of 50 subtracted from each sample.

The ei_clusters subdirectory contains an individual CSV file for each keypress trial, written in the desired format to be usable by Edge Impulse Studio for model generation. The description of the format of each file can be found in the software/training_scripts/README.md file of this project.