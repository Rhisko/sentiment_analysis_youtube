import pandas as pd
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import string
import nltk
from nltk.tokenize import word_tokenize 
from nltk.probability import FreqDist
from config.config import list_stopwords_additional,slang_to_formal

nltk.download('punkt_tab')
nltk.download('stopwords')

list_stopwords = stopwords.words("indonesian")
list_stopwords.extend(list_stopwords_additional)

class DataPreprocessor:
    def __init__(self, file_path,video_id):
        self.file_path = file_path
        self.df = None
        self.output_path = f"data/outputs/transcription_{video_id}_cleaned.csv"

    def load_data(self):
        self.df = pd.read_csv(self.file_path)
        print(self.df.head())


    def preprocess(self):
        def remove_tweet_special(text):
            # remove tab, new line, ans back slice
            text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
            # remove non ASCII (emoticon, chinese word, .etc)
            text = text.encode('ascii', 'replace').decode('ascii')
            # remove mention, link, hashtag
            text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", text).split())
            # remove incomplete URL
            return text.replace("http://", " ").replace("https://", " ")
        #remove number
        def remove_number(text):
            return  re.sub(r"\d+", "", text)
        #remove punctuation
        def remove_punctuation(text):
            return text.translate(str.maketrans("","",string.punctuation))
        #remove whitespace leading & trailing
        def remove_whitespace_LT(text):
            return text.strip()
        #remove multiple whitespace into single whitespace
        def remove_whitespace_multiple(text):
            return re.sub('\s+',' ',text)
        # remove single char
        def remove_singl_char(text):
            return re.sub(r"\b[a-zA-Z]\b", "", text)       
        #convert to lower case
        def convert_to_lower(text):          
            text = text.lower()  # Change To lower
            return text
        # NLTK word tokenize 
        def word_tokenize_wrapper(text):
            return word_tokenize(text)
        
        
        # NLTK calc frequency distribution
        def freqDist_wrapper(text):
            return FreqDist(text)

        
        #remove stopword pada list token
        def stopwords_removal(words):
            return [word for word in words if word not in set(list_stopwords)]
        
        def replace_slang(text):
            words = text.split()
            replaced_words = [slang_to_formal.get(word.lower(), word) for word in words]
            return ' '.join(replaced_words)

        self.df['Transcription_after_preprocess'] = self.df['Transcription'].apply(remove_tweet_special)
        self.df['Transcription_after_preprocess'] = self.df['Transcription_after_preprocess'].apply(remove_number)
        self.df['Transcription_after_preprocess'] = self.df['Transcription_after_preprocess'].apply(remove_punctuation)
        self.df['Transcription_after_preprocess'] = self.df['Transcription_after_preprocess'].apply(remove_whitespace_LT)
        self.df['Transcription_after_preprocess'] = self.df['Transcription_after_preprocess'].apply(remove_whitespace_multiple)
        self.df['Transcription_after_preprocess'] = self.df['Transcription_after_preprocess'].apply(remove_singl_char)
        self.df['Transcription_after_preprocess'] = self.df['Transcription_after_preprocess'].apply(convert_to_lower)
        self.df['Transcription_after_preprocess'] = self.df['Transcription_after_preprocess'].apply(replace_slang)
        
        self.df['Transcription_tokens'] = self.df['Transcription_after_preprocess'].apply(word_tokenize_wrapper)
        
        self.df['Transcription_fdist'] = self.df['Transcription_tokens'].apply(freqDist_wrapper)
        print(f"Transcription fdist : {self.df['Transcription_fdist'].head().apply(lambda x : x.most_common())}")
        
        self.df['Transcription_tokens_WSW'] = self.df['Transcription_tokens'].apply(stopwords_removal)

        #Write To CSV 
        self.df.to_csv(self.output_path, index=False)
        
        #Write To TXT
        self.df['Transcription'].to_csv("data/outputs/transcription_original.txt",sep='\t', index=False)
        self.df['Transcription_after_preprocess'].to_csv("data/outputs/transcription_afterprocess.txt",sep='\t', index=False)
        self.df['Transcription_tokens'].to_csv("data/outputs/transcription_tokenize.txt",sep='\t', index=False)
        self.df['Transcription_fdist'].to_csv("data/outputs/transcription_fdist.txt",sep='\t', index=False)     
        self.df['Transcription_tokens_WSW'].to_csv("data/outputs/Transcription_tokens_WSW.txt",sep='\t', index=False)     
        return self.df

    def vectorize(self):
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(self.df['Transcription_after_preprocess'])
        return X, vectorizer
