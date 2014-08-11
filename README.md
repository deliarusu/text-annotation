text-annotation
===============

Introduction
------------

This project implements algorithms for determining the relatedness between
two concepts and for annotating text based on concept relatedness.

Given a knowledge base or ontology as input, the relatedness between two 
concepts is computed using:

* a definition-based measure: based on the concept and connected concepts 
definitions (human-readable text describing their meaning)
* a structure-based measure: using the ontology or knowledge base structure
(how concepts are related in the knowledge base)
* a hybrid measure combining concept definitions and knowledge base structure

Words in text are annotated with concepts from the ontology or knowledge base 
as follows. First, candidate concepts are identified for words in a given 
context window. Second, the relatedness between candidate concepts in the 
context window is computed. Third, the candidate concept with the best 
relatedness score is selected to annotate the word.

The code is organized in four main packages:

1. The knowledgebase package contains modules for representing the knowledge
base as a NetworkX graph of concepts and relations between concepts, as well
as a module for representing concept definitions as a Bag of Words (BOW).
2. The text package is useful for text pre-processing.
3. The relatedness package modules contain implementations of the 
definition-based and structure-based algorithms.
4. The annotation package contains modules with the implementation of the text
annotation algorithm.

Configuration     
-------------

See util.writeconfig for the parameters that should be set for the relatedness
and text annotation modules.

Examples
--------

The relatedness and annotation packages contain example code for determining 
the relatedness between two concepts and for annotating text respectively. 
See relatedness.main_relatedness and annotation.main_annotation for more 
details.