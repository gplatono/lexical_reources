
import ast

class SemcorSenseFrequency:
    ''' uses the Semcor Corpus to determine if a synset is frequent '''

    def __init__(self):
        with open(".\\Resources\\semcor_noun_sense_frequency.txt", 'r') as f:
            s = f.read()
            list = ast.literal_eval(s)
            self.dictionary = {key:value for (key, value) in list}

    def is_frequent(self, synset, threashold = 0.2):

        word = synset.split(".")[0]
        syn_freq_list = self.dictionary.get(word)

        if syn_freq_list == None:
            return True # don't comment if we're not sure about it

        # scan through the list, look for it and take a running count
        total = 0
        occurs = 0
        seen = False

        for syn, num in syn_freq_list:
            total += num
            if not seen and syn == synset:
                occurs = num
                seen = True


        if not seen:
            return False

        return (occurs / total) > threashold