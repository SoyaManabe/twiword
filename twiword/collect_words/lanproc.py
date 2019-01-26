import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

def language(sentence):
    tokens = nltk.word_tokenize(sentence)
    return tokens