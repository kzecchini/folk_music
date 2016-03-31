
# coding: utf-8

# In[1]:

import cPickle as pickle
import numpy as np
import pandas as pd
from nltk import ngrams, skipgrams


# # Make Markov class

# In[3]:

import random
from collections import defaultdict



class Markov(object):

    def __init__(self, list_tokens):
        self.cache = defaultdict(list)
        self.list_tokens = list_tokens
        self.tokens_size = len(self.list_tokens)
        self.database()

    def triples(self):
        """ Generates triples from the given data string. So if our string were
            "What a lovely day", we'd generate (What, a, lovely) and then
            (a, lovely, day).
        """
        for tokens in self.list_tokens:
            if len(tokens) < 3:
                return

            for i in range(len(tokens) - 2):
                yield (tokens[i], tokens[i+1], tokens[i+2])

#     Considered using just unigram to predict next note... perhaps would create wider higher order grams
#     and allow for more randomization.
    
#     def doubles(self):
#         for tokens in self.list_tokens:
#             if len(tokens) < 2:
#                 return

#             for i in range(len(tokens) - 1):
#                 yield (tokens[i], tokens[i+1])

    def database(self):
        for w1, w2 in self.doubles():
            key = w1
            self.cache[key].append(w2)
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            self.cache[key].append(w3)

    def generate_markov_text(self, size=25):
        seed_list = random.randint(0, self.tokens_size-1)
        seed = random.randint(0, len(self.list_tokens[seed_list])-3)
        seed_word, next_word = self.list_tokens[seed_list][seed], self.list_tokens[seed_list][seed+1]
        w1, w2 = seed_word, next_word
        gen_words = []
        for i in xrange(size):
            gen_words.append(w1)
            try:
                w1, w2 = w2, random.choice(self.cache[(w1, w2)])
            except IndexError:
                try:
                    w1, w2 = w2, random.choice(self.cache[w2])
                except IndexError:
                    seed_list2 = random.randint(0, self.tokens_size-1)
                    new_w2 = self.list_tokens[seed_list2][random.randint(0, len(self.list_tokens[seed_list2])-3)]
                    w1, w2 = w2, new_w2
        gen_words.append(w2)
        return gen_words


# In[ ]:



