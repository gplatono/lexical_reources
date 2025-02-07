import io
import os
import sys
from semcor_sense_frequency import SemcorSenseFrequency
from brown_frequency import BrownFrequency
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk import FreqDist as FD
import ast
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter
'''
This script is for creating a heirarcy from any list of nouns.
The list must take one of two forms:
1 - a word on each line
...
arm
army
baby
bag
ball
band
...
2 - a word on each line with selected synsets
...
arm:[1, 4]
army:[1]
baby:[1, 6]
bag:[1]
ball:[1, 3, 6, 9]
band:[2, 5]
...
The first option is very simple and not difficult to generate on the fly,
and the second option can be generated from the first one using the
"selecting_synsets_script.py" script.  This involves very time intensive manual
selection of synsets but dramatically decreases the complexity of the tree
'''

# CONFIG ------------------------------------------------------------------------------------------
# I/O -------------------------------------------
# the input file
file_in = "ogden_nouns_manually_selected.txt"

# the output file
file_out = None
use_output = True
epilog_output = False

# Filtering Flags -------------------------------
# should we use only exact matches?
filter_inexact_matches = True

# should we filter by synset frequency? (Semcor)
filter_infrequent_senses = False

# should we filter the inner nodes?
filter_inner_nodes = True

# should we filter suspected named entities?
filter_named_entities = True

# should we filter parents with only one child?
filter_single_parents = True

# the frequency cutoff to filter the inner nodes by
trimming_threashold = 5
# 0 is 0%, 1 is ~20%, 15 is ~35%, etc.

# the frequency cutoff to filter the infrequent senses by
sense_trimming_threashold = 0.2

# how do we want to handle the multiple hypernyms cases?
use_more_frequent_parent = True
use_arbitrary_parent = False

# Printing / Debug Flags ------------------------
print_synsets = False   # determines if the synsets & definitions are printed
print_paths = False      # determines if the path for each word is printed
print_numbers = False    # determines if various numbers are printed
print_tree_one = False    # determines if we print out the tree
print_tree_two = False    # determines if we print out the tree after trimming

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

# quick functions -------------------------------
def name(node):
    return node.name.split(".")[0].replace("_", " ")
def synstr(synset):
    return (str(synset))[8:-2]
def get_flags():
    out = ""
    if filter_inexact_matches:
        out += "t"
    else:
        out += "f"
    if filter_inner_nodes:
        out += "t"
    else:
        out += "f"
    if filter_named_entities:
        out += "t"
    else:
        out += "f"
    if filter_single_parents:
        out += "t"
    else:
        out += "f"
    out += str(trimming_threashold)
    return out

# Check for args ----------------------------------------------------------------------------------
if len(sys.argv) > 1:
    if "-fim" in sys.argv:
        if sys.argv[(1+sys.argv.index("-fim"))].lower()[0] == "t":
            filter_inexact_matches = True
        else:
            filter_inexact_matches = False
    if "-fis" in sys.argv:
        if sys.argv[(1+sys.argv.index("-fis"))].lower()[0] == "t":
            filter_infrequent_senses = True
        else:
            filter_infrequent_senses = False
    if "-fne" in sys.argv:
        if sys.argv[(1+sys.argv.index("-fne"))].lower()[0] == "t":
            filter_named_entities = True
        else:
            filter_named_entities = False
    if "-fsp" in sys.argv:
        if sys.argv[(1+sys.argv.index("-fsp"))].lower()[0] == "t":
            filter_single_parents = True
        else:
            filter_single_parents = False
    if "-f" in sys.argv:
        if sys.argv[(1+sys.argv.index("-f"))].lower()[0] == "t":
            filter_inner_nodes = True
        else:
            filter_inner_nodes = False

    if "-ftt" in sys.argv:
        trimming_threashold = int(sys.argv[(1+sys.argv.index("-ftt"))].lower())

    if "-stt" in sys.argv:
        sense_trimming_threashold = float(sys.argv[(1+sys.argv.index("-stt"))].lower())

    if "-epi" in sys.argv:
        if sys.argv[(1+sys.argv.index("-epi"))].lower()[0] == "t":
            epilog_output = True
        else:
            epilog_output = False

    if "-i" in sys.argv:
        file_in = sys.argv[(1+sys.argv.index("-i"))].lower()

    if "-o" in sys.argv:
        file_out = sys.argv[(1+sys.argv.index("-o"))].lower()
    else:
        file_out = None

    if "-d" in sys.argv:
        print_synsets = True
        print_paths = True
        print_numbers = True
        print_tree_one = True
        print_tree_two = True


# Reading -----------------------------------------------------------------------------------------
# storing the words
words = []

# did we clarify the synsets, i.e. use input option 2?
clarify_synsets = False
clarified_synsets = dict()

# set the working directory
os.chdir(os.path.abspath(os.path.dirname(__file__)))

# do the actual reading
with open(".\\Sources\\" + file_in, "r") as f:
    # read the first line
    line = f.readline().strip()

    # determine if this is the 1st or 2nd type of list
    if ':' in line: # type 2
        clarify_synsets = True
        word = line.split(':')[0]
        words.append(word)
        clarified_synsets[word] = ast.literal_eval(line.split(':')[1])
        while line:
            line = f.readline().rstrip()
            if line == "":
                break
            word = line.split(':')[0]
            words.append(word)
            clarified_synsets[word] = ast.literal_eval(line.split(':')[1])

    else: # type 1
        words.append(line)
        while line:
            line = f.readline().rstrip()
            if line == "":
                break
            words.append(line)

if print_numbers:
    print("WORDS: " + str(len(words)))

# reading complete --------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

# important long-time things
brFreq = BrownFrequency()

# Get Synsets -------------------------------------------------------------------------------------
# a place to store them
synsets = []

# it really depends here which input type list
if clarify_synsets: # type 2
    for word in words:
        all_syns = wn.synsets(word, pos=wn.NOUN)
        for i in clarified_synsets[word]:

            # otherwise append
            synsets.append(all_syns[i-1])

else: # type 1

    if filter_inexact_matches:
        inexactRemoved = 0

    if filter_infrequent_senses:
        # get the sense frequency list
        infreqSenseRemoved = 0
        seFreq = SemcorSenseFrequency()

    for word in words:
        all_syns = wn.synsets(word, pos=wn.NOUN)
        for syn in all_syns:

            # if we're removing inexact matches, check if it maches and don't add a path if not
            if filter_inexact_matches and not synstr(syn).split(".")[0] == word:
                inexactRemoved += 1
                continue

            if filter_infrequent_senses and not seFreq.is_frequent(synstr(syn), threashold = sense_trimming_threashold):
                infreqSenseRemoved += 1
                continue

            synsets.append(syn)

    if print_numbers:
        if filter_inexact_matches:
            print("INEXACT REMOVED: " + str(inexactRemoved))
        if filter_infrequent_senses:
            print("INFREQ SENSES REMOVED: " + str(infreqSenseRemoved))


if print_numbers:
    print("SYNSETS: " + str(len(synsets)))

if print_synsets:
    for syn in synsets:
        print(synstr(syn) + ":")
        print("\t" + syn.definition())

# synsets aquired ---------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

# Generate Paths ----------------------------------------------------------------------------------
# a place to store them
paths = []

# for each synset make a path
for syn in synsets:
    if use_arbitrary_parent:
        hypernyms = syn.hypernyms()
        synstring = synstr(syn)
        path = [synstring]

        # climb up the tree
        while not hypernyms == []:
            next_syn = hypernyms[-1]
            string_next = synstr(next_syn)

            # ensures there's no cycles formed
            if string_next in path:
                break

            path.append(string_next)

            hypernyms = next_syn.hypernyms()

        if print_paths:
            print(synstring)
            print("\t" + str(path))

        # add the valid path to the paths
        paths.append(path)
    elif use_more_frequent_parent:

        hypernyms = syn.hypernyms()
        synstring = synstr(syn)
        path = [synstring]

        # climb up the tree
        while not hypernyms == []:
            if len(hypernyms) > 1:
                dic = {word:brFreq.get_freq(synstr(word)) for word in hypernyms}
                if all(x == 0 for x in dic.values()):
                    mini = hypernyms[0]
                    for i in range(1, len(hypernyms)):
                        if len(synstr(hypernyms[i])) < len(synstr(mini)):
                            mini = hypernyms[i]
                    next_syn = mini
                else:
                    maxi = hypernyms[0]
                    for i in range(1, len(hypernyms)):
                        if dic.get(hypernyms[i]) > dic.get(maxi):
                            maxi = hypernyms[i]
                    next_syn = maxi
            else:
                next_syn = hypernyms[0]
            string_next = synstr(next_syn)

            # ensures there's no cycles formed
            if string_next in path:
                break

            path.append(string_next)

            hypernyms = next_syn.hypernyms()

        if print_paths:
            print(synstring)
            print("\t" + str(path))

        # add the valid path to the paths
        paths.append(path)


if print_numbers:
    print("PATHS: " + str(len(paths)))

# paths generated ---------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

# Seeding a Tree ----------------------------------------------------------------------------------
# we want to merge the paths together to make the heirarchy
# a place to store all of the nodes
nodes = dict()

# this is surely the root node
root_node = Node("entity.n.01")
nodes["entity.n.01"] = root_node

# for each path
for path in paths:

    # store the node that will be used as the parent, initialized to the root
    prev_node = root_node

    # traverse the path in reverse, starting with the top of the path
    for word in reversed(path):

        # if it's not in the tree yet, make a new node
        if not word in nodes.keys():
            new_node = Node(word, parent=prev_node)
            nodes[word] = new_node
            prev_node = new_node

        # if it's already in the tree build the rest below this
        else:
            prev_node = nodes.get(word)

if print_numbers:
    print("NODES: " + str(len(nodes)))

if print_tree_one:
    for pre, fill, node in RenderTree(root_node, style=AsciiStyle()):
        print(("%s%s" % (pre, node.name)).encode("utf-8"))

prenodes = len(nodes)
# tree constructed --------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

# Trimming ----------------------------------------------------------------------------------------
# do we want to filter the suspected named entities?
# these are the ones that are direct children of the root but are leaves
if filter_named_entities:
    # just a count of how many we've removed, bookkeeping
    named_entities_removed = 0

    # for each child of the root
    for children in root_node.children:

        # if it is a leaf
        if children.children == ():

            # remove it
            children.parent = None
            nodes.pop(children.name)

            named_entities_removed += 1

    if print_numbers:
        print("N.E.s REMOVED: " + str(named_entities_removed))

# do we want to filter the less frequent inner nodes?
if filter_inner_nodes:

    # get the nodes using a preorder traversal
    preorder_tree_nodes = [node for node in PreOrderIter(root_node)]

    # just a count of how many we've removed, bookkeeping
    inner_nodes_removed = 0

    # now we need to eliminate the nodes that don't occur frequently enough
    for node in preorder_tree_nodes:

        # don't remove a leaf
        if node.children == ():
            continue

        if not brFreq.is_frequent(name(node), trimming_threashold):
        # remove it from the tree
            parent = node.parent

            # don't remove the root
            if parent == None:
                continue

            # this is probably better

            inner_nodes_removed += 1

            # make the children's parent into this node's parent
            for child in node.children:
                child.parent = parent

            node.parent = None
            nodes.pop(node.name)

    if print_numbers:
        print("INNERS REMOVED: " + str(inner_nodes_removed))

# do we want to filter parents of only one child?
if filter_single_parents:

    single_parents_removed = 0

    # get the nodes using a preorder traversal
    preorder_tree_nodes = [node for node in PreOrderIter(root_node)]

    for node in preorder_tree_nodes:
        # if only has one child
        if len(node.children) == 1:
        # remove it from the tree
            parent = node.parent

            single_parents_removed += 1

            # make the children's parent into this node's parent
            for child in node.children:
                child.parent = parent

            node.parent = None
            nodes.pop(node.name)

    if print_numbers:
        print("S.P.s REMOVED: " + str(single_parents_removed))



if print_numbers:
    print("NODES POST-FILTERING: " + str(len(nodes)))

if print_tree_two:
    for pre, fill, node in RenderTree(root_node, style=AsciiStyle()):
        print(("%s%s" % (pre, node.name)))



# done filtering ----------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
'''
# Analysis ----------------------------------------------------------------------------------------
preorder_tree_nodes = [node for node in PreOrderIter(root_node)]
dups = dict()
counter = 0

for node in preorder_tree_nodes:
    if len(node.children) != len(set([name(n) for n in node.children])):

        for i in range(0, len(node.children)-1):
            for j in range(i+1, len(node.children)):
                if name(node.children[i]) == name(node.children[j]):
                    dups[name(node)] = [node.children[i].name, node.children[j].name]
        counter += len(dups)
for key in dups.keys():
    print(key)
    set = dups[key]
    print(set[0], wn.synset(set[0]).definition())
    print(set[1], wn.synset(set[1]).definition())
print(counter)


# done --------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
'''
# Output ------------------------------------------------------------------------------------------
if not use_output:
    exit()

if file_out == None:
    splits = file_in.split(".")
    file_out = splits[0] + "_hierarchy." + splits[1]

# don't want to override anything
if os.path.exists(".\\Hierarchies\\" + file_out):
	splits = file_out.split(".")
	counter = 2
	while os.path.exists(".\\Hierarchies\\" + splits[0] + "_" + str(counter) + "." + splits[1]):
		counter += 1
	file_out = splits[0] + "_" + str(counter) + "." + splits[1]

if epilog_output:
    def epilog_hier(node):
        lis = [root_node, node]
        for chil in node.children:
            lis.append(chil)

        out = "'" + lis[0].name + ((node.depth*4)*' ')
        for i in range(1, len(lis)):
            out += " '" + lis[i].name

        return "(add-hier " + out + ")"

    # for each node we want to output the node and the children
    preorder_tree_nodes = [node for node in PreOrderIter(root_node)]

    with open(".\\Hierarchies\\" + file_out, "w") as f:
        for node in preorder_tree_nodes:
            if node.children != ():
                f.write(epilog_hier(node) + "\n")


else:
    with open(".\\Hierarchies\\" + file_out, "w") as f:
        f.write("Filter Inexact Synsets: " + str(filter_inexact_matches) + "\n")
        f.write("Filter Infrequent Senses: " + str(filter_infrequent_senses) + "\n")
        f.write("Filter Named Entities: " + str(filter_named_entities) + "\n")
        f.write("Filter Inner Nodes: " + str(filter_inner_nodes) + "\n")
        f.write("Filter Single Parents: " + str(filter_single_parents) + "\n")
        f.write("WORDS:"+str(len(words))+"\n")
        f.write("PATHS:"+str(len(paths))+"\n")
        f.write("PRE-NODES:"+str(prenodes)+"\n")
        f.write("POST-NODES:"+str(len(nodes))+"\n")
        for pre, fill, node in RenderTree(root_node, style=AsciiStyle()):
            f.write(("%s%s\n" % (pre, node.name)))


# done --------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------