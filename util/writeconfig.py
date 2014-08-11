
import ConfigParser

'''
Create configuration file for this project
'''

config = ConfigParser.RawConfigParser()

config.add_section('KnowledgeBase')
# Knowledge base: 'wordnet', 'dbpedia', 'opencyc'
config.set('KnowledgeBase', 'kb', 'wordnet')

config.add_section('Relatedness')
# Relatedness type: one of 'definition', 'hybrid', 'structure'
config.set('Relatedness', 'rel_type', 'structure')
# Definition-based relatedness: level for connected concepts
config.set('Relatedness', 'def_level', '1')
# Definition-based relatedness: definition weight type
# for now supported are 'level_weight' and 'equal_weight'
config.set('Relatedness', 'def_weight', 'level_weight')
# Structure-based relatedness: maximum distance in the knowledge base
config.set('Relatedness', 'max_dist', '5')
# Hybrid relatedness: hybrid weight
config.set('Relatedness', 'h_weight', '0.3')
# Relatedness aggregation: 'average' or 'median'
config.set('Relatedness', 'aggreg', 'average')

config.add_section('Annotation')
# Annotation algorithm window size
config.set('Annotation', 'window_size', '2')
# Writing our configuration file to 'example.cfg'
with open('textannotation.cfg', 'wb') as configfile:
    config.write(configfile)