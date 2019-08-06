#Uncomment the lines below to download and install wordnet corpus for nltk
#import nltk
#nltk.download('wordnet')
import nltk
#nltk.download('averaged_perceptron_tagger')
#nltk.download('brown')

from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.tag import pos_tag

brown_news_tagged = brown.tagged_words(categories='news')
data = nltk.ConditionalFreqDist((word.lower(), tag) for (word, tag) in brown_news_tagged)


words = open("merged_wordlist_without_BNC_nouns_freqs").readlines()

for word in words:
	tags = data[word].keys()
	print (word, ' '.join(tags))

	#print (wn.synsets('word'))
	#print (word, pos_tag(word.strip()))