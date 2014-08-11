
import ConfigParser

from relatedness import kbrelatedness
from knowledgebase import kbconfig

'''
Example code for determining the relatedness between concepts
'''

if __name__ == '__main__':
   
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
    
    r = kbrelatedness.Relatedness(relatedness_type = rel_type, \
                                  kb_gr = kb_graph, kb_bow = kb_bowdef, \
                                  def_level = level, def_weight = dweight, \
                                  hybrid_weight = hweight, \
                                  struct_max_dist = max_dist) 
    
    r.relatedness_type = 'definition'
    d = r.compute('physical_entity.n.01', 'entity.n.01')
    print 'Def', d
    
    r.relatedness_type = 'structure'
    s = r.compute('physical_entity.n.01', 'entity.n.01')
    print 'Struct', s
    
    r.relatedness_type = 'hybrid'
    h = r.compute('physical_entity.n.01', 'entity.n.01')
    print 'Hybrid', h
    
    print kb_graph.connected_concepts('entity.n.01', 2)
    
    