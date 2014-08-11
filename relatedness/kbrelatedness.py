
from util import exception

DEFINITION = 'definition'
HYBRID = 'hybrid'
STRUCTURE = 'structure'

class Relatedness(object):
    
    '''
    Relatedness class
    
    kb_gr: the knowledge base graph
    kb_bow: the BOW representation of the knowledge base definitions
    def_level: connected concepts level (see relatedness definition)
    def_weight: weight for definition relatedness 
    hybrid_weight: weight for hybrid relatedness 
    struct_max_dist: maximum distance in the knowledge base
    aggregation: how to aggregate relatedness (AVERAGE, MEDIAN, None)
    '''

    kb_gr = None
    kb_now = None
    aggregation = None
    def_level = None
    def_weight = None
    struct_max_dist = None
    hybrid_weight = None
    relatedness_type = None

    def __init__(self, relatedness_type, kb_gr = None, kb_bow = None, \
                 def_level = None, def_weight = None, \
                 hybrid_weight = None, struct_max_dist = None, \
                 aggregation =  None):
        
        '''
        Class constructor
        '''
        
        self.kb_gr = kb_gr
        self.kb_bow = kb_bow
        
        self.def_level = def_level
        self.def_weight = def_weight
        
        self.hybrid_weight = hybrid_weight
        
        self.struct_max_dist = struct_max_dist
        
        self.aggregation = aggregation
        
        self.relatedness_type = relatedness_type
        
    def relatedness_definition(self, concept1, concept2):
    
        '''
        Definition-based relatedness between two concepts
        
        :param concept1: concept
        :param concept2: concept
        :return: relatedness between concept1 and concept2
        '''
    
        if self.kb_gr == None:
            raise exception.RelatednessException(self.kb_gr, \
                               'Knowledge base graph cannot be None')
        elif self.kb_bow == None:
            raise exception.RelatednessException(self.kb_bow, \
                               'Knowledge base BOW cannot be None')
        elif self.def_weight == None:
            raise exception.RelatednessException(self.def_weight, \
                               'Definition-based relatedness ' \
                               'definition weight cannot be None')
        elif self.def_level == None:
            raise exception.RelatednessException(self.def_level, \
                               'Definition-based relatedness ' \
                               'connected concept level cannot be None')
    
        connected_concepts1 = self.kb_gr.connected_concepts(concept1, \
                          self.def_level, self.def_weight)
        connected_concepts2 = self.kb_gr.connected_concepts(concept2, \
                          self.def_level, self.def_weight)
    
        connected_concept_ids1 = \
            self.kb_bow.corpus_concept_ids(connected_concepts1)
        connected_concept_ids2 = \
            self.kb_bow.corpus_concept_ids(connected_concepts2)
    
        extended_def1 = self.kb_bow.centroid(connected_concept_ids1).toarray()
        extended_def2 = self.kb_bow.centroid(connected_concept_ids2).toarray()
    
        K = (extended_def1 * extended_def2).sum()
     
        '''
        print 'Extended1 = ' + str(extended_def1[:,:10]) + \
        ', dim = ' + str(extended_def1.shape) + \
        ', type = ' + str(type(extended_def1))
        print 'Extended2 = ' + str(extended_def2[:,:10]) + \
        ', dim = ' + str(extended_def2.shape) + \
        ', type = ' + str(type(extended_def2))
        print 'K = ' + str(K) + ', dim = ' + \
        str(K.shape) + ', type = ' + str(type(K))
        '''
        
        return K
    
    def distance_structure(self, concept1, concept2):
        
        '''
        The distance between two concepts in the knowledge base
        represented as a graph
        
        :param concept1: concept
        :param concept2: concept
        :return: relatedness between concept1 and concept2        
        '''
    
        distance = self.kb_gr.weighted_concept_path(concept1, concept2)
        
        return distance 
    
    def relatedness_structure(self, concept1, concept2):
        
        '''
        The relatedness between two concepts in the knowledge base
        represented as a graph
        
        :param concept1: concept
        :param concept2: concept
        :return: relatedness between concept1 and concept2        
        '''    
    
        if self.kb_gr == None:
            raise exception.RelatednessException(self.kb_gr, \
                               'Knowledge base graph cannot be None')
    
        distance = self.kb_gr.weighted_concept_path(concept1, concept2)
        
        max_dist = self.struct_max_dist
        if self.struct_max_dist == None and \
            self.kb_gr.max_dist != None:
            max_dist = self.kb_gr.max_dist
    
        if max_dist == None:
            raise exception.RelatednessException(max_dist, \
                'Maximum distance in the knowledge base cannot be None')
    
        relatedness = 1 - float(distance)/max_dist
        
        return relatedness
    
    def relatedness_hybrid(self, concept1, concept2):
    
        '''
        Determines the hybrid relatedness between two concepts. 
        Returns the hybrid relatedness.    
    
        :param concept1: concept
        :param concept2: concept
        :return: relatedness between concept1 and concept2        
        '''
    
        if self.hybrid_weight == None or self.hybrid_weight == 0:
            raise exception.RelatednessException(self.hybrid_weight, \
                               'Unsupported hybrid weight')
    
        rel_def = self.relatedness_definition(concept1, concept2)
    
        rel_struct = self.relatedness_structure(concept1, concept2)
    
        rel_hybrid = self.hybrid_weight * rel_def + \
            (1 - self.hybrid_weight) * rel_struct
    
        return rel_hybrid
    
    def compute(self, concept1, concept2):
        
        '''
        Compute relatedness between two concepts
        
        :param concept1: concept
        :param concept2: concept
        :return: relatedness between concept1 and concept2        
        '''
                
        if self.relatedness_type == None:
            raise exception.RelatednessException(self.relatedness_type, \
                               'Relatendness type cannot be None, but one of ' \
                               'DEFINITION, STRUCTURE, HYBRID')
        elif self.relatedness_type == DEFINITION:
            return self.relatedness_definition(concept1, concept2)
        elif self.relatedness_type == STRUCTURE:
            return self.relatedness_structure(concept1, concept2)
        elif self.relatedness_type == HYBRID:
            return self.relatedness_hybrid(concept1, concept2)
        else:
            raise exception.RelatednessException(self.relatedness_type, \
                               'Unsupported hybrid weight')        
    
        