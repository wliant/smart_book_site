import csv
import gensim.models as g
import gensim
import smart_open
import pandas as pd
import os
import re
import numpy as np
from utils import read_novel

class NovelDoc2Vec:
    def __init__(self, vector_size = 256, min_count=3):
        self.gensim_model = gensim.models.doc2vec.Doc2Vec(vector_size=vector_size, min_count=min_count, epochs=25)
        self.book_list = pd.read_csv('data/books_list.csv', header=0)
    def begin_training_all_data(self, model_fname = 'model/NovelDoc2Vec.model'):
        count = 0
        save_iteration = 50
        cat_map = {}
        for i, book_id in enumerate(self.book_list['book_id']):
            total_cat = 0
            cat = self.book_list['category'][i]
            if cat in cat_map.keys():
                total_cat = int(cat_map[cat])
            if total_cat > 500:
                continue
            
            corpus_fname = 'data/book_content/{}.txt'.format(str(book_id))
            if os.path.isfile(corpus_fname):
                print('training book {}'.format(book_id))
                self.model_training(corpus_fname, first_time = (i==0), skip_interval=3)
                cat_map[cat] = total_cat + 1
            if count % save_iteration == 0 :
                print('saving the model')
                self.save_model(model_fname=model_fname)
            count += 1
    def model_training(self, corpus_fname, first_time = False, skip_interval=2):
        train_corpus = list(read_novel(corpus_fname, skip_interval=skip_interval))
        if first_time:
            self.gensim_model.build_vocab(train_corpus, update=False)
        else:
            self.gensim_model.build_vocab(train_corpus, update=True)
        self.gensim_model.train(train_corpus, total_examples=self.gensim_model.corpus_count, epochs=self.gensim_model.epochs)
        
    def calculate_doc_vectors(self, corpus_fname):
        corpus = list(read_novel(corpus_fname, skip_interval=2))
        avg_model = [] 
        count = 1
        for row in corpus:
            a = self.gensim_model.infer_vector(row[0])
            if len(avg_model) == 0:
                avg_model = a
                continue
            avg_model = (avg_model * count + a) / (count + 1)
            count += 1
        return avg_model
    
    def get_doc_vectors_statistics(self, corpus_fname, skip_interval=2):
        corpus = list(read_novel(corpus_fname, skip_interval=skip_interval))
        sections = [] 
        for row in corpus:
            a = self.gensim_model.infer_vector(row[0], epochs=20)
            sections.append(a)
        return [np.mean(sections, axis=0), np.median(sections, axis=0), np.std(sections, axis=0)]
    def save_model(self, model_fname = 'model/NovelDoc2Vec.model'):
        self.gensim_model.save(model_fname)
    def load_model(self, model_fname = 'model/NovelDoc2Vec.model'):
        self.gensim_model = g.Doc2Vec.load(model_fname)