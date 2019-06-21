from nltk.corpus import wordnet as wn
import io
'''
A script for viewing and selecting which senses of words to use in
tree seeding

Usage:
...
(1/200) angle -
	angle.n.01: the space between two lines or planes that intersect; the inclination of one line to another; measured in degrees or radians
	slant.n.01: a biased way of looking at or presenting something
	angle.n.03: a member of a Germanic people who conquered England and merged with the Saxons and Jutes to become Anglo-Saxons
>> 1
...
'''
# CONFIG ------------------------------------------------------------------------------------------
# the input file name
file_in = "ogden_nouns.txt"

# the output file name
file_out = None

# -------------------------------------------------------------------------------------------------

# just a quick helpful function
def get_string_from_synset(synset):
    return str(synset)[8:-2]


# READING -----------------------------------------------------------------------------------------
# initialize words
words = []

# read in the words
with open(".\\Sources\\" + file_in, "r") as f:
    line = f.readline().strip()
    words.append(line)
    while line:
        line = f.readline().rstrip()
        words.append(line)
words = words[:-1]

# -------------------------------------------------------------------------------------------------
# FILTERING ---------------------------------------------------------------------------------------

kept = dict()
index = 0
while index < len(words):
    word = words[index]

    print("(" + str(index + 1) + "/" + str(len(words)) + ") " + word + " - ")

    synsets = wn.synsets(word, pos=wn.NOUN)

    for syn in synsets:
        print("\t" + get_string_from_synset(syn) + ": " + syn.definition())

    print(">>", end=' ')

    try:
        senses = [int(x) for x in input().split()]
    except:
        print("Sorry didn't get that...  Try again")
        continue
    index += 1

    kept[word] = senses


# -------------------------------------------------------------------------------------------------
# OUTPUT ------------------------------------------------------------------------------------------
# the default case
if file_out == None:
    splits = file_in.split(".")
    file_out = splits[0] + "_manually_selected." + splits[1]

# don't want to override anything
if os.path.exists(".\\Sources\\" + file_out):
	splits = file_out.split(".")
	counter = 2
	while os.path.exists(".\\Sources\\" + splits[0] + "_" + str(counter) + "." + splits[1]):
		counter += 1
	file_out = splits[0] + "_" + str(counter) + "." + splits[1]

# actually write
with open(".\\Sources\\" + file_out, "w") as f:
    for word in words:
        f.write(word + ":" + str(kept[word]) + "\n")

# -------------------------------------------------------------------------------------------------