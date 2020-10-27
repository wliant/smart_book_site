import csv
import gensim.models as g
import gensim
import smart_open
import pandas as pd
import os
import re
import numpy as np
from sklearn.model_selection import train_test_split
import random
import math
from keras.models import Model
from keras.layers import Dense
from keras.models import load_model
from keras.optimizers import Adam
from utils import load_book_vector, prepare_book_data
from doc2vec import NovelDoc2Vec

book_features = ['category_encode', 'view_count_normalized', 'average_rating', 'percent_positive', 'percent_negative', 'percent_neutral', 'overall_sentiment' ]

class RecommendationEngine:
    def __init__(self, model_fname = 'model/default_recommend_model.h5'):
        # doc2vec
        self.book2vec = NovelDoc2Vec()
        self.book2vec.load_model(model_fname = 'model/NovelDoc2Vec-3.model')
        # recommendation engine
        self.base_recommend_movel = load_model(model_fname)
        # self.base_recommend_movel.trainable = False
        # for i in range(len(self.base_recommend_movel.layers)-2):
        #     self.base_recommend_movel.layers[i].trainable = False
        self.tf_recommend_model = self.base_recommend_movel
        
        # book data
        self.book_list, self.view_scaler, self.category_le = prepare_book_data()
        self.book_vector = load_book_vector()

    def learn_preference(self, preferred_enc_cat = [], preferred_book_titles = [], disliked_enc_cat = [], disliked_book_titles = [] ):
        preferred_doc_embeds, preferred_input_data, preferred_score = self._build_learning_pref_data(preferred_enc_cat, 0.85, 1.0)
        neutral_prefs = []
        for i in range(len(self.category_le.classes_)):
            if i not in preferred_enc_cat and i not in disliked_enc_cat:
                neutral_prefs.append(i)
        neutral_doc_embeds, neutral_input_data, neutral_score = self._build_learning_pref_data(neutral_prefs, 0.4, 0.65)
        disliked_doc_embeds, disliked_input_data, disliked_score = self._build_learning_pref_data(disliked_enc_cat, 0.0, 0.4)
        doc_embeds = np.vstack((preferred_doc_embeds, disliked_doc_embeds))
        x_all = np.vstack((preferred_input_data, disliked_input_data))
        y_all = np.concatenate((preferred_score, disliked_score))
        X_train, X_test, doc_embeds_train, doc_embeds_test, y_train, y_test = train_test_split(x_all, doc_embeds, y_all, test_size=0.25, random_state=42)
        self._transfer_learning([doc_embeds_train, X_train], y_train, [doc_embeds_test, X_test], y_test)

    def get_recommendation(self, length=5, samples = 5000):
        random_row_ids = random.sample(range(0, len(self.book_list)), samples)
        scores = self._calculate_recommendation_score_with_row_ids(random_row_ids)
        top_scorers_idx = np.argsort(scores.flatten())[int(-1*length):]
        return [self.book_list['title'][random_row_ids[top_scorers_id]] for top_scorers_id in top_scorers_idx]
        
    def calculate_recommendation_score(self, book_titles):
        row_ids = self._convert_book_titles_to_rows(book_titles)
        return self._calculate_recommendation_score_with_row_ids(row_ids)

    def _build_learning_pref_data(self, enc_cats, min_score, max_score):
        all_inputs, doc_embeds = self._get_book_input_features(range(0,len(self.book_list)))
        scores = []
        selected_inputs = []
        selected_doc_embeds = []
        for i, input in enumerate(all_inputs):
            if input[0] in enc_cats:
                scores.append(np.round(random.uniform(min_score,max_score)))
                selected_inputs.append(input)
                selected_doc_embeds.append(doc_embeds[i])
        return np.array(selected_doc_embeds), np.array(selected_inputs), np.array(scores)

    def _get_book_input_features(self, row_ids):
        x_all = []
        doc_vectors = []
        for id in row_ids:
            book_id = self.book_list['book_id'][id]
            if book_id in self.book_vector.keys():
                doc_vectors.append([self.book_vector[book_id]])
            else:
                doc_vectors.append([np.zeros(256)])
            x_all.append([self.book_list[book_feature][id] for book_feature in book_features])
        return np.array(x_all), np.array(doc_vectors)

    def _transfer_learning(self, input_training, label_training, input_validation, label_validation):
        tf_output = Dense(1, activation='sigmoid')(self.base_recommend_movel.layers[-2].output)
        tf_model = Model(inputs=self.base_recommend_movel.input, outputs=tf_output)
        tf_model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.005), metrics=['accuracy']) 
        tf_model.fit(input_training, label_training,
          validation_data=(input_validation, label_validation),
          epochs=16, verbose=True,batch_size=32)
        tf_model.save('model/user_preference_model.h5')
        self.tf_recommend_model = tf_model

    def _calculate_recommendation_score_with_row_ids(self, row_ids):
        input_features_1, input_features_doc_vectors = self._get_book_input_features(row_ids)
        scores = self.tf_recommend_model.predict([input_features_doc_vectors, input_features_1])
        return scores
        
    def _convert_book_titles_to_rows(self, book_titles):
        res = []
        for book_title in book_titles:
            for i,title in enumerate(self.book_list.index):
                if book_title.lower() == title.lower():
                    res.append(i)
        return res
    
if __name__ == '__main__':
    r = RecommendationEngine()
    print('category index: {}'.format(r.category_le.classes_))
    
    # train using preference, for example user like category index 0,4,8 and don't like 1,5,6,7
    r.learn_preference(preferred_enc_cat=[0,4,8], disliked_enc_cat=[1,5,6,7])
    
    # get best books to be recommended from random sampling
    recommended_books = r.get_recommendation(length = 10, samples = 5000)
    
    # calculate raw score
    scores = r.calculate_recommendation_score(recommended_books)
    
    print('recommended books : {}'.format(recommended_books))
    print('score: {}'.format(scores))