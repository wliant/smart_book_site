import csv
import gensim.models as g
import gensim
import smart_open
import pandas as pd
import os
import re
import numpy as np
from sklearn import preprocessing


def read_novel(fname, skip_interval=1):
    with smart_open.open(fname, encoding="utf-8") as f:
        tokens = []
        c = 1
        for i, line in enumerate(f):
            new_tokens = gensim.utils.simple_preprocess(line)
            if len(tokens) + len(new_tokens) > 256:
                if c%skip_interval == 0:
                    yield gensim.models.doc2vec.TaggedDocument(tokens, [0])
                tokens = []
                c += 1
            tokens.extend(new_tokens)

def prepare_book_data():
    book_list = pd.read_csv('data/books_list.csv', header=0)
    sentiment_list =  pd.read_csv('data/goodreads_rating_with_sentiment.csv', header=0)
    sentiment_list = sentiment_list.drop_duplicates(subset=['old_title'], keep='first')
    sentiment_list = sentiment_list.drop(['old_id', 'new_id', 'new_title', 'image_url', 'small_image_url', 'author', 'author_id'], axis = 1)
    book_list = book_list.set_index('title').join(sentiment_list.set_index('old_title'))
    book_list['title'] = book_list.index
    ## parse view into view count
    view_regex = re.compile(r'\((?P<view>[0-9].*) view\)')
    book_list['view_count'] = book_list.apply(lambda x: int(view_regex.match(x['view']).group('view').replace(',','')), axis = 1)
    ## Normalize view count
    x = []
    cats = []
    for i,view_count in enumerate(book_list['view_count']):
        x.append([view_count])
        cats.append(book_list['category'][i])
    scaler = preprocessing.StandardScaler()
    x_scaled = scaler.fit_transform(x)
    ## Label category
    le = preprocessing.LabelEncoder()
    cat_enc = le.fit_transform(cats)
    book_list = book_list.assign(view_count_normalized=x_scaled.flatten())
    book_list = book_list.assign(category_encode=cat_enc)
    # book_list_sorted = book_list.sort_values('view_count', kind = 'mergesort', ascending=False)
    return book_list, scaler, le

def save_book_vector(book_ids, vector_embeds, first_time = False):
    vector_size = len(vector_embeds[0])
    fieldnames = ['book_id']
    for i in range(vector_size):
        fieldnames.append('w{}'.format(i))
    data = []
    for (i,book_id) in enumerate(book_ids):
        item = {
            'book_id': book_id
        }
        for j in range(vector_size):
            item['w{}'.format(j)] = vector_embeds[i][j]
        data.append(item)
    mode = 'a'
    if first_time:
        mode = 'w'
    with open('model/book_vector_embed.csv',mode, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if first_time:
            writer.writeheader()
        writer.writerows(data)

def load_book_vector(vector_size = 256):
    data = {}
    with open('model/book_vector_embed.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            vector = []
            for i in range(vector_size):
                vector.append(row['w{}'.format(i)])
            data[row['book_id']] = np.array(vector)
    return data
   

    