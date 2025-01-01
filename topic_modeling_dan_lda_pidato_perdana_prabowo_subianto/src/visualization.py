import pyLDAvis.gensim_models
import pyLDAvis

class Visualization:
    def __init__(self, lda_model, corpus, dictionary):
        self.lda_model = lda_model
        self.corpus = corpus
        self.dictionary = dictionary

    def save(self, filename):
        # Prepare the visualization
        vis = pyLDAvis.gensim_models.prepare(self.lda_model, self.corpus, self.dictionary)
        # Save the visualization to an HTML file
        pyLDAvis.save_html(vis, filename)
        print(f"Visualisasi disimpan ke {filename}")
