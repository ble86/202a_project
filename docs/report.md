# Table of Contents
* [Abstract](#0-abstract)
* [Introduction](#1-introduction)
* [Related Work](#2-related-work)
* [Technical Approach](#3-technical-approach)
* [Evaluation and Results](#4-evaluation-and-results)
* [Discussion and Conclusions](#5-discussion-and-conclusions)
* [References](#6-references)

# Abstract
Our project is to investigate an embedded systems-based methodology for identifiying a laptop or keyboard user's keystrokes. This project takes a hardware-based approach rather than a software-based approach to replicate a potential malicious attack on a user's computer. Our project is attempting to replicate vibrational-based sensing methods of machine learning identification problems investigated by research groups at Stanford, but to a smaller scale. In our project, vibrational sensors will be placed at the bottom of a laptop and/or keyboard and record vibrational patterns at multiple points of the laptop/keyboard chassis. Following this, a form of supervised or unsupervised learning model will be used to identify the keys that were pressed by the user and transmit those from a microcontroller to another device. The second device will then try to reconstruct the message that is being typed. Our goal is to have our system perform reasonably accurate keystroke identification such that a person separated from the keyboard may be able to deduce the information typed by the keyboard user.

# 1. Introduction

### 1.a. Motivation & Objective
Vibrational Sensor Approach to Malicious Keylogging is an attempt to prove the viability of a side channel attack on a keyboard. We record the vibrational information traveling through the keyboard to attempt to extract useful, potentially malicious, information about the true key activity of the keyboard. Such a proof of concept could potentially have real world implications for supply chains.

### 1.b. State of the Art & Its Limitations:
There has been some recent work on side channel attacks on keyboards. Notable methods rely on using smartphone accelerometers or microphones to sense typing on the phone or the typing on a nearby keyboard through propagated vibrations. The former was able to detect 4 digit passcodes on smartphones with a 61% success by using microphone access (Shumailov, 2019). While this is impressive, it is limited by the increasing use of “Allow access to microphone when open” permissions and also limiting permissions to non-trusted applications. It is also unable to classify more precise information, as password codes cover far larger regions on the phone compared to small keyboard icons.

The phone based vibration detection for nearby keyboards was able to achieve a high success rate for word classification as high as 80%, but omitted words of four letters of lower due to the difficulty and ambiguity in classifying these words. It also required access to the phone’s accelerometer, and proper local placement of the phone. It is subject to simple defenses, like making sure phones are not placed on desks, or injecting some noise into the medium intentionally.


### 1.c. Novelty & Rationale
The primary novelties to the project are the use of a dedicated system with contact microphones and the post processing we are doing to associate key clusters. A dedicated system, although more difficult and risky to deploy onto or inside a keyboard, is not subject to phone software security limitations. In addition, it allows for precise placement of the sensors, and hopefully higher fidelity when classifying letters, allowing us to classify smaller words. Various side channel analysis techniques have been demonstrated with sensing devices such as IMUs; however, to our knowledge there has yet to be an analysis done with a low cost contact microphone. Furthermore, as a result of our key clustering approach to localization we created a novel approach to infer words from key clusters. 

### 1.d. Potential Impact
Given the successful inference of keypress vibration data into words, we will have demonstrated the viability of a malicious side channel attack. Due to the nature of the attack, there would be no direct method for detection of the attack. Such a device could potentially be integrated into a keyboard during manufacturing or potentially embedded into a small form factor device and attached to a keyboard already deployed in the field.

### 1.e. Challenges
Perhaps the largest risk of our project is the uncertainty that contact microphones are not sensitive enough or operate in the desired band to pick up on the needed information to infer anything useful about the actual keys being pressed. Relevant work has shown the IMUs can be used to perform similar attacks; however, the use of contact mics is novel and we do not know if localization of key presses are possible using them. 

### 1.f. Project Goals/Requirements for Success
The overall goal of our project is to demonstrate a side channel attack where keystroke information can be inferred from its resulting vibration. We want to be able to detect individual key-press events from vibration data and record that data for training and classification. We also want to deploy an edge-based machine learning for key press classification. Finally, we want to communicate our classifications to a second device to verify classifications can be read by another user to represent malicious keylogging.

### 1.g. Metrics of Success
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


# 2. Related Work
Once we approached the limitation of how precisely our embedded model could classify keyboard areas, we needed to use natural language processing to classify words based on context. For individual words, this was closely related to an autocorrect problem. The simplest approach to autocorrect is by assigning nearby letters with an associated probability, and then to find the highest posterior probability. In our case, all letters in a cluster have equal probability, and letters in other clusters are assigned a probability based on the model’s assigned likelihood.

Once possible words have been developed with associated probabilities, we took inspiration from word suggestion problems to create likely combinations of words. Peter Norvig, a director of research at google, demonstrates how he walks through the problem using likely 2-tuple and 1-tuple word combination databases, and we adapted this approach using the same database for our implementation.

# 3. Technical Approach

### 3.a. Vibration Sensing and Amplification
The most basic requirement of the project is the ability to detect vibrational data from key presses. To achieve this, four contact microphones were attached to the back of the keyboard. These contact microphones originally had a very low signal power so an amplifier was used to amplify the signal approximately 10 times in the passband.

![Contact Mic](media/contact_mic.jpg)
Figure 1. Contact Microphones Attached to Keyboard

![Amplifier](media/amplifier.png)
Figure 2. Amplifier Design for 10x Gain of Microphone Signal

![ADC](media/adc.png)
Figure 3. ESP32 ADC Block Diagram

Next, the sensor data needed to be read and recorded by our embedded device. In order to achieve this one of the ESP32’s four ADCs were used. Originally the RTC ADC was used because it was accessible; however, the RTC ADC operates in the low power domain which means it is optimized for low power consumption. The RTC ADC configuration was subsequently abandoned for the DIG ADC. The DIG ADC is optimized for speed and throughput, leverages the I2S DMA to write samples directly to memory, and generates an interrupt when sampling is finished. Furthermore, there is a pattern table which can take up to 16 specific ADC commands. We leveraged this to read each four of our sensors in a round robin fashion.

![ESP](media/esp_flowchart.png)
Figure 4. Embedded Device Program Flow

Once sensor data is amplified and read, it needs to be sorted, qualified, scaled, and deployed. Each sample when read from memory is tagged with the channel it was read from. By leveraging this tag, each sample can be added to its respective queue and quickly sorted. The data also needs to be qualified as a keypress by measuring the average energy. This is done by squaring and summing all the sensor reading. Though not strictly necessary a baseline is subtracted from the sensor's value reading. This stops the energy level from becoming exceptionally high. Finally the data needs to be scaled and deployed. In this case we are scaling the data from 16 bit value to an 8 bit value and subtracting 50 from it. The shift from 12 bit data to 8 bit data is performed for compatibility with old training data. The subtraction of 50 was found experimentally and performs better in the edge impulse model than our unscaled data. The data is now ready to be fed into the machine learning model or offloaded for training.

### 3.b. Classification of Key Localization from Sensor Data
Once the data is scaled and properly formatted, all the data is provided to a new project in Edge Impulse Studio, a service that offers drag-and-drop design processes for signal processing and machine learning for embedded systems projects. Each sample keypress’s sensor data was provided to Edge Impulse through CSV files. 

Because contact microphones inherently deal with vibrational data, we were interested in looking at the frequency spectrum energies within the entire window of the vibrational keypress event. For this reason, we decided to use the spectral analysis and spectrogram signal processing blocks that Edge Impulse provides for us, in addition to using the raw data itself. 

The spectral analysis block takes windowed FFTs of a given size for each sensor in our raw data and calculates the overall energy of the frequency bins given by the FFT for each sensor across the sampling window. We found an optimal performance in separating features of the raw data when using a 256 point FFT across our sampling window of roughly 1 second. This causes some feature separation that makes it more distinguishable for a model to discern the different output classes.

![Features](media/feature_explorer.png)
Figure 5. Feature Scatter Plot for Classification of Spectral Analysis Data

Spectrograms, alternatively calculate FFT energies for given framed lengths of time within the sampling window and a specific stride of time between each energy calculation. Through trial and error, we found that optimal performance occurred when a 32 point FFT was applied to 20 millisecond frames and frames were spaced 30 milliseconds apart. 

![Spectrogram](media/spectrogram.png)
Figure 6. Example Output Spectrogram

Because we used 4 sensors, and each sensor had a set of feature vectors from the raw data, spectral analysis, and spectrogram, we decided to use a basic two layer 2D convolutional neural network to classify the data, treating each sensor as if it's a dimension of an image. Our convolutional network’s first layer had a convolutional/pool kernel size of 3 and 16 filters. The second layer used a convolutional/pool kernel size of 3 and 8 filters. Each convolutional/pool layer had a dropout of 0.1 applied after them to reduce overfitting. Reshape and flatten layers are added to the inputs and outputs of the model, respectively to ensure proper dimensioning from input to output.

![NN](media/nn_model.png)
Figure 7. Final Neural Network Architecture

Originally, we attempted to test this type of model on its own to classify what key was pressed on the embedded device. However, in our initial tests, this resulted in poor classification of 5%. Because of this poor accuracy, we attempted to classify localized areas of the keyboard instead of individual keys. This was a great success compared to individual keys, as our initial model’s test accuracy jumped to 17%. Because of this, we decided to move from classifying keys on target and move to classifying localized areas and communicate those areas to another device to run a word prediction model, which will be discussed in the next section. 

![Keys](media/key_model.png)
Figure 8. Initial Classification Accuracy Classifying for Individual Keys

![Clusters](media/cluster_model.png)
Figure 9. Initial Classification Accuracy Classifying for Localized Keyboard Areas

Through trial and error of the parameters of the signal processing blocks and by reassigning the localization areas based on the location of the sensors on the keyboard, we eventually managed to achieve a model accuracy of 72%, which we felt was sufficient to pass to a secondary model off-target to perform probabilistic word prediction. Furthermore, because our final model showed 100% accuracy at classifying the spacebar, this reaffirmed that we could use a probabilistic word prediction model since we would know when every word started and stopped.

![Final Model](media/final_model_acc.png)
Figure 10. Final Classification Accuracy of CNN Model

### 3.c. Word Prediction Model
Two observations we made at this point of the model are:
- The clustering was able to provide substantial information about the keypresses, but it alone was not able to form a precise prediction of words
- The space bar was consistently good for classification.

With this in mind, we implemented an off board language processing algorithm to utilize contextual information in generating likely words. We thought this was a realistic and reasonable approach, as the system only needs to send out one character per classification, which is the same as if it had fully classified the letter and desired to send the information out. In fact, in more power optimized implementations, this can be reduced to just 3 bits per key due to the smaller number of possible clusters. 
	
We utilized the high accuracy of space bar classification to separate and group key presses into words. Once we found this, we calculated all the possible words and the probability it was pressed. Then, we took the next words and found the relative probability that the 2-tuple existed. This was done by calculating the posterior probability (training data was uniform, so we did not divide by a constant):

$$
p(classification data|2tuple was typed)=[p(classification data|2tuple was typed) * p(2tuple was typed)]
$$

The first term in the right expression is the output of our training model, which returned the. Key presses are conditionally independent, so they were multiplied to find the total probability of the classification. The second probability is given by our dataset of 2-tuples.

In order to not overweight possible 2-tuples, as not all sets of 2 words are closely related in a sentence, we incorporated a threshold which, upon not being reached, would allow us to classify the single word based on 1-tuple probabilities. This is a naive implementation and can be improved through more complex NLP techniques, but it worked well for our test cases.


# 4. Evaluation and Results
Evaluating our system became a difficult challenge when we first attempted to deploy our Edge Impulse model on our embedded device. We found that for a given raw data sample that we knew to be in our training and test data, the classification that was given to that data point was different between Edge Impulse Studio and the on-target library that Edge Impulse generated. This situation occurred for both an ESP32 and an Arduino.

![Edge Impulse](media/ei.png)
Figure 11. Classification of test sample in Edge Impulse Studio. We can see that the alpha sample (noted by the first word in the sample name) is very confidently classified as alpha

![Arduino](media/arduino_model.png)
Figure 12. Classification of same test sample in generated Arduino library

Through discussing with a team member at Edge Impulse using their support page, we were told that this issue was a bug in Edge Impulse’s C++ SDK, and thus the poor classification on-target was an issue that was out of our control to fix and required an internal ticket to be developed for a still currently unresolved issue.

Despite this issue, we could still perform classification keypress events even though the classification may not be accurate. The video below shows an example of keypress events occurring and the resulting probabilities for each of the 7 localization areas printed to the terminal as a string.

[![Edge Classification](arduino_classification.png)](https://www.youtube.com/shorts/SFzgV2aLuNs)

Click the link above to open YouTube video demonstration

Our ESP32 could thus reliably determine when a keypress occurred and classify it as we expect it to. If we were to operate under the assumption of a fully working on-target model, these classifications would be sufficient to pass to our word prediction model to result in accurate keylogging.

One point to note is that in our system, the source of the vibrational data may not have always been a keypress that triggered the classification. For example, banging the table caused enough environmental vibrational noise that the model considered it a keypress. 

Additionally, because of the bug in the on-device model classification, we could no longer rely on the spacebar identification to accurately define the breaking of words for our word prediction model. Therefore, we imposed a limit to our word prediction model in order to obtain a fully functioning system.

For our word prediction model, we first tested the model using static probability values for cluster localization classifications of predefined words. We tested the phrases "cut off", "crock pot", and "the cow jumped over the moon". We used Edge Impulse Studio to create a localization classification for each letter of each phrase and manually coded those probabilities into an array for each phrase. Running the model with these static values, we got the following results.

![Cut Off](media/cut_off.png)
Figure 13. Word prediction from static probabilities of keyboard localization for the phrase "cut off"

![Crock Pot](media/crock_pot.png)
Figure 14. Word prediction from static probabilities of keyboard localization for the phrase "crock pot"

![The Cow](media/the_cow.png)
Figure 15. Word prediction from static probabilities of keyboard localization for the phrase "the cow jumped over the moon"

We see that for the phrases "cut off" and "crock pot" the predicted words match exactly what we expect. Additionally, we saw that the predictive model is able to absorb occasional mispredictions in the keyboard localization model where the desired letter cluster was the second or third most likely choice, as the context of the surrounding letters allows it to choose the best fitting word for the context.

As for the phrase "the cow jumped over the moon" the predicted phrase only replaced "cow" for "air". What we found here is that because the localizations in the word "air" perfectly overlap the localizations in the word "cow", the more probable phrase that was returned by the model based on the key clustering was "the air". This shows a flaw in our current system of two-word classification in that the model only picks the most probable two-word pairs, leaving out information of other pairs. Additionally, the larger context of the sentence is not able to contribute to the classification of previous words. Unfortunately we were unable to create large-scale validation with datasets such as books and texts due to the deployable model, so additional test cases were costly to develop. However, we were able to demonstrate that random word sets and sentences could be classified with our test data.

The video below shows a full demonstration of the embedded keypress system communicating with the off-target model. As mentioned before, we imposed a limitation to the word model since we could no longer trust the spacebar classification to separate words. The limitation we imposed is to assume all words are 4 letters long. As shown in the video below, we see that the system registers individual keypresses and after 4-8 keypresses it classifies single or two-word pairs, respectively. This leads us to believe that under a functioning edge model for keyboard localization, we would be able to achieve high accuracy predictions of typed words.

[![System Demo](https://img.youtube.com/vi/M0ijDe24-Xw/0.jpg)](https://www.youtube.com/watch?v=M0ijDe24-Xw)
Click the image above to open YouTube video demonstration


# 5. Discussion and Conclusions
Despite the Edge Impulse bug the project was still a relative success. The ESP32 seemed like a solid choice for this project and its ADC is capable of much more than what we were doing with it, however this was due largely to luck. In retrospect it would have made sense to evaluate the platform choice with more rigor. For example, had the ESP32 not had a capable DIG ADC we would have been forced to change platforms. Furthermore, choosing a platform with bluetooth included in the SOM would have let us achieve more potential project goals as our platform only had WiFi capabilities.

Unfortunately due to time constraints we did not have the option to look into deploying other machine learning models. Being that our deployed Edge Impulse model did work, having more time would have potentially allowed us to integrate another model. For example, Edge Impulse models are based on TensorFlow Lite. We could have potentially built our own two layer CNN using TensorFlow Lite and achieve similar results to our undeployed edge impulse model.

The word prediction model was successful in absorbing many errors in clustering classification, as well as selecting a letter from the cluster. We demonstrated it could create reasonable information from even 3 letter words, which had not been done before. It is still to be evaluated what the percentage error is in this over a large number of words and sentences. 

Finally, we believe there to be much more to investigate here in the future. Quality, placement, and number of contact mics should be further considered. For example, can we potentially achieve similar results with a small form factor custom embedded device and a single contact mic? Such an example would show the real world (potentially dangerous) use cases for our system, as it could be easily concealed. The type of sensor itself should also be considered. An IMU could potentially be a suitable replacement for the sensors in our system. Furthermore, an IMU typically measures at least three degrees of freedom in its sensing capabilities so given it is sensitive enough, much more data could potentially be learned about the key press.


# 6. References
Dong, Y., Fagert, J., Zhang, P. , Noh, H.Y. (2021). Non-parametric Bayesian Learning for Newcomer Detection using Footstep-Induced Floor Vibration. In Proceedings of the 20th International Conference on Information Processing in Sensor Networks (IPSN '21). Association for Computing Machinery, New York, NY, USA, 551–562. https://dl.acm.org/doi/pdf/10.1145/3412382.3458785

Norvig, P. (2011, November 22). Natural language corpus data: Beautiful data. Retrieved December 12, 2022, from http://norvig.com/ngrams/ 

Shumailov, I. Simon, L., Yan, J., Anderson, R. (2019). Hearing your touch: A new acoustic side channel on smartphones. https://doi.org/10.48550/arXiv.1903.11137

Marquardt, P., Verma, A., Carter, H., and Traynor., P. (2011). (Sp)iPhone: decoding vibrations from nearby keyboards using mobile phone accelerometers. In Proceedings of the 18th ACM conference on Computer and communications security (CCS '11). Association for Computing Machinery, New York, NY, USA, 551–562. https://doi.org/10.1145/2046707.2046771

Khurana, R., Nagaraja, S. (2013). Simple Defences against Vibration-Based Keystroke Fingerprinting Attacks. In: Christianson, B., Malcolm, J., Stajano, F., Anderson, J., Bonneau, J. (eds) Security Protocols XXI. Security Protocols 2013. Lecture Notes in Computer Science, vol 8263. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-642-41717-7_16 

Edge Impulse Studio: https://www.edgeimpulse.com/
