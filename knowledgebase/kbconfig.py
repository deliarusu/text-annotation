
import kbbow, kbgraph
from nltk.corpus import wordnet as wn

WORDNET = 'wordnet'
DBPEDIA = 'dbpedia'
OPENCYC = 'opencyc'

def config_wn():
    
    '''
    Create WordNet NetoworkX graph and BOW objects
    
    :return: WordNet graph and BOW objects
    '''
    
    # WordNet graph
    wn_gr = kbgraph.WnGraph(wn)
    wn_gr.build_graph()
       
    # WordNet BOW
    wn_bow = kbbow.WnBow(wn)
    wn_bow.wn_corpus()
    wn_bow.term_vector()
    
    return wn_gr, wn_bow

def config(kb):
    
    '''
    Create graph and BOW objects for different knowledge bases
    
    :param kb: the knowledge base id
    :return: knowledge base graph and BOW objects
    '''
    
    if kb == 'wordnet':
        return config_wn()
    elif kb == 'dbpedia':
        raise NotImplementedError()
    elif kb == 'opencyc':
        raise NotImplementedError() 
        