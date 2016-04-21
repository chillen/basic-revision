from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.util import ngrams
import operator

MAX_N = 3
FUTURE = "future"
PRESENT = "present"
PAST = "past"
sample = open("tenseText.txt").read()

# Adapted from stack overflow
# Very basic function, really just used for symbol reference
# http://stackoverflow.com/questions/30016904/determining-tense-of-a-sentence-python
def determine_most_tense_sentence(sentence):
    tagged = pos_tag( word_tokenize(sentence) )
    tense = {}
    tense[FUTURE] = len([word for word in tagged if word[1] == "MD"])
    tense[PRESENT] = len([word for word in tagged if word[1] in ["VBP", "VBZ", "VBG"]])
    tense[PAST] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])

    sortedTenses = sorted(tense.items(), key=operator.itemgetter(1))
    sortedTenses.reverse()

    return sortedTenses


def determine_primary_tense(sample):
    sentences = sent_tokenize(sample)
    tense = {}
    tense[FUTURE] = 0
    tense[PRESENT] = 0
    tense[PAST] = 0

    for sentence in sentences:
        most = determine_most_tense_sentence(sentence)[0][0]
        tense[most] += 1

    sortedTenses = sorted(tense.items(), key=operator.itemgetter(1))
    sortedTenses.reverse()
    return sortedTenses[0][0]

primaryTense = determine_primary_tense(sample)
print("Determined Summary Primary Tense: " + primaryTense)
print("Analyzing Text: Remember - All tenses should be "+primaryTense)

for sentence in sent_tokenize(sample):
    tenses = determine_most_tense_sentence(sentence)
    # Dumb check: The most used tense is incorrect
    if tenses[0][0] != primaryTense:
        print(" -- [Problem] Majority of sentence is of incorrect tense; \""+sentence+"\"")
    elif (tenses[1][1] + tenses[2][1]) != 0:
        print(" -- [Warning] Sentence may have a tense error; \""+sentence+"\"")
