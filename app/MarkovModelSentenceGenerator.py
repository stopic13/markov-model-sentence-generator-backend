## Sara Topic

import re
import random
from pprint import pprint
import numpy as np
# A class to generate sentences using a second order markov chain
# In a second-order Markov Model, the probability of transitioning to a state is based only on the current state
# In this implementation a state is an ordered pair of two words i.e. (The, dog)
# Let's say the probability of transitioning from (The, dog) to (has) is 0.4 and the probability of transtioning from (The,dog) to (is) is 0.6. We pick a pseudo-random number between 0 and 1, and let's say it leads us to choose (is). Then the current state becomes (dog, is). This model terminates when it reaches a state that has a period, exclamation point, or question mark as the second element in the tuple.
class MarkovModelSentenceGenerator():
    # __init__()
    #
    # Initializes MarkovModelSentenceGenerator class
    #
    # @return: None
    def __init__(self):
        # mapping of (word1, word2) to (word 3, frequency of word 3 after word 1 and word 2)
        self.freq_dict = {}

    # create_freq_table()
    #
    # Reads in a file and maps each two words in the file to a dictionary of word -> number of occurrences
    #
    # @param file_name: text file to parse
    # @return: None
    def create_freq_table(self, file_name):
        with open(file_name) as file:
            data = file.read()
            # parse out the Chapter and any numbers
            data = data.replace("Chapter", " ")
            data = re.sub(r'[0-9]+', '', data)
            # pattern match - split on spaces but exclude quotation marks
            p = re.compile(r"\w+(?:'\w+)*|[^\w\s\"\”\“\(\)]")
            # get all of the words in the text
            all_text = p.findall(data)
            # look at every three words
            for i in range(len(all_text) - 2):
               curr_state_0 = all_text[i]
               curr_state_1 = all_text[i + 1]
               next_state = all_text[i + 2]
               # we've already seen this word pair
               if (curr_state_0, curr_state_1) in self.freq_dict:
                   # grab the corresponding dictionary
                   transition_states = self.freq_dict[(curr_state_0, curr_state_1)]
                   # either add this state as a possible transition state or increment its frequency
                   if next_state in transition_states:
                       transition_states[next_state] += 1
                   else:
                       transition_states[next_state] = 1
               # this is a new word pair
               else:
                   # make a new dictionary and add this state as a key with 1 as the value
                   transition_states = {}
                   transition_states[next_state] = 1
                   self.freq_dict[(curr_state_0, curr_state_1)] = transition_states

    # compute_weighted_probabilities()
    #
    # Takes each item in self.freq_dict mapping words to frequency an turns them into \
    # weighted probabilities corresponding to their frequency
    #
    # @return: None
    def compute_weighted_probabilities(self):
       # for each pair of words in the dictionary
       for key in self.freq_dict:
           # get all the possible states we could transition to mapped to their frequency
           transition_states = self.freq_dict[key]  # for line in file:
           # sum up the total number of times each word was seen so we know what factor to scale by
           sum = 0
           for word in transition_states:
               sum += transition_states[word]
           # scale each occurrence by dividing by the total number of occurrences
           for word in transition_states:
               transition_states[word] = transition_states[word] / sum

    # pick_random_start_state()
    #
    # Select a random key from self.freq_dict to be our start state
    #
    # @return: a key selected from self.freq_dict
    def pick_random_start_state(self):
        while True:
            word = random.choice(list(self.freq_dict.keys()))
            # make sure the first character of the first word is capital and the second word is not punctuation signifiying \
            #  the end of a sentence - just so sentences are more interesting
            first_char = word[0][0]
            second_word = word[1]
            if first_char.isupper() and (second_word != "?" and second_word != "." and second_word != "!"):
                break
        return word


    # generate_sentence()
    #
    # Use the markov model contained in self.freq_dict to select keys until we reach stop punctuation (. ? !)
    # Print the generated sentence to the console.
    #
    # @return: None
    def generate_sentence(self):
        sentence = []
        word = self.pick_random_start_state()
        # until we reach stop punctuation
        while True:
            sentence.append(word)
            # break if we reached the end of the sentence
            if word[1] == '.' or word[1] == "?" or word[1] == "!":
              #  print(word[1])
                break
            # from the possible transition states, select one based on the weighted probabilities
            d_choices = []
            d_probs = []
            for k in self.freq_dict[word].keys():
                d_choices.append(k)
                d_probs.append(self.freq_dict[word][k])
            choices = np.random.choice(d_choices, 1, p=d_probs)
            # the new state becomes the second word from the current state and the transition state just selected
            word = (word[1], choices[0])
        # print the sentence
        retStr = ""
        for word in sentence:
            retStr += word[0]
            retStr += " "
            print(word[0], end=" ")
        # print the end punctuation
        retStr += sentence[-1][1]
        print(sentence[-1][1])
        retStr = retStr.replace(" ,", ",")
        retStr = retStr.replace(" ;", ";")
        retStr = retStr.replace(" .", ".")

        return retStr
#
# sentence_generator = MarkovModelSentenceGenerator()
# #sentence_generator.create_freq_table("foo.txt")
# # # sentence_generator.create_freq_table("persuasion.txt")
# # # sentence_generator.create_freq_table("sleepingbeauty.txt")
# # sentence_generator.create_freq_table("madamebovary.txt")
#
# sentence_generator.create_freq_table("app/foo.txt")
#
# print(sentence_generator.freq_dict)
#
# sentence_generator.create_freq_table("app/bar.txt")
# print(sentence_generator.freq_dict)
#
#
# sentence_generator.compute_weighted_probabilities()
# print(sentence_generator.freq_dict)
# # sentence_generator.generate_sentence()
