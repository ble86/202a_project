# Project Proposal

## 1. Motivation & Objective

## 2. State of the Art & Its Limitations

## 3. Novelty & Rationale

## 4. Potential Impact

## 5. Challenges

## 6. Requirements for Success 
The overall goal of our project is to demonstrate a side channel attack where keystroke information can be inferred from its resulting vibration. We want to be able to detect individual key-press events from vibration data and record that data for training and classification. We also want to deploy an edge-based machine learning for key press classification. Finally, we want to communicate our classifications to a second device to verify classifications can be read by another user to represent malicious keylogging.

## 7. Metrics of Success
The specific steps needed to complete a system that has the ability to classify vibration based key presses was logically broken into three separate systems. The embedded system, the machine learning model, and secondary device, each with their separate metrics of success.

Our embedded system must have the ability to CONTINUOUSLY:
1. Detect vibration events. In this case the vibration events are key presses and only key presses.
2. Record key press event sensor data for further use (classification/training) at a high sampling rate
3. Deploy an edge-based machine learning model
4. Communicate classifications to a secondary device

Our machine learning model must have the ability to:
1. Process and scale data for classification
2. Perform classification of keypresses with high accuracy (>65%) on raw sensor data

Our secondary device must have the ability to:
1. Accept classification data from the embedded device 
2. Decipher the received data and display it as human-readable words to represent keylogging

## 8. Execution Plan
Eric and Graham plan to work on the circuit implementation and embedded programming of the ESP32 training and test programs for classification of keypress events. Brandon plans on creating an Edge Impulse Studio project to generate a model to classify keypresses from the vibrational data.

## 9. Related Work

### 9.a. Papers

### 9.b. Datasets

### 9.c. Software

## 10. References
