This folder contains resources for exploring and building noun hierarchies:
Sources:
  contains noun lists for generating hierarchies or more selective lists
Hierarchies:
  contains the hierarchies generated from the noun lists
generate_hiers.py:
  a script which allows for hierarchy generation from the list of source nouns.  Use the configuration variables at the beginning of the file.
selecting_synsets_script.py:
  a script for manual filtering or selection of senses of the words of a particular list, allows for much more selective hierarchy generation at the cost of being quite labor intensive, though the script tries to make is easier
toy_script.py:
  this was for some initial exploration, still some useful bits but generally avoid using

The generated hierarchies, when using default output file name None, are outputted to the file "[file_in]_***NN_hierarchy.txt".  The first star corresponds to whether or not inexact matches were filtered out, the second star corresponds to whether any filtering of the inner nodes was done, the third star corresponds to whether suspected named entities were removed.  NN is the trimming threshold used to filter the inner nodes of the hierarchy by frequency.