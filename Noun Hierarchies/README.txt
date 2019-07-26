This folder contains resources for exploring and building noun hierarchies:
Sources:
  contains noun lists for generating hierarchies or more selective lists

Hierarchies:
  contains the hierarchies generated from the noun lists

generate_hiers.py:
  a script which allows for hierarchy generation from the list of source nouns.
  usage: To set any of the following flags, put "-flag true" or "-flag false", and for thresholds just put a number
-f: filter, i.e. should any nodes be removed to condense the tree
-ftt: filter trimming threshold, 0 < x < 100, if f is enabled it will remove words that occur less than x times in the Brown corpus.  It depends, but generally 0 is 0%, 1 is ~20%, 15 is ~35%, etc.

-fim: filter inexact matches, i.e. ignore the words which aren't the name of the wordnet synset

-fis: filter infrequent senses, i.e. remove the senses that aren't of at least a certain frequency of total uses in the Semcor corpus
-stt: sense trimming threshold, 0 < x < 1, if fis is enabled then senses that occur less than (x*100)% of the time are removed

-fne: filter named entities, i.e. remove the synsets which correspond to named entities

-fsp: filter single parents, i.e. remove the synsets which have exactly one child in the hierarchy

-i: use this to set the input file

-o: use this to set the output file
-epi: use epilog hierarchy output

-d: enables debugging mode, it prints a lot of things in the console

example: py generate_hiers.py -i ogden_nouns.txt -o on_hierarchy.txt -f true -ftt 10 -fis false -fim true -epi true

selecting_synsets_script.py:
  a script for manual filtering or selection of senses of the words of a particular list, allows for much more selective hierarchy generation at the cost of being quite labor intensive, though the script tries to make is easier

toy_script.py:
  this was for some initial exploration, still some useful bits but generally avoid using
