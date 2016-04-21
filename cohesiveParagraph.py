from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from collections import Counter as mset
from collections import defaultdict
import numpy as np
import operator
import nltk

# Inspired by summary builder
# https://thetokenizer.com/2013/04/28/build-your-own-summary-tool/

sample = open("cohesiveText.txt").read()

print("[NOTE] If this is the first time run, NLTK will download necessary word lists.")
nltk.download('punkt')
nltk.download('wordnet')


regToken = RegexpTokenizer(r'\w+') # Get rid of pesky punctuation
sentences = sent_tokenize(sample)
sentenceCount = {}
count = 0
THRESH = 1 # How many stdev until it's not cohesive?

def intersect_value(s1, s2):
    s1 = regToken.tokenize(s1)
    s2 = regToken.tokenize(s2)
    normalizer = (len(s1) + len(s2)) / 2
    intersect = 0
    # Find an intersection, but also look at similarities
    for w1 in s1:
        synw1 = wn.synsets(w1);
        if len(synw1) > 0:
            synw1 = synw1[0]
        else:
            continue
        for w2 in s2:
            synw2 = wn.synsets(w2)
            if len(synw2) > 0:
                synw2 = synw2[0]
            else:
                continue
            similar = wn.wup_similarity(synw1, synw2)
            if similar is not None:
                #if similar != 1:
                #    similar /= 2
                intersect += similar

    #normalize to the size of each sentence
    return intersect# / normalizer

for i in range(len(sentences)):
    s1 = sentences[i]
    sentenceCount[s1] = 0
    for j in range(len(sentences)):
        s2 = sentences[j]
        if i != j:
            sentenceCount[s1] += intersect_value(s1, s2)

sentenceCount = sorted(sentenceCount.items(), key=operator.itemgetter(1))
sentenceCount.reverse()

# Find std dev
stdDev = np.std([sentence[1] for sentence in sentenceCount])
mean = sum([sentence[1] for sentence in sentenceCount]) / len([sentence[1] for sentence in sentenceCount])
#print([sentence[1] for sentence in sentenceCount])

print(" ----- BEGIN PROGRAM -----")

print("Provided Sample: " + sample)
print("\nAnalyzing Text... \n")

print("Evaluated Text: Cohesion score left, sentence right\n")
for sentence, score in sentenceCount:
    #print(sentence)
    print("[{0:4.2f}] \"{1:20s}\"".format(score, sentence))
    
print("\nStd: " + str(stdDev) + "; Mean: " + str(mean) + "; Thresh: " + str(mean - THRESH*stdDev) + "\n")
for sentence in sentenceCount:
    if mean - THRESH*stdDev > sentence[1]:
        print("\n[Problem] This sentence seems unrelated to the rest of the paragraph:\n\t \'"+sentence[0]+"\"")
