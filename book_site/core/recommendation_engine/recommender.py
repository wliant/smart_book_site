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

book_features = ['category_encode', 'view_count_normalized', 'average_rating', 'v_mean_compound', 'v_percentage_polarity_review_negative', 'v_percentage_polarity_review_positive' ]


class RecommendationEngine:
    def __init__(self, user_model_fname = 'model/default_recommend_model.h5', base_model_fname = 'model/default_recommend_model.h5' ):
        # doc2vec
        self.book2vec = NovelDoc2Vec()
        self.book2vec.load_model(model_fname = 'model/NovelDoc2Vec-3.model')
        # recommendation engine
        self.recommend_model = load_model(user_model_fname)
        self.base_model = load_model(base_model_fname)
        
        # book data
        self.book_list, self.view_scaler, self.category_le = prepare_book_data()
        self.book_vector = load_book_vector()
    # for transfer learning online
    def learn_preference(self, preferred_enc_cat = [], disliked_enc_cat = []):
        preferred_doc_embeds, preferred_input_data, preferred_score = self._build_learning_pref_data(preferred_enc_cat, 0.9, 1.0)
        while len(preferred_doc_embeds) < 2000:
            print('clone data for prefered cat')
            preferred_doc_embeds_2, preferred_input_data_2, preferred_score_2 = self._build_learning_pref_data(preferred_enc_cat, 0.8, 1.0)
            preferred_doc_embeds = np.vstack((preferred_doc_embeds, preferred_doc_embeds_2))
            preferred_input_data = np.vstack((preferred_input_data, preferred_input_data_2))
            preferred_score = np.concatenate((preferred_score, preferred_score_2))
        disliked_doc_embeds, disliked_input_data, disliked_score = self._build_learning_pref_data(disliked_enc_cat, 0.0, 0.3)
        while len(disliked_doc_embeds) < 2000:
            print('clone data for diliked cat')
            disliked_doc_embeds_2, disliked_input_data_2, disliked_score_2 = self._build_learning_pref_data(disliked_enc_cat, 0.0, 0.3)
            disliked_doc_embeds = np.vstack((disliked_doc_embeds, disliked_doc_embeds_2))
            disliked_input_data = np.vstack((disliked_input_data, disliked_input_data_2))
            disliked_score = np.concatenate((disliked_score, disliked_score_2))
        doc_embeds = np.vstack((preferred_doc_embeds, disliked_doc_embeds))
        x_all = np.vstack((preferred_input_data, disliked_input_data))
        y_all = np.concatenate((preferred_score, disliked_score))
        X_train, X_test, doc_embeds_train, doc_embeds_test, y_train, y_test = train_test_split(x_all, doc_embeds, y_all, test_size=0.25, random_state=42)
        self._transfer_learning([doc_embeds_train, X_train], y_train, [doc_embeds_test, X_test], y_test)
    
    # length = number of book to be recommended
    # samples = number of book to be sampled for recommendation 
    # output is list of book titles, ordered from best score to least score
    def get_recommendation(self, length=5, samples = 1500):
        return self._get_recommendation(self.recommend_model,length, samples)

    # same with get_recommendation but it is using base model (popular based recommendation) for recommendation
    def get_popular_recommendation(self, length = 5, samples = 1500):
        return self._get_recommendation(self.base_model,length, samples)

    # length = number of book to be recommended
    # categories = list of category from which the books to be recommended, it is list of string: ['romance']
    # output is list of book titles, ordered from best score to least score
    def get_recommendation_by_categories(self, categories= [], length=5):
        if len(categories) == 0:
            return self.get_recommendation(length=length, samples=2500)
        row_idx = self._get_idx_by_categories(categories)
        scores = self._calculate_recommendation_score_with_row_ids(row_idx)
        top_scorers_idx = np.flip(np.argsort(scores.flatten())[int(-1*length):])
        return [self.book_list['title'][row_idx[top_scorers_id]] for top_scorers_id in top_scorers_idx]
    
    # input = list of book titles
    # output = score for each book
    def calculate_user_preference_score(self, book_titles):
        return self._calculate_score_with_book_titles(book_titles, self.recommend_model)

    # input = list of book titles
    # output = score for each book
    def calculate_base_model_score(self, book_titles):
        return self._calculate_score_with_book_titles(book_titles, self.base_model)
    
    # ========================================================================
    # ========================== Internal Functions ==========================
    def _get_recommendation(self, model, length, samples):
        random_row_ids = random.sample(range(0, len(self.book_list)), samples)
        scores = self._calculate_recommendation_score_with_row_ids(random_row_ids, recommend_model = model)
        top_scorers_idx = np.flip(np.argsort(scores.flatten())[int(-1*length):])
        return [self.book_list['title'][random_row_ids[top_scorers_id]] for top_scorers_id in top_scorers_idx]

    def _calculate_score_with_book_titles(self, book_titles, model):
        row_ids, book_cat_counts = self._convert_book_titles_to_rows(book_titles)
        scores = self._calculate_recommendation_score_with_row_ids(row_ids, recommend_model = model)
        final_scores = []
        c = 0
        for book_cat_count in book_cat_counts:
            final_scores.append(max(scores[c:c+book_cat_count])[0])
            c = c+book_cat_count
        return final_scores

    def _get_idx_by_categories(self, categories = []):
        row_idx = []
        for id in range(len(self.book_list['book_id'])):
            cat = self.book_list['category'][id]
            if cat in categories:
                row_idx.append(id)
        return row_idx
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
            x_data = []
            for book_feature in book_features:
                feature = self.book_list[book_feature][id]
                if math.isnan(feature):
                    x_data.append(0.0)
                else:
                    x_data.append(feature)
            x_all.append(x_data)
        return np.array(x_all), np.array(doc_vectors)

    def _transfer_learning(self, input_training, label_training, input_validation, label_validation):
        # Transfer Learning last layer
        self.recommend_model.trainable = False
        for i in range(len(self.recommend_model.layers)-2):
            self.recommend_model.layers[i].trainable = False
        tf_output = Dense(1, activation='sigmoid')(self.recommend_model.layers[-2].output)
        tf_model = Model(inputs=self.recommend_model.input, outputs=tf_output)
        tf_model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.005), metrics=['accuracy']) 
        tf_model.fit(input_training, label_training,
          validation_data=(input_validation, label_validation),
          epochs=30, verbose=True,batch_size=32)
        self.tf_acc_logs = tf_model.history.history['accuracy']
        self.tf_val_acc_logs = tf_model.history.history['val_accuracy']
        # unfreeze & fine tune whole layer
        tf_model.trainable = True
        for i in range(len(tf_model.layers)):
            tf_model.layers[i].trainable = True
        tf_model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy']) 
        tf_model.fit(input_training, label_training,
          validation_data=(input_validation, label_validation),
          epochs=20, verbose=True,batch_size=32)
        self.tf_acc_logs.extend(tf_model.history.history['accuracy'])
        self.tf_val_acc_logs.extend(tf_model.history.history['val_accuracy'])
        tf_model.save('model/user_preference_model.h5')
        self.recommend_model = tf_model

    def _calculate_recommendation_score_with_row_ids(self, row_ids, recommend_model = None):
        input_features_1, input_features_doc_vectors = self._get_book_input_features(row_ids)
        if recommend_model == None:
            scores = self.recommend_model.predict([input_features_doc_vectors, input_features_1])
        else:
            scores = recommend_model.predict([input_features_doc_vectors, input_features_1])
        return scores
        
    def _convert_book_titles_to_rows(self, book_titles):
        res = []
        book_cat_counts = []
        for book_title in book_titles:
            book_cat_count = 0
            for i,title in enumerate(self.book_list.index):
                if book_title.lower() == title.lower():
                    res.append(i)
                    book_cat_count += 1
            book_cat_counts.append(book_cat_count)
        return np.array(res), np.array(book_cat_counts)

    

if __name__ == '__main__':
    r = RecommendationEngine(user_model_fname = 'model/user_preference_model.h5')
    print('category index: {}'.format(r.category_le.classes_))
    
    # train using preference, for example user like category index 0,4,8 and don't like 1,5,6,7
    # r.learn_preference(preferred_enc_cat=[0,2,3,8], disliked_enc_cat=[1,5,6,7])
    
    # get best books to be recommended from random sampling
    recommended_books = r.get_recommendation(length = 10, samples = 5000)
    
    # calculate raw score
    scores = r.calculate_user_preference_score(recommended_books)
    base_scores = r.calculate_base_model_score(recommended_books)
    
    print('recommended books : {}'.format(recommended_books))
    print('score: {}'.format(scores))
    print('base_scores: {}'.format(base_scores))
    