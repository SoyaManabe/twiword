from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import *
t = Tokenizer()
text = "リンゴは英語でappleという"
token_filters = [POSKeepFilter('名詞'), TokenCountFilter()]
a = Analyzer(token_filters=token_filters)
for k, v in a.analyze(text):
    print('%s: %d' % (k,v))

def sep(texts):
    token_filters = [POSKeepFilter('名詞'), TokenCountFilter()]
    a = Analyzer(token_filters=token_filters)
    return a.analyze(texts)
