# lexical_resources
This directory is for various lexical resources, such as lists of "X most frequent"
 or "X most fundamental words" in the English language, words lists by syntactic
categories, the data on the word inflection (i.e., tenses and aspects of verbs), etc.

Specifically:

5000_words_coca.csv, 5000_words_coca.xlsx - the list 0f 5000 most frequent words
in American English, gathered from the Corpus of the Contemporary American English
(COCA). See https://www.english-corpora.org/coca/. The datasets contain the words
themselves (in alphabetical order) as well as the frequency data and the part of
speech tag for each word.

dolch_wordlist - the list of 220 English words composed by Edward Dolch in the 
1930s and 1940s. The list is based on the children stories designed for the readers 
up to the elementary school. The file contains just the words in the alphabetical 
order.

ogden_wordlist - the list of 850 Basic English words composed by Charles K. Ogden 
in the 1930. The list is designed as a basic vocabulary for the people learning 
English as a second language. The file contains just the words in the alphabetical 
order.

NGSL+1.01+by+band.csv, NGSL+1.01+by+band.xlsx - The New General Service List is an 
expanded version (composed in 2013) of the classic General Service List (composed in 1953)
 which was intended, pretty much like Ogden's list, for the ESL learners. The purpose was
to collect the smallest subset of English vocabulary with the maximum coverage of
texts. The NGSL contains about 2800 unique word lemmas, along with the usage 
frequency and various words forms. That is, the entry for "be", also contains forms
such as "was", "being", "am", etc.

BNC_top_2164_nouns - the list of 2164 most frequent nouns from the British National
Corpus (BNC), covering about 80% of 19,278,169 total noun occurrences in the corpus. 
The data are formatted into two columns, where the first column lists the (probably 
absolute) frequencies of the words and the second the words themselves. The data are
sorted in a descending order of frequency. The list was compiled by Jonathan Gordon.

Note from J. Gordon:
"I included the plural nouns, making them singular when I could. So, 'scissors' 
remains plural, but 'pants' was turned to 'pant' (which is how it is in WordNet:
 they just note 'usually in the plural'). There are probably some erroneous singulars
 in there, but I think this is good enough."

BNC_nouns_freqs - contains the list of all (about 169000) the nouns from the BNC
 along with their absolute frequency in the corpus. The data are formatted in a 
similar way to Jonathan's list and sorted in a descending order of frequency.
