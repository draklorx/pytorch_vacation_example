import nltk
import numpy
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

def create_vector(input, vocabulary):
    # setup an empty array to store the vector
    vector = []

    # split the input sentence into individual words and punctuation
    input_words = nltk.word_tokenize(input)
    # stem each word reducing it to a base word (running or runs becomes run for example)
    input_words = [stemmer.stem(input_word.lower()) for input_word in input_words]
    
    # loop over each input word
    for word in vocabulary:
        # if the input word is in the vocabulary, set the corresponding index to 1 else 0
        vector.append(1 if word in input_words else 0)

    # return the bag of words as a numpy array
    return vector

def get_pattern_words(intents) -> list[str]:
    words = []

    for intent in intents:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)

    words = [stemmer.stem(w.lower()) for w in words if w != ("?" or "!")]
    return sorted(list(set(words)))


def get_labels(intents) -> list[str]:
    labels: list[str] = []
    for intent in intents:
        labels.append(intent["tag"])

    return sorted(list(set(labels)))

def create_data(intents, words, labels):
    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for intent in intents:
        for pattern in intent["patterns"]:
            vector = create_vector(pattern, words)
            training.append(vector)
            output_row = out_empty[:]
            output_row[labels.index(intent["tag"])] = 1
            output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)
    return training, output
