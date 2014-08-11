
import ConfigParser
import sys

from text import preprocess
import sliding_window

from relatedness import kbrelatedness
from knowledgebase import kbconfig

'''
Example code for annotating plain text received as an argument
'''

if __name__ == '__main__':

    text = sys.argv[1]
    
    config = ConfigParser.RawConfigParser()
    # the configuration file - see util.writeconfig for details
    config.read('textannotation.cfg')
    
    kb = config.get('KnowledgeBase', 'kb')
    window_size = config.getint('Annotation', 'window_size')
    level = config.getint('Relatedness', 'def_level')
    dweight = config.get('Relatedness', 'def_weight')
    rel_type = config.get('Relatedness', 'rel_type')
    max_dist = config.getint('Relatedness', 'max_dist')
    hweight = config.getfloat('Relatedness', 'h_weight')
    aggreg = config.get('Relatedness', 'aggreg')
    
    kb_graph, kb_bowdef = kbconfig.config(kb)
        
    # preprocess input text    
    doc = preprocess.document_tokens(text)
    
    # identify candidate concepts for the tokens
    token_concepts = preprocess.assign_concepts(kb_graph, doc)
    
    # create the relatedness object and set necessary parameters
    r = kbrelatedness.Relatedness(relatedness_type = rel_type, \
                                  kb_gr = kb_graph, kb_bow = kb_bowdef, \
                                  def_level = level, def_weight = dweight, \
                                  hybrid_weight = hweight, \
                                  struct_max_dist = max_dist, \
                                  aggregation = aggreg)
    
    # annotate tokens
    sliding_window.wsd(doc.tokens, token_concepts, window_size, r)
    
    # check annotation result
    for token_id, annotation in token_concepts.iteritems():
        try:
            print doc.tokens[token_id], \
            annotation.candidate_concepts[annotation.annotation_id]
        except:
            pass
    