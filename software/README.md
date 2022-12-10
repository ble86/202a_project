# Software

The following describes the folder structure for all software programs used for this project and how to run the full system.

## File Summary

training_scripts contains Python scripts used to collect raw sensor data, clean the data, remap the data values, and convert the data into CSV files usable by Edge Impulse for generating a model for isolating keyboard localization clusters.

python_model contains scripts for running a static word/phrase prediction from known localization probabilities given by Edge Impulse as well as running a system-integrated word/phrase prediction from live, on-target classification of localized keyboard clusters.

arduino contains example projects for getting the Edge Impulse Model running on an Arduino Nano RP2040 despite not being used in the final product.

ei-mapped-range-arduino-1.0.6.zip contains the library for the Edge Impulse classification used for both the Arduino and ESP32 to perform classification on device.

## Run programs

Prior to running any Python scripts, perform the following commands to generate the recommended virtual environment.

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Training

To perform training, follow the instructions in the training_scripts/README.md file.

### Word Prediction Model
To perform word prediction, follow the instructions in the python_model/README.md file.

### Run Final System
To run the final system, simply follow the instructions to run the ESP32 code to flash the ESP32 program, then follow the instructions to run the word prediction model on your personal computer, with the flashed ESP32 connected to your personal computer through the USB connection. 