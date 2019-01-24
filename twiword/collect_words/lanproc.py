import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

def language(sentence):
    token = nltk.word_tokenize(sentence)
    return nltk.pos_tag(token)