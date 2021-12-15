# Abanoub Kamal

import Scrapping_model
import CleanData_model
import pandas as pd
import csv
import AutoCorrection_model

header = ["Author", "Book_Name", "Book_Category", "Book_url"]
extracted_data_file     = './extracted_data.csv'
cleaned_data_file       = './cleaned_data.csv'
autocorrected_data_file = './autocorrected_extracted_data.csv'
dictionary_file         = './arabic-wordlist-1.6.txt'
delimiter = '،،،،'

def __init__():
    url= "https://www.arab-books.com//page/{}"
    
    # scrap data from the website and store it in csv file 
    Scrapping_model.ScrapData(url)
    
    #cleaning data
    authors, titles, categories, links = split_file(extracted_data_file)
    authors = list(map(lambda s: s+delimiter, authors))
    titles = list(map(lambda s: s+delimiter, titles))
    categories = list(map(lambda s: s+delimiter, categories))
    CleanData_model.CleanData(str(authors), str(titles), str(categories), links, cleaned_data_file, header, delimiter)
    
    ### AutoCorrection
   
    spell_checker = AutoCorrection_model.SpellChecker()
    print("Starting AutoCorrecting Misspelling....\n")
    base_words = spell_checker.read_corpus(dictionary_file)
    vocabs = set(base_words) ## Vocabulary (Unique Words)

    word_dict_counts = spell_checker.get_count(base_words)
    word_prob   = spell_checker.get_probs(word_dict_counts) 

    authors, titles, categories, links = spell_checker.read_corpus_lines(cleaned_data_file)   
    authors = list(map(lambda orig_string: orig_string+'،،،،', authors))   
    titles = list(map(lambda orig_string: orig_string+'،،،،', titles))   
    categories = list(map(lambda orig_string: orig_string+'،،،،', categories))   

    correct_authors    = autocorrect_misspellings(authors, vocabs, word_prob, spell_checker)
    correct_titles     = autocorrect_misspellings(titles, vocabs, word_prob , spell_checker)
    correct_categories = autocorrect_misspellings(categories, vocabs, word_prob, spell_checker)

    with open(autocorrected_data_file, "w", encoding='utf-8-sig') as file:
        print("-- SAVING Autocorrected Data In csv File --")
        wr = csv.writer(file)
        wr.writerow(header)
        
        lines1 = correct_authors.split(delimiter)
        lines2 = correct_titles.split(delimiter)
        lines3 = correct_categories.split(delimiter)
        
        for (l1, l2, l3, l4) in zip(lines1, lines2, lines3, links):
            s = u','.join([str(l1), str(l2), str(l3), str(l4)]) + u'\n'
            file.write(s)
            
  
    #Clustering Data 
    data_df = pd.read_csv(r"E:\#Universty_Resources\Level 4\Selected-3\Project\autocorrected_extracted_data.csv") 
    # book_list = data_df.Book_Category.dropna().unique()
    print(data_df)
    print("enter book name")
    book = str(input())
    book_info = data_df.loc[data_df['Book_Name'].str.contains(book)]
    print("Book Type:", book_info.Book_Category )
    
    
    
            
    


def autocorrect_misspellings(lines, vocabs, word_prob, spell_checker):
    correct_lines = []
    for line in lines:
        for word in line.split(' '):
            corrections = spell_checker.correct_spelling(word, vocabs, word_prob)
            correct     = spell_checker.correct_word(word, corrections)
            if correct:
                correct_lines.append(correct)
            else:
                correct_lines.append(word)

    correct_lines = ' '.join(correct_lines)
    
    return correct_lines
    
def split_file(filename):
    data = pd.read_csv(filename)
    
    # converting column data to list
    authors = data['Author'].tolist()
    titles = data["Book_Name"].tolist()
    categories = data["Book_Category"].tolist()
    links = data["Book_url"].tolist()
    return authors, titles, categories, links


        
        

