from gensim import corpora
from gensim.models import LdaModel
from collections import Counter
import pandas as pd

class LdaModeling:
    def __init__(self, tokenized_texts, video_id,total_topics, number_words):
        """
        Inisialisasi model LDA.
        
        :param tokenized_texts: List of tokenized documents (list of lists of tokens).
        :param total_topics: Jumlah topik yang ingin dibangun.
        :param number_words: Jumlah kata yang ingin ditampilkan per topik.
        """
        self.tokenized_texts = tokenized_texts["Transcription_tokens_WSW"]
        self.output_path_imp_wcount = f"data/outputs/df_imp_wcount_{video_id}.csv"
        self.output_path_dominan_topic = f"data/outputs/df_dominan_topic_{video_id}.csv"
        self.total_topics = total_topics
        self.number_words = number_words
        self.dictionary = None
        self.corpus = None
        self.lda_model = None

    def create_corpus(self):
        # Created Dict from  tokenized texts
        self.dictionary = corpora.Dictionary(self.tokenized_texts) 
        # Mengonversi tokenized texts menjadi format yang sesuai untuk LDA
        self.corpus = [self.dictionary.doc2bow(text) for text in self.tokenized_texts]
        print("Corpus created:", self.corpus)
        return self.corpus

    def build_model(self):
        # Build model  LDA
        if self.corpus is None or self.dictionary is None:
            raise ValueError("Corpus and dictionary must be created before building the model.")
        
        self.lda_model = LdaModel(self.corpus, num_topics=self.total_topics, id2word=self.dictionary, passes=15)
        return self.lda_model

    def print_topics(self):
        if self.lda_model is None:
            raise ValueError("LDA model has not been built yet.")
        
        for idx, topic in self.lda_model.print_topics(num_words=self.number_words):
            print(f'Topic {idx}: {topic}')
    def word_count_of_topic_keywords(self):
            # Count the occurrences of each word in the documents
            data_flat = [word for text in self.tokenized_texts for word in text]
            counter = Counter(data_flat)

            # Get topics and their keywords
            topics = self.lda_model.show_topics(formatted=False)
            out = []
            for i, topic in topics:
                for word, weight in topic:
                    out.append([word, i, weight, counter[word]])

            # Create a DataFrame to display the results
            df_imp_wcount = pd.DataFrame(out, columns=['word', 'topic_id', 'importance', 'word_count'])
            df_imp_wcount.to_csv(self.output_path_imp_wcount, index=False)
    def format_topics_sentences(self, corpus=None, texts=None):
        # Init output
        sent_topics_df = pd.DataFrame()

        # Get main topic in each document
        for i, row_list in enumerate(self.lda_model[corpus]):
            row = row_list[0] if self.lda_model.per_word_topics else row_list            
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = self.lda_model.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    # Create a Series for the current document's dominant topic
                    topic_data = pd.Series([int(topic_num), round(prop_topic, 4), topic_keywords])
                    # Concatenate the Series to the DataFrame
                    sent_topics_df = pd.concat([sent_topics_df, topic_data.to_frame().T], ignore_index=True)
                else:
                    break

        sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

        # Add original text to the end of the output
        contents = pd.Series(texts)
        sent_topics_df = pd.concat([sent_topics_df, contents.rename("Original_Text")], axis=1)
        sent_topics_df.to_csv(self.output_path_dominan_topic, index=False)
        return sent_topics_df
