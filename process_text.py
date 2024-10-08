import re
from collections import Counter
import pandas as pd
import pickle
import pkg_resources
from symspellpy import SymSpell, Verbosity

class Text():
    def __init__(self):
        self.w=[]
        self.file_name_date=None
        self.tag=None

    def filter_words(self):
        with open(r'data\recognized.txt', 'r') as f:
            self.file_name_data = f.read()
            self.file_name_data = self.file_name_data.lower()
            #correcting text.
            self.file_name_data=re.sub('[^A-Za-z0-9 ]+', '', self.file_name_data)
            self.file_name_data=(self.auto_correct(self.file_name_data))
            #finding words longer than 6 letters.
            self.file_name_data = re.sub(r"\b\w{1,6}\b", "", self.file_name_data)
            self.w = re.findall(r'\w+', self.file_name_data)
            self.w=set(self.w)

    def count_words(self):
        str_list= self.file_name_data.split()
        self.frequency = Counter(str_list)
        #for word in self.frequency:
            #print('Frequency of ', word, 'is :', self.frequency[word])

    def difficulty(self):
        self.glossary_words=[]
        total=sum(self.frequency.values())
        for word,freq in self.frequency.items():
            if (freq/total)<1:
                self.glossary_words.append(word)
        self.glossary_words.sort()

    def auto_correct(self,input_term=''):
        sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
        sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
        suggestions = sym_spell.lookup_compound(input_term, max_edit_distance=2)
        for suggestion in suggestions:
            return(suggestion.term)


    def definitions(self):
        with open('data/dictionary.pkl', 'rb') as f:
            data = pickle.load(f)
        self.word_info={}
        self.recognized_words=[]
        for word in self.glossary_words:
           try: 
               data[word]=data[word].split('3')[0]

           except KeyError:
               pass
           
           else:
               self.recognized_words.append(word)
               self.word_info.update({word:[data[word]]})
               

    def write_to_dataframe(self):
        self.df=pd.DataFrame(self.word_info)

    def run(self):
        text=Text()
        text.filter_words()
        text.count_words()
        text.difficulty()
        text.definitions()
        return text.recognized_words,text.word_info

def main():
        text=Text()
        text.filter_words()
        text.count_words()
        text.difficulty()
        text.definitions()
        text.write_to_dataframe()
        print(text.glossary_words)
        print(text.word_info)


if __name__=='__main__':
    main()
