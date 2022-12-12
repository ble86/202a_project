# Project Proposal

## 1. Motivation & Objective
Vibrational Sensor Approach to Malicious Keylogging is an attempt to prove the viability of a side channel attack on a keyboard. We record the vibrational information traveling through the keyboard to attempt to extract useful, potentially malicious, information about the true key activity of the keyboard. Such a proof of concept could potentially have real world implications for supply chains.

## 2. State of the Art & Its Limitations

## 3. Novelty & Rationale
The primary novelties to the project are the use of contact microphones and the post processing we are doing to associate key clusters. Various side channel analysis techniques have been demonstrated with sensing devices such as IMUs; however, to our knowledge there has yet to be an analysis done with a low cost contact microphone. Furthermore, as a result of our key clustering approach to localization we created a novel approach to infer words from key clusters. ERIC EXPLAIN PLZZZ

## 4. Potential Impact
Given the successful inference of keypress vibration data into words, we will have demonstrated the viability of a malicious side channel attack. Due to the nature of the attack, there would be no direct method for detection of the attack. Such a device could potentially be integrated into a keyboard during manufacturing or potentially embedded into a small form factor device and attached to a keyboard already deployed in the field.

## 5. Challenges
Perhaps the largest risk of our project is the uncertainty that contact microphones are not sensitive enough or operate in the desired band to pick up on the needed information to infer anything useful about the actual keys being pressed. Relevant work has shown the IMUs can be used to perform similar attacks; however, the use of contact mics is novel and we do not know if localization of key presses are possible using them. 

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
