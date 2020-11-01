import tensorflow as tf
from tensorflow import keras as ks
from core.models import *
import numpy as np
import spacy
import pickle
from gensim.models import LdaModel
from nltk.tokenize import word_tokenize

dimension = 20


i = tf.keras.Input(shape=(dimension))
x = ks.layers.Dense(2048, activation='relu')(i)
x = ks.layers.Dense(2048, activation='relu')(x)
x = ks.layers.Dense(2048, activation='relu')(x)
x = ks.layers.Dense(9, activation='sigmoid', name='prediction_layer')(x)
model = ks.Model(i, x)

weights_file = "/usr/classification.hdf5"
lda_model = pickle.load(open("/usr/lda_topics.pkl", "rb"))
dictionary = pickle.load(open("/usr/dictionary.pkl", "rb"))

model.load_weights(weights_file)

class_mapping = [
    "adventure",
    "fantasy",
    "historical",
    "horror",
    "mystery",
    "romance",
    "science-fiction",
    "thriller",
    "young-adult"
]

def get_topic_distribution(unseen_text):
    tokens= word_tokenize(unseen_text)
    return lda_model[dictionary.doc2bow(tokens)][0] # get topic probability distribution for a documen


def convert(text):
    v = get_topic_distribution(text)
    target = [a[1] for a in v]
    to_add = dimension - len(target)
    return np.array([target + [0 for _ in range(to_add)]])


def classify(book_id):
    book_contents = BookContent.objects.filter(book__id=book_id)
    text = " ".join([bc.content for bc in book_contents])

    result = model.predict(convert(text))[0]
    category = class_mapping[np.argmax(result)]

    print("found category {}".format(category))

    book = Book.object.get(pk=book_id)
    before = book.categories.all()
    for cat in before:
        book.categories.remove(cat)

    c = Category.objects.get(name=category)
    book.categories.add(c)
    book.save()


