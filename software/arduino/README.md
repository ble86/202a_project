# Arduino Programs

The two folders here contain two projects used to run a classification model on an Arduino Nano RP2040 for keypress localization classification.

The ei_model project communicates with an ESP32 to receive ADC sensor data, through serial pins, map the data as done with Edge Impulse training, and classify the keypress.

The static_buffer project contains the base code for running classification from a single buffer containing a hard-coded raw feature vector (corresponding to a known training data value). This was used to debug the issue of incompatible classifications between Edge Impulse Studio and on-target model.

These Arduino projects ended up not being used for the final version of the system.

