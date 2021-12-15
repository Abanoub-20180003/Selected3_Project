# Gerges & Ehab

import re
import string
from nltk.corpus import stopwords
from nltk.stem.isri import ISRIStemmer
import csv


class CleanData(object):
    
    def __init__(self, authors, titles, categories, links, cleaned_data_file, header, delimiter):
        print("Start Cleaning....") 
        filtered_authors    = self._clean(authors)
        filtered_titles     = self._clean(titles)
        filtered_categories = self._clean(categories)
        ## Write Cleaned Scrapped Data Into New Text File
        print("-- SAVING Cleaned Data In csv File --")
        with open(cleaned_data_file, "w", encoding='utf-8-sig') as file:
            wr = csv.writer(file)
            wr.writerow(header)
            lines1 = filtered_authors.split(delimiter)
            lines2 = filtered_titles.split(delimiter)
            lines3 = filtered_categories.split(delimiter)
            
            for (l1, l2, l3, l4) in zip(lines1, lines2, lines3, links):
                s = u','.join([str(l1), str(l2), str(l3), str(l4)]) + u'\n'
                file.write(s)
                
        print("Cleaning Finished!\n")  
      

    def _clean(self, text):
        ## 1.1 Replace punctuations with a white space
        remove_punctuations = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
        ## 1.2 Normalize
        normalized = re.sub("گ", "ك", remove_punctuations)
        normalized = re.sub("ى", "ي", normalized)
        ## 2.1 Remove Non-Arabic Words
        remove_nonarabic = re.sub(r'\s*[A-Za-z]+\b', '' , normalized)
        ## 2.2 Remove Stop Words.
        stop_words = set(stopwords.words('arabic'))
        filtered_sentence = ' '.join([word for word in remove_nonarabic.split() 
                                          if word not in stop_words])
        ## 3.0 Stemming
        st = ISRIStemmer()
        st.stem(filtered_sentence)
        
        return filtered_sentence
    
