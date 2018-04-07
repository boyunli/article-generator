import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

from python.nlp.line2words import segment, BASE_DIR

def tfIdf(article):
    wordslist = segment(article)
    vectorizer = CountVectorizer(stop_words=stop_words())
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(wordslist))

    words = vectorizer.get_feature_names()
    weight = tfidf.toarray()

    n = 10
    tag = []
    for w in weight:
        loc = np.argsort(-w)
        for i in range(n):
            keyword = words[loc[i]]
            print('关键词:{}, weight:{}'.format(keyword, w[loc[i]]))
            tag.append(keyword)
    return ' '.join(tag)

def stop_words():
    file = '{}/stop_words.txt'.format(BASE_DIR)
    content = ''
    with open(file) as f:
        content = f.readlines()
    return [x.strip() for x in content]


