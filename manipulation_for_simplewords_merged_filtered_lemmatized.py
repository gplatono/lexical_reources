import io
import os
from nltk.stem import WordNetLemmatizer

# thanks https://www.machinelearningplus.com/nlp/lemmatization-examples-python/
from nltk.corpus import wordnet
import nltk

os.chdir("C:\\Users\\aaron\\Google Drive\\AJ\\Python")

words = []
with open(".\\Lexical Resources\\wordslist.txt", "r") as f:
    line = f.readline().rstrip()
    words.append(line)
    while line:
        line = f.readline().rstrip()
        words.append(line)
words = words[:-1]

words_all_lower = list(map(lambda x: x.lower(), words))
words_all_lower = list(dict.fromkeys(words_all_lower))
# do we want to care about capitalization?  If not we have dupicates...
# This operation removes 23 from the original list
# 4789 -> 4776

words = words_all_lower

# now I want to count the words that contain digits...  probably don't want these
digitals = [x for x in words if any(char.isdigit() for char in x)]

# the origial list contains 2 numbers... 1970 and 1960, remove them
words = [x for x in words if x not in digitals]
# 4776 -> 4774

# there are some words that are "too short" for us to consider
# the list contains entries like "r", "t", "e", and though some
# have dictionary definitions we don't care about them... let's inspect them
shorts = [x for x in words if len(x) < 3]
# ['ah', 'am', 'ad', 't', 'er', 'my', 'as', 'pc', 'be', 'oh', 'so', 'in', 'at',
# 'up', 'to', 'a', 'of', 'me', 're', 'tv', 'ms', 'pm', 'ok', 'on', 'r', 'we',
# 'b', 'p', 'is', 'uh', 'vs', 'us', 'e', 'hi', 'ha', 'mm', 'an', 'no', 'it',
# 'he', 'do', 'or', 'if', 'i', 'mr', 'ie', 'by', 'go']

# by inspection I generated this:
invalid_shorts = ['t', 'er', 're', 'r', 'b', 'p', 'e', 'mm', 'ms', 'vs']

# remove the invalid shorts
words = [x for x in words if x not in invalid_shorts]
# 4774 -> 4766

# we may not want some of the words that have non-alphabetic characters
non_alpha = [x for x in words if not x.isalpha()]
# 24 of them:
# ['well-known', "n't", 'co-operation', 'old-fashioned', "o'clock", 'short-term',
# 'one-third', 'hon.', 'full-time', 'self-esteem', 'so-called', 'and/or',
# 'e-mail', 'high-tech', 'middle-class', "let'", 'mm-hmm', 't-shirt', "don't",
# 'well-being', '****************', 'two-thirds', 'long-term']

invalid_non_alpha = ['****************', "n't", 'and/or', "let'", 'mm-hmm', "don't",
                        "hon."]

# remove the invalid nonalphabetics
words = [x for x in words if x not in invalid_non_alpha]
# 4766 -> 4761

# now we want to lemmatize everything
def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag)

lemmatizer = WordNetLemmatizer()

lemmatized = []

for word in words:
    pos = get_wordnet_pos(word)
    if pos == None:
        lemmatized.append(word)
        continue
    nw = lemmatizer.lemmatize(word, pos)

    if not nw == 'be':
        lemmatized.append(nw)
    else:
        lemmatized.append(word)

# remove duplicates
lemmatized = list(dict.fromkeys(lemmatized))

# 4761 -> 4604
words = lemmatized

with open(".\\Lexical Resources\\newwordslist.txt", "w") as f:
    for word in words:
        f.write(word + "\n")
