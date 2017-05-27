import gensim
model = gensim.models.Word2Vec.load('word2vec_wx')
def is_synonyms(s1,s2):
    try:
        return model.similarity(s1,s2)
    finally:
        return 0

