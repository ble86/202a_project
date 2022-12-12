# Project Proposal

## 1. Motivation & Objective
Vibrational Sensor Approach to Malicious Keylogging is an attempt to prove the viability of a side channel attack on a keyboard. We record the vibrational information traveling through the keyboard to attempt to extract useful, potentially malicious, information about the true key activity of the keyboard. Such a proof of concept could potentially have real world implications for supply chains.

## 2. State of the Art & Its Limitations
There has been some recent work on side channel attacks on keyboards. Notable methods rely on using smartphone accelerometers or microphones to sense typing on the phone or the typing on a nearby keyboard through propagated vibrations. The former was able to detect 4 digit passcodes on smartphones with a 61% success by using microphone access (Shumailov, 2019). While this is impressive, it is limited by the increasing use of “Allow access to microphone when open” permissions and also limiting permissions to non-trusted applications. It is also unable to classify more precise information, as password codes cover far larger regions on the phone compared to small keyboard icons.

The phone based vibration detection for nearby keyboards was able to achieve a high success rate for word classification as high as 80%, but omitted words of four letters of lower due to the difficulty and ambiguity in classifying these words. It also required access to the phone’s accelerometer, and proper local placement of the phone. It is subject to simple defenses, like making sure phones are not placed on desks, or injecting some noise into the medium intentionally.

## 3. Novelty & Rationale
The primary novelties to the project are the use of a dedicated system with contact microphones and the post processing we are doing to associate key clusters. A dedicated system, although more difficult and risky to deploy onto or inside a keyboard, is not subject to phone software security limitations. In addition, it allows for precise placement of the sensors, and hopefully higher fidelity when classifying letters, allowing us to classify smaller words. Various side channel analysis techniques have been demonstrated with sensing devices such as IMUs; however, to our knowledge there has yet to be an analysis done with a low cost contact microphone. Furthermore, as a result of our key clustering approach to localization we created a novel approach to infer words from key clusters. 

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
Dong, Non-parametric Bayesian Learning for
Newcomer Detection using Footstep-Induced Floor Vibration: https://dl.acm.org/doi/abs/10.1145/3412382.3458785

Shumailov, acoustic side channel attack on smart phone passcodes: https://doi.org/10.48550/arXiv.1903.11137

Marquardt, using phone accelerometers to detect vibrations from nearby keyboards and classifying words: https://doi.org/10.1145/2046707.2046771

Khurana, defense against phone accelerometer side channel attacks: https://doi.org/10.1007/978-3-642-41717-7_16

### 9.b. Datasets
1w_count and 2w_count datasets by Norvig for word and bigram probabilities

### 9.c. Software
Python for training scripts and word prediction model 

Edge Impulse Studio for model generation

C and Arduino for Embedded Programming

## 10. References
Dong, Y., Fagert, J., Zhang, P. , Noh, H.Y. (2021). Non-parametric Bayesian Learning for Newcomer Detection using Footstep-Induced Floor Vibration. In Proceedings of the 20th International Conference on Information Processing in Sensor Networks (IPSN '21). Association for Computing Machinery, New York, NY, USA, 551–562. https://dl.acm.org/doi/pdf/10.1145/3412382.3458785

Norvig, P. (2011, November 22). Natural language corpus data: Beautiful data. Retrieved December 12, 2022, from http://norvig.com/ngrams/ 

Shumailov, I. Simon, L., Yan, J., Anderson, R. (2019). Hearing your touch: A new acoustic side channel on smartphones. https://doi.org/10.48550/arXiv.1903.11137

Marquardt, P., Verma, A., Carter, H., and Traynor., P. (2011). (Sp)iPhone: decoding vibrations from nearby keyboards using mobile phone accelerometers. In Proceedings of the 18th ACM conference on Computer and communications security (CCS '11). Association for Computing Machinery, New York, NY, USA, 551–562. https://doi.org/10.1145/2046707.2046771

Khurana, R., Nagaraja, S. (2013). Simple Defences against Vibration-Based Keystroke Fingerprinting Attacks. In: Christianson, B., Malcolm, J., Stajano, F., Anderson, J., Bonneau, J. (eds) Security Protocols XXI. Security Protocols 2013. Lecture Notes in Computer Science, vol 8263. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-642-41717-7_16 

Edge Impulse Studio: https://www.edgeimpulse.com/

