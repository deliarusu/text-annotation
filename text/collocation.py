
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import BigramAssocMeasures

def find_ngrams(tokens, n):
    
    '''
    Candidate ngrams from tokens
    
    :param tokens: the input tokens where to find ngrams
    :param n: ngram length, common values are 2 or 3
    :return: candidate ngrams
    '''
     
    candidate_ngrams = {}
    for i in range(len(tokens) - n + 1):
        ngr = ' '.join(tokens[i:i+n])
        candidate_ngrams.setdefault(ngr, 0)
        candidate_ngrams[ngr] += 1
  
    return candidate_ngrams

def bigram_collocations(corpus_words):
    
    '''
    Bigram collocations from words
    
    :param corpus_words: tokenized corpus
    :return collocations in corpus
    '''
    
    finder = BigramCollocationFinder.from_words(corpus_words)
    bigram_measures = BigramAssocMeasures()
    return finder.nbest(bigram_measures.pmi, 10)

