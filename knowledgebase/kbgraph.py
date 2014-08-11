
'''
Graph representation of the knowledge base
'''

import networkx as nx
import math
import sys
from util import exception

MAXLOGDEG = 'maxlogdeg'
SQRTLOGDEG = 'sqrtlogdeg'
MAX_LEVEL = 5
EQUAL_WEIGHT = 'equal_weight'
LEVEL_WEIGHT = 'level_weight'

EPSILON = sys.float_info.epsilon

class Graph(object):
    
    '''
    Graph representation for a generic lexical database
    '''

    def __init__(self):
        
        '''
        Class constructor
        '''
        
        # Networkx graph
        self.G = nx.Graph() 
        
        # all shortest path distances in the graph
        self.all_dist = {}
        
        # maximum distance between nodes in the graph
        self.max_dist = None
    
    def node_degree(self, node):
        
        '''
        Degree of a node in the WordNet graph
        '''
        
        return self.G.degree(node)
    
    def weight_graph(self, weight):
        
        '''
        Add weights to the node edges
        
        :param weight: weight type 'maxlogdeg' or 'sqrtlogdeg'
        '''
        
        if weight != MAXLOGDEG and weight != SQRTLOGDEG:
            raise exception.GraphException(weight, 'Undefined graph weight')
        
        for edge in self.G.edges_iter():
            #print edge, edge[0], edge[1]
            
            deg_node1 = self.node_degree(edge[0])
            deg_node2 = self.node_degree(edge[1])
            
            if deg_node1 == 0:
                deg_node1 = EPSILON
                
            if deg_node2 == 0:
                deg_node2 = EPSILON                      
            
            if weight == MAXLOGDEG:
                self.G.edge[edge[0]][edge[1]]['weight'] = \
                    max(math.log(deg_node1), math.log(deg_node2))
            elif weight == SQRTLOGDEG:
                self.G.edge[edge[0]][edge[1]]['weight'] = \
                    max(math.sqrt(deg_node1, deg_node2))
            
            #print edge, self.G.edge[edge[0]][edge[1]]['weight']
            
    def weighted_concept_path(self, node1, node2):
        
        '''
        Shortest path between two nodes
        
        :param node1: id of node 1
        :param node2: id of node 2
        :return: shortest path between node1 and node2
        '''
        spath = 0
        
        if self.all_dist:
            try:
                spath = self.all_dist[node1][node2]                
            except:
                raise exception.GraphException((node1, node2), \
                               'No path for this node pair')
        else:
            try:
                spath = nx.dijkstra_path_length(self.G, node1, node2)
            except:
                raise exception.GraphException((node1, node2), \
                               'No path for this node pair')
        
        return spath
     
    def all_distances(self):
        
        '''
        All distances between nodes in the graph
        '''
        
        try:
            self.all_dist = nx.all_pairs_dijkstra_path_length(self.G)
        except:
            raise exception.GraphException(self.all_dist, \
                               'Error computing all pairs path length')
        
    def find_max_distance(self):
        
        '''
        Find the maximum distance between nodes in the graph
        '''       
        
        if not self.all_dist:
            self.all_distances()
            
        try:
            maxd = -1
            for d1 in self.all_dist.itervalues():
                for d2 in d1.itervalues():
                    if d2 > maxd:
                        maxd = d2
            self.max_dist = maxd            
        except:
            raise exception.GraphException(self.max_dist, \
                               'Error computing maximum distance')
    
          
    def connected_concepts(self, node, level, weight_type = None):
        
        '''
        Connected concepts for a node in the graph
        
        :param node: the node for which connected concepts are retrieved
        :param level: distance between node and connected concepts
        :param weight_type: type of weighting for connected concepts
        :return: dictionary of connected concepts and their weight
        '''
                
        if level > MAX_LEVEL or level < 0:
            raise exception.GraphException(level, \
                'Level should be greater than 0 and less than %s' %(MAX_LEVEL))
        
        if weight_type == None:
            weight_type = EQUAL_WEIGHT
        
        if weight_type != EQUAL_WEIGHT and weight_type != LEVEL_WEIGHT:
            raise exception.GraphException(weight_type, \
                               'Unsupported weight type')
        
        res_nodes = {}
        weight = 0
        
        if weight_type == EQUAL_WEIGHT:
            weight = 1.0
        
        # find connected concepts and weight them
        while level > 0:
            nodes = nx.single_source_shortest_path(self.G, node, level)
            snodes = set(nodes.keys())
                        
            if weight_type == LEVEL_WEIGHT:
                weight = 1/float(level)               
                        
            for c in snodes:
                res_nodes[c] = weight
            
            level -= 1
        
        return res_nodes

class WnGraph(Graph):
    
    '''
    Graph representation of the WordNet lexical database
    '''
    
    def __init__(self, wordnet):
        
        '''
        Class constructor
        '''
        
        Graph.__init__(self)
        self.wordnet = wordnet
    
    def add_edges(self, synset, csynsets):
        
        '''
        Add edges between a synset and connected synsets
        
        :param synset: synset representing a concept
        :param csynsets: synsets related to synset
        '''
        
        for cs in csynsets:
            self.G.add_node(cs.name)
            self.G.add_edge(synset.name, cs.name)
        
    def build_graph(self):
        
        '''
        Build a networkx graph from WordNet
        '''
        
        for synset in list(self.wordnet.all_synsets()):
        #for synset in list(self.wordnet.all_synsets('n'))[:10]:
            self.G.add_node(synset.name)
            self.add_edges(synset, synset.hypernyms())
            self.add_edges(synset, synset.hyponyms())
            self.add_edges(synset, synset.instance_hypernyms())
            self.add_edges(synset, synset.instance_hyponyms())
            self.add_edges(synset, synset.member_holonyms())
            self.add_edges(synset, synset.substance_holonyms())
            self.add_edges(synset, synset.part_holonyms())
            self.add_edges(synset, synset.member_meronyms())
            self.add_edges(synset, synset.substance_meronyms())
            self.add_edges(synset, synset.part_meronyms())
            self.add_edges(synset, synset.attributes())
            self.add_edges(synset, synset.entailments())
            self.add_edges(synset, synset.causes())
            self.add_edges(synset, synset.also_sees())
            self.add_edges(synset, synset.verb_groups())
            self.add_edges(synset, synset.similar_tos())
            
        print nx.info(self.G)
    
    def wn_pos(self, pos):
        
        '''
        Convert to WordNet part-of-speech
        '''
        
        if len(pos) < 1:
            return None
        
        if pos[0] == 'N':
            return self.wordnet.NOUN
        elif pos[0] == 'V':
            return self.wordnet.VERB
        elif pos[0] == 'J':
            return self.wordnet.ADJ
        elif pos[0] == 'R':
            return self.wordnet.ADV
        else:
            return None
        
     
    def concepts(self, token):
        
        '''
        Find concepts for a given token
        
        :param token: token for which concepts are to be found
        :return list of concepts for the token
        '''
        
        concepts = []
        
        word = token.word_str.lower()
        word = word.replace(' ', '_')
        pos = self.wn_pos(token.pos)
        lemma = token.lemma
        lemma = lemma.replace(' ', '_')
        
        print word, lemma, pos
        
        if pos != None:
        
            try:
                concepts = self.wordnet.synsets(word, pos)
            except:
                try:
                    concepts = self.wordnet.synsets(lemma, pos)
                except:
                    pass
            
        concepts = [s.name for s in concepts]
        
        return concepts
        
        
            
        
         
            
            
           
    
    
    