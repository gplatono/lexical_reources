import ast

class BrownFrequency:
    ''' Uses Brown Corpus to determine the frequency of words '''

    def __init__(self):
        with open(".\\Resources\\brown_freqs.txt", "r") as f:
            list1 = ast.literal_eval(f.readline())
            list2 = ast.literal_eval(f.readline())
            list3 = ast.literal_eval(f.readline())
        self.single_dictionary = {key:value for (key, value) in list1}
        self.double_dictionary =  {key:value for (key, value) in list2}
        self.triple_dictionary =  {key:value for (key, value) in list3}

    def get_freq(self, word):
        word = word.replace("_", " ")
        num_spaces = len(word.split())-1
        if num_spaces == 0:
            if not word in self.single_dictionary.keys():
                return 0
            return self.single_dictionary[word]
        if num_spaces == 1:
            if not word in self.double_dictionary.keys():
                return 0
            return self.double_dictionary[word]
        if num_spaces == 2:
            if not word in self.triple_dictionary.keys():
                return 0
            return self.triple_dictionary[word]
        return 0

    def is_frequent(self, word, threashold):
        return self.get_freq(word) >= threashold