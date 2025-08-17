from pydoc import doc
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

    print(len(vector), len(vocabulary))
    # return the bag of words as a numpy array
    return vector

def get_vocab_data(intents):
    # setup return values
    words = []
    labels = []

    # setup documents
    docs_x = []
    docs_y = []

    # loop over intents
    for intent in intents:
        # for each intent loop over patterns
        for pattern in intent["patterns"]:
            # tokenize the words in the pattern
            wrds = nltk.word_tokenize(pattern)
            # extend the words list with the tokenized words
            words.extend(wrds)
            # add the tokenized words to the documents
            docs_x.append(wrds)
            # add the associated tag to the documents
            docs_y.append(intent["tag"])

        # add the tag to the labels if not already present
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    # stem words and remove some punctuation
    words = [stemmer.stem(w.lower()) for w in words if w != ("?" or "!")]
    # remove duplicates and sort
    words = sorted(list(set(words)))
    # sort labels
    labels = sorted(labels)

    # create training and output lists
    training = []
    output = []

    # create a zero array the same length as the number of labels
    out_empty = [0 for _ in range(len(labels))]

    # loop over each document
    for x, doc in enumerate(docs_x):
        # create the bag of words
        bag = []
        # stem each word in the document
        wrds = [stemmer.stem(w.lower()) for w in doc]

        # for each word in the vocabulary
        for w in words:
            # if the word is in the document
            if w in wrds:
                # append 1 to the bag
                bag.append(1)
            else:
                # append 0 to the bag
                bag.append(0)

        # create the output row
        output_row = out_empty[:]
        # set the corresponding index to 1
        output_row[labels.index(docs_y[x])] = 1

        # append the bag and output row to the training and output lists
        training.append(bag)
        output.append(output_row)

    # convert to numpy arrays
    training = numpy.array(training)
    output = numpy.array(output)
    return words, labels, training, output

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
