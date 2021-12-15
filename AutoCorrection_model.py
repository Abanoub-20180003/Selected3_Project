# Eriny 

import re
import string
from collections import Counter
import numpy as np
import csv


class SpellChecker(object):

    def read_corpus(self, filename):
        with open(filename, "r", encoding='utf-8-sig') as file:
            lines = file.readlines() ## Read The File Line By Line
            words = []
            for line in lines:
              words += re.findall(r'\w+', line.lower()) ## Put Each Word In Its Lowercase.
    
        return words
    
    def read_corpus_lines(self, filename):
        lines1 = []
        lines2 = []
        lines3 = []
        lines4 = []
        with open(filename, "r", encoding='utf-8-sig') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                lines1.append(row["اسم الكاتب"])
                lines2.append(row["عنوان الكتاب"])
                lines3.append(row["نوع الكتاب"])
                lines4.append(row["رابط الكتاب"])
        return lines1, lines2, lines3, lines4
    
    def get_count(self, word_list):
        word_count_dict = {}  ## Each Word Count
        word_count_dict = Counter(word_list)
        return word_count_dict
    
    def get_probs(self, word_count_dict):
        ## 𝑃(𝑤ᵢ) = 𝐶(𝑤ᵢ) / M 
        m = sum(word_count_dict.values())
        word_probs = {w: word_count_dict[w] / m for w in word_count_dict.keys()}
        
        return word_probs
    
    def _split(self, word):
        return [(word[:i], word[i:]) for i in range(len(word) + 1)]
    
    def _delete(self, word):
        return [l + r[1:] for l,r in self._split(word) if r]
    
    def _swap(self, word):
        return [l + r[1] + r[0] + r[2:] for l, r in self._split(word) if len(r)>1]
    
    def _replace(self, word):
        letters = string.ascii_lowercase
        return [l + c + r[1:] for l, r in self._split(word) if r for c in letters]
    
    def _insert(self, word):
        letters = string.ascii_lowercase
        return [l + c + r for l, r in self._split(word) for c in letters]
       
    def _edit1(self, word):  
        return set(self._delete(word) + self._swap(word) + 
                   self._replace(word) + self._insert(word))
    
    def _edit2(self, word):
      return set(e2 for e1 in self._edit1(word) for e2 in self._edit1(e1))
    
    def correct_spelling(self, word, vocabulary, word_probability):
        if word in vocabulary:
            #print(f"\n'{word}' is already correctly spelt")
            return 
        
        suggestions = self._edit1(word) or self._edit2(word) or [word]
        best_guesses = [w for w in suggestions if w in vocabulary]
          
        return [(w, word_probability[w]) for w in best_guesses]
            
    
    def correct_word(self, word, corrections):
        if corrections:
            print('\nSuggested Words:', corrections)
            probs = np.array([c[1] for c in corrections])
            ## Get The Index Of The Best Suggested Word (Higher Probability)
            best_ix = np.argmax(probs) 
            correct = corrections[best_ix][0]
            print(f"\n'{correct}' is Suggested for '{word}'")
            return correct        
        