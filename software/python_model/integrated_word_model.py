import numpy as np
from numpy.lib.polynomial import poly1d
from collections import Counter
from english_words import english_words_lower_alpha_set
import serial

import os

CURR_FOLDER = os.path.dirname(os.path.abspath(__file__))
COUNT_1W_FILE = os.path.join(CURR_FOLDER, 'count_1w.txt')
COUNT_2W_FILE = os.path.join(CURR_FOLDER, 'count_2w.txt')

# # Serial port parameters
serial_speed = 921600

# EDIT THIS VALUE SPECIFIC TO YOUR DEVICE
serial_port = '' 

if __name__ == '__main__':
    letter_count = 0
    word_on = 1
    ser = serial.Serial(serial_port, serial_speed, timeout=1)

    with open(COUNT_1W_FILE, "r") as file:
        tuple1 = [line.split()for line in file]
        tuple1 = list(map(lambda x: [x[0].lower(), x[1]], tuple1))
    with open(COUNT_2W_FILE, "r") as file:
        tuple2 = [line.split() for line in file]
        tuple2 = list(map(lambda x: [x[0].lower(), x[1].lower(), x[2]], tuple2))

    word1 = [[[],[],[]], [[],[],[]]]
    word2 = [[[],[],[]], [[],[],[]]]

    while (True):
        data = ser.readline()
        if data:
            # print(data)

            alpha_val = float(data[2:7])
            bravo_val = float(data[10:15])
            charlie_val = float(data[18:23])
            delta_val = float(data[26:31])
            echo_val = float(data[34:39])
            foxtrot_val = float(data[42:47])
            space_val = float(data[50:55])

            probs = {
                'a': alpha_val,
                'b': bravo_val,
                'c': charlie_val,
                'd': delta_val,
                'e': echo_val,
                'f': foxtrot_val,
                's': space_val
            }
            
            sorted_probs = sorted(probs.items(), key=lambda kv: (kv[1], kv[0]))

            print(sorted_probs)
            # if(sorted_probs[-1][0] != 's' and word_on == 1):
            if(letter_count < 4 and word_on == 1):
                word1[0][0].append(sorted_probs[-1][0])
                word1[1][0].append(sorted_probs[-1][1])
                word1[0][1].append(sorted_probs[-2][0])
                word1[1][1].append(sorted_probs[-2][1])
                word1[0][2].append(sorted_probs[-3][0])
                word1[1][2].append(sorted_probs[-3][1])     
                letter_count += 1          
            elif(letter_count < 4 and word_on == 2):
                word2[0][0].append(sorted_probs[-1][0])
                word2[1][0].append(sorted_probs[-1][1])
                word2[0][1].append(sorted_probs[-2][0])
                word2[1][1].append(sorted_probs[-2][1])
                word2[0][2].append(sorted_probs[-3][0])
                word2[1][2].append(sorted_probs[-3][1])
                letter_count += 1
            if letter_count == 4:
                letter_count = 0
                if (word_on == 1):
                    word_on = 2
                else:
                    #combine first two words into key as word1;word2
                    #make list to dictionary
                    lst = list(map(lambda words: ';'.join(words[0:2]), tuple2))
                    tuple_dict={lst[i]:tuple2[i][2] for i in range(len(lst))}
                    word_dict={tuple1[i][0]:tuple1[i][1] for i in range(len(tuple1))}

                    data=list(english_words_lower_alpha_set)
                    data_clustered=data.copy()


                    seta={'q','w','e','r'}
                    setb={'a','s','d','z','x','c'}
                    setc={'f','g','v','b'}
                    setd={'t','y','u','i'}
                    sete={'h','j','n','m'}
                    setf={'o','p','k','l'}

                    #Transform dictionary words to clusters
                    for x in range(len(data)):
                        temp=""
                        for y in data[x]:
                            if y in seta:
                                temp+='a'
                            if y in setb:
                                temp+='b'
                            if y in setc:
                                temp+='c'
                            if y in setd:
                                temp+='d'
                            if y in sete:
                                temp+='e'
                            if y in setf:
                                temp+='f'
                        data_clustered[x]=temp

                    clustered_words_set=set(data_clustered)

                    #list cluster combinations and their probabilities for word 1. Omit if probability is 0.
                    num_choices=3 #number of top choices from model
                    num_possible=num_choices**len(word1[0][0])
                    possible_clusters_1=list()
                    probability_list_1=list()
                    for i in range(num_possible): #number of combinations
                        tempcomb=""
                        probability=1
                        for x in range(len(word1[0][0])): #length of word
                            tempcomb+=word1[0][(int)(i/(num_choices**x))%num_choices][x]
                            probability*=word1[1][(int)(i/(num_choices**x))%num_choices][x]
                        if (probability!=0) & (tempcomb in clustered_words_set):
                            possible_clusters_1.append(tempcomb)
                            probability_list_1.append(probability)

                    #list cluster combinations and probabilities for word 2
                    num_choices=3 #number of top choices from model
                    num_possible=num_choices**len(word1[0][0])
                    possible_clusters_2=list()
                    probability_list_2=list()
                    for i in range(num_possible): #number of combinations
                        tempcomb=""
                        probability=1
                        for x in range(len(word2[0][0])): #length of word
                            tempcomb+=word2[0][(int)(i/(num_choices**x))%num_choices][x]
                            probability*=word2[1][(int)(i/(num_choices**x))%num_choices][x]
                        if (probability!=0) & (tempcomb in clustered_words_set):
                            possible_clusters_2.append(tempcomb)
                            probability_list_2.append(probability)


                    possible_words_1=list()
                    word_probability_1=list()
                    possible_words_2=list()
                    word_probability_2=list()
                    #Attach clusters to words
                    for i in range(len(data_clustered)):
                        for j in range(len(possible_clusters_1)):
                            if data_clustered[i]==possible_clusters_1[j]:
                                possible_words_1.append(data[i])
                                word_probability_1.append(probability_list_1[j])
                        for j in range(len(possible_clusters_2)):
                            if data_clustered[i]==possible_clusters_2[j]:
                                possible_words_2.append(data[i])
                                word_probability_2.append(probability_list_2[j])

                    #key words to 2-tuple probabilities and find total probability of tuple
                    tuples=list()
                    tuple_probabilities=list()
                    for i in range(len(possible_words_1)):
                        for j in range(len(possible_words_2)):
                            if(tuple_dict.__contains__(possible_words_1[i]+";"+possible_words_2[j])):
                                tuples.append(possible_words_1[i]+" "+possible_words_2[j])
                                tuple_probabilities.append(int(tuple_dict[possible_words_1[i]+";"+possible_words_2[j]])*word_probability_1[i]*word_probability_2[j])

                    #find max probability tuple. if no tuple, or if tuple is not probably enough, move onto individually max likelihood word.
                    threshold=10

                    maximum=0
                    if(len(tuples)!=0):
                        maximum=max(tuple_probabilities)
                        print(maximum)
                    
                    if(maximum>threshold):
                        likely_word=tuples[tuple_probabilities.index(maximum)]
                        print(likely_word)
                        word_on = 1
                        word1 = [[[],[],[]], [[],[],[]]]
                        word2 = [[[],[],[]], [[],[],[]]]

                    else:
                        word1_guesses=list()
                        word1_guess_probabilities=list()
                        found=0
                        for i in range(len(possible_words_1)):
                            if(word_dict.__contains__(possible_words_1[i])):
                                word1_guesses.append(possible_words_1[i])
                                word1_guess_probabilities.append(int(word_dict[possible_words_1[i]])*word_probability_1[i])
                                found=1
                
                        if (found==0):
                            print(possible_words_1)

                        else:
                            maximum=max(word1_guess_probabilities)
                            likely_word=word1_guesses[word1_guess_probabilities.index(maximum)]
                            print(likely_word)

                        word1 = word2
                        word2 = [[[],[],[]], [[],[],[]]]
                        word_on = 2
                        #if still empty then just choose random word? or provide set of words