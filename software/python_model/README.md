# Python Word Probability Model

## File Summary

The two Python files, fixed_word_model.py and integrated_word_model.py, are two scripts for two methods of running a word probability model based on likely letters in the word.

### fixed_word_model.py

fixed_word_model.py is implemented with a few hard-coded examples from Edge Impulse Studio's classifications for localized areas of a keyboard using vibrational data from four contact microphones placed on the bottom of the keyboard. 

Each hard-coded example uses a multi-dimensional array. The first dimension is separate words ("the", "cow", "jumped"). The second dimension separates lists of classified localization areas from lists of probabilities. The third dimension classifies the most likely localization area, second most likely localization area, etc. and corresponding probabilities. Then the last dimension is each letter within a single word ("t", "h", "e").

The user can choose one of the multiple hard-coded examples to run by changing the TEST_WORD constant on line 92 to one of the word constants coded above it.

Running this Python will result in one word/phrase/sentence prediction from static localization classifications.

### integrated_word_model.py

integrated_word_model.py is implemented to be integrated with the embedded system which performs on-target classification for localized areas of a keyboard using vibrational data from four contact microphones placed on the bottom of the keyboard. 

The script stores each keypress from the embedded system as a single element of a multi-dimensional array arranged in the same manner as in fixed_word_model.py. However, classifications are only made on two word sets at a time. 

Furhtermore, each word is imposed with a four letter classification limit due to unresolved errors in generated Arduino library for on-device implementation of Edge Impulse's model given by Edge Impulse.

Running this Python will result in continuous word/phrase/sentence prediction from static localization classifications.

### count_1w.txt and count_2w.txt

These files provide dictionary likelihoods of single words and two word combinations and are used as a reference for predicting words and phrases from keypress localizations.

## Running the scripts

In order to run fixed_word_model.py, ensure you are using the suggested virtual environment setup as described in the top-level software README. 

Change line 92 in fixed_word_model.py to perform the desired word/phrase classification.

Run the following command:
```
python3 fixed_word_model.py
```

In order to run integrated_word_model.py, ensure you are using the suggested virtual environment setup as described in the top-level software README. 

Connect the embedded keypress classification device to a USB serial port on your personal computing device.

Change line 17 in integrated_word_model.py to set the file reference for the serial port used by your computer to communicate with the embedded device (Linux/Mac method of referring to devices).

Run the following command:
```
python3 integrated_word_model.py
```

Typing multiple keypresses should result in printouts on the screen of each keypresses localization probabilities and after multiple keypresses, a one or two-word prediction will be printed to the screen.

The script can be terminated by unplugging the embedded device.
