
from sklearn.feature_extraction.text import TfidfVectorizer

class Bow():
    
    '''
    Bag of Words representation of the knowledge base
    '''
    
    def __init__(self):
    
        '''
        Class constructor
        '''
        
        # corpus representing Knowledge Base definitions
        self.corpus = []
        
    def term_vector(self):
        
        '''
        Term vector associated with the corpus
        '''
        
        vectorizer = TfidfVectorizer(min_df = 1, \
                                     ngram_range=(1, 2), \
                                     token_pattern=r'\b\w+\b')
        self.T = vectorizer.fit_transform(self.corpus)  
        print self.T.shape
    
    def centroid(self, connected_concept_ids): 
        
        '''
        Compute the centroid for concept definitions identified
        by connected_concept_ids
        
        :param connected_concept_ids: the connected concept definitions
                                      for which a centroid is computed
        '''
        
        acc = None
        weight_sum = 0
        for cid, weight in connected_concept_ids.iteritems():
            if acc != None:
                temp = weight * self.T[cid]
                acc = acc + temp
            else:
                acc = weight * self.T[cid]  
            weight_sum += weight      
        acc /= weight_sum
        
        #print 'weight_sum', weight_sum
        
        return acc       
        
class WnBow(Bow):
    
    '''
    BOW representation for WordNet
    '''
    
    def __init__(self, wordnet):
        
        '''
        Class constructor
        '''
        
        Bow.__init__(self)
        self.wordnet = wordnet
        self.concept_ids = {}
    
    def wn_corpus(self):
        
        '''
        BOW corpus from concept definitions
        '''
        
        for synset in list(self.wordnet.all_synsets()):
                       
            s = synset.definition
            for ex in synset.examples:
                s += ' ' + ex
            self.corpus.append(s)
            self.concept_ids[synset.name] = len(self.corpus) - 1
            
                       
    def corpus_concept_ids(self, connected_concepts):
        
        '''
        Corpus ids for connected concepts
        
        :param connected_concepts: ids of connected concepts
        :return: ids of corpus definitions associated with the 
                 connected concepts
        '''
        
        ids = {}
        for c, w in connected_concepts.iteritems():
            #print c, self.corpus[self.concept_ids[c]]
            ids[self.concept_ids[c]] = w
        
        return ids
            