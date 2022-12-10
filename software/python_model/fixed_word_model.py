import numpy as np
from english_words import english_words_lower_alpha_set
import os

CURR_FOLDER = os.path.dirname(os.path.abspath(__file__))
COUNT_1W_FILE = os.path.join(CURR_FOLDER, 'count_1w.txt')
COUNT_2W_FILE = os.path.join(CURR_FOLDER, 'count_2w.txt')

# Edge Impulse Example Classifications of Localized Areas
# For letters in the word 'crock'
CROCK_POT=[[[['b','a','d','b','d'],
['f','f','f','c','f'],
['e','e','e','f','e']],
[[0.99, 1.0, 0.58, 0.95,0.36],
[0.0, 0.0, 0.42, 0.04,0.28],
[0.0,0.0,0.0,0.0,0.20]]],
# Edge Impulse Example Classifications of Localized Areas
# For letters in the word 'pot'
[[['d','f','d'],
['b','e','a'],
['f','d','f']],
[[0.32, 0.59, 0.97],
[0.19, 0.35, 0.02],
[0.17,0.05,0.0]]]]

# Edge Impulse Example Classifications of Localized Areas
# For letters in the word 'cut'
CUT_OFF=[[[['b','d','d'],
['c','a','b'],
['d','f','a']],
[[0.8, 0.97, 0.47],
[0.15, 0.02, 0.18],
[0.02, 0.00, 0.15]]],
# Edge Impulse Example Classifications of Localized Areas
# For letters in the word 'off'
[[['f','c','c'],
['d','f','c'],
['e','b','b']],
[[0.93, 0.29, 0.45],
[0.03, 0.23, 0.19],
[0.02, 0.18, 0.16]]]]

# Edge Impulse Example Classifications of Localized Areas
# For letters in the word 'the'
THE_COW_JUMPED_OVER_THE_MOON = [[[['d','e','a'],
['b','c','f'],
['e','f','e']],
[[0.33, 0.42, 1.00],
[0.29, 0.34, 0.0],
[0.11, 0.09, 0.0]]],
# Edge Impulse Example Classifications of Localized Areas
# For letters in the word 'cow'
[[['b','f','a'],
['f','e','f'],
['e','d','e']],
[[0.99, 0.66, 1.00],
[0.0, 0.16, 0.0],
[0.0, 0.12, 0.0]]],
# Edge Impulse Example Classifications of Localized Areas
# For letters in the word 'jumped'
[[['e','d','e','f','a','b'],
['c','b','c','e','f','f'],
['f','e','f','d','e','e']],
[[0.42, 0.33, 0.42, 0.66, 1.00, 0.99],
[0.34, 0.29, 0.34, 0.16, 0.0, 0.0],
[0.09, 0.11, 0.09, 0.12, 0.0, 0.0]]],
# Edge Impulse Example Classifications of Localized Areas
# For letters in the word 'over'
[[['f','c','a','a'],
['e','e','f','f'],
['d','b','d','e']],
[[0.66, 0.57, 1.00, 1.00],
[0.16, 0.20, 0.0, 0.0],
[0.12, 0.16, 0.0, 0.0]]],
# Edge Impulse Example Classifications of Localized Areas
# For letters in the word 'the'
[[['d','e','a'],
['b','c','f'],
['e','f','e']],
[[0.33, 0.42, 1.00],
[0.29, 0.34, 0.0],
[0.11, 0.09, 0.0]]],
# Edge Impulse Example Classifications of Localized Areas
# For letters in the word 'moon'
[[['e','f','f','e'],
['c','e','e','c'],
['f','d','d','f']],
[[0.42, 0.66, 0.66, 0.42],
[0.34, 0.16, 0.16, 0.34],
[0.09, 0.12, 0.12, 0.09]]]]

TEST_WORD = THE_COW_JUMPED_OVER_THE_MOON

if __name__ == '__main__':
    with open(COUNT_1W_FILE, "r") as file:
        tuple1 = [line.split() for line in file]
        tuple1 = list(map(lambda x: [x[0].lower(), x[1]], tuple1))
    with open(COUNT_2W_FILE, "r") as file:
        tuple2 = [line.split() for line in file]
        tuple2 = list(map(lambda x: [x[0].lower(), x[1].lower(), x[2]], tuple2))

    test_word = TEST_WORD
    
    for i in range(0, len(test_word), 2):
        word1 = test_word[i]
        word2 = test_word[i+1]
        #combine first two words into key as word1;word2
        #make list to dictionary
        lst = list(map(lambda words: ';'.join(words[0:2]), tuple2))
        tuple_dict={lst[i]:tuple2[i][2] for i in range(len(lst))}
        word_dict={tuple1[i][0]:tuple1[i][1] for i in range(len(tuple1))}

        data=list(word_dict.keys())
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
        threshold=0

        maximum=0
        if(len(tuples)!=0):
            maximum=max(tuple_probabilities)
        
        if(maximum>threshold):
            likely_word=tuples[tuple_probabilities.index(maximum)]
            print(likely_word, end=" ")
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
                print(likely_word,end=" ")

            word1 = word2
            word2 = [[[],[],[]], [[],[],[]]]
            word_on = 2

        #if still empty then just choose random word? or provide set of words