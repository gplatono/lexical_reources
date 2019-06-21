import io
import os
import anytree
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk import FreqDist as FD

# ----------------------------------------------------------------------------------------------
# semnatics
only_litterals = True   # this removes the synsets that aren't exactly the word
pruning_threashold = 15  # any word with frequency less than this won't be included in the tree

# debug flags
print_paths = False      # determines if the path for each word is printed
print_numbers = True    # determines if various lengths are printed
print_tree_one = False    # determines if we print out the tree
print_tree_two = True    # determines if we print out the tree after trimming
# ---------------------------------------------------------------------------------------------

# just a quick helpful function
def get_string_from_synset(synset):
    return str(synset)[8:-2]

# read the words ----------------------------------------------------------------------------------
os.chdir("C:\\Users\\aaron\\Google Drive\\AJ\\Python")

words = []

with open(".\\Lexical Resources\\Noun Heirarchies\\ogden_nouns.txt", "r") as f:
    line = f.readline().strip()
    words.append(line)
    while line:
        line = f.readline().rstrip()
        words.append(line)
# for the ogden picturable nouns
'''
with open(".\\Lexical Resources\\Noun Heirarchies\\nouns.txt", "r") as f:
    line = f.readline().strip()
    words.append(line)
    while line:
        line = f.readline().rstrip()
        words.append(line)
'''# for the nouns list we've generated

if print_numbers:
    print("WORDS: " + str(len(words)))
# -------------------------------------------------------------------------------------------------
# This is for counting the number of words that don't have unique hypernyms -----------------------
'''
counterZ = 0
counterT = 0
counterM = 0
counterTotal = 0
for word in words:
    for syn in wn.synsets(word, pos=wn.NOUN):
        counterTotal += 1
        hyps = syn.hypernyms()
        if not len(hyps) == 1:
            if len(hyps) == 0:
                counterZ += 1
            elif len(hyps) == 2:
                counterT += 1
                print(str(hyps) + ", " + syn.definition() + ", " + str(syn))
            else:
                counterM += 1
                print(hyps)
print(counterZ)
print(counterT)
print(counterM)
print(counterTotal)
'''
# -------------------------------------------------------------------------------------------------
# get paths ---------------------------------------------------------------------------------------
paths = []

for word in words:
    # get all the noun senses of the word
    word_synsets = wn.synsets(word, pos=wn.NOUN)

    # for each valid sense, make a path
    for syn in word_synsets:
        hypernyms = syn.hypernyms()
        syn_string = get_string_from_synset(syn)

        if only_litterals and not syn_string.split(".")[0] == word:
            continue

        path = [syn_string]

        # climb up the tree
        while not hypernyms == []:
            next_syn = hypernyms[-1]
            next_syn_string = get_string_from_synset(next_syn)

            # ensures there's no cycles formed
            if next_syn_string in path:
                break

            path.append(next_syn_string)

            hypernyms = next_syn.hypernyms()

        if print_paths:
            print(word)
            print("\t" + str(path))

        # add the valid path to the paths
        paths.append(path)

if print_numbers:
    print("PATHS: " + str(len(paths)))

# -------------------------------------------------------------------------------------------------
# merge the paths into a tree ---------------------------------------------------------------------
nodes = dict()

root_node = Node("entity.n.01")

nodes["entity.n.01"] = root_node

for path in paths:
    prev_node = root_node
    for word in reversed(path):
        if not word in nodes.keys():
            new_node = Node(word, parent=prev_node)
            nodes[word] = new_node
            prev_node = new_node
        else:
            prev_node = nodes.get(word)

if print_numbers:
    print("NODES: " + str(len(nodes)))

if print_tree_one:
    for pre, fill, node in RenderTree(root_node, style=AsciiStyle()):
        print(("%s%s" % (pre, node.name)).encode("utf-8"))
# -------------------------------------------------------------------------------------------------
# calculating a good pruning threashold -----------------------------------------------------------
'''
tree_words = [node.name.split(".")[0] for node in PreOrderIter(root_node)]
tree_words = [s.replace("_", " ") for s in tree_words]
tree_words = list(dict.fromkeys((tree_words)))
fdist = FD(w.lower() for w in brown.words())
counter = [0 for n in range(0, 10000)]
for word in tree_words:
    counter[fdist[word]] += 1
    #if fdist[word] == x:
        #print(word)

for i in range(0, 10000):
    if not counter[i] == 0:
        print(i, counter[i])
'''
# -------------------------------------------------------------------------------------------------
# actually pruning --------------------------------------------------------------------------------
freq = FD(w.lower() for w in brown.words())
preorder_tree_nodes = [node for node in PreOrderIter(root_node)]

# quick function
def name(node):
    return node.name.split(".")[0].replace("_", " ")

# we need to get rid of the nodes that are leaves but also have entity as a parent
# these named entities
named_entities_removed = 0
for children in root_node.children:
    if children.children == ():
        children.parent = None
        nodes.pop(children.name)
        named_entities_removed += 1

# now we need to eliminate the nodes that don't occur frequently enough
inner_nodes_removed = 0
for node in preorder_tree_nodes:
    if freq[name(node)] <= pruning_threashold:
    # remove it from the tree
        parent = node.parent

        # don't remove the root
        if parent == None:
            continue

        # don't remove a leaf
        if node.children == ():
            continue

        inner_nodes_removed += 1

        # make the children's parent into this node's parent
        for child in node.children:
            child.parent = parent

        node.parent = None
        nodes.pop(node.name)

if print_numbers:
    print("NAMED-ENTITES REMOVED: " + str(named_entities_removed))
    print("INNER-NODES REMOVED: " + str(inner_nodes_removed))
    print("POST-NODES: " + str(len(nodes)))

if print_tree_two:
    for pre, fill, node in RenderTree(root_node, style=AsciiStyle()):
        print(("%s%s" % (pre, node.name)).encode("utf-8"))
# -------------------------------------------------------------------------------------------------
