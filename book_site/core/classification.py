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
    ldamallet = LdaModel.load("/usr/lda_model")
    tokens = tokens= word_tokenize(unseen_text)
    return ldamallet[dictionary.doc2bow(tokens)] # get topic probability distribution for a documen


def convert(text):
    v = get_topic_distribution(text)
    return [[a[1] for a in v]]


def classify(book_id):
    book_contents = BookContent.object.filter(book__id=book_id)
    text = " ".join([bc.content for bc in book_contents])

    result = model.predict(convert(text))[0]
    category = class_mapping[np.argmax(result)]

    book = Book.object.get(pk=book_id)
    before = book.categories.all()
    for cat in before:
        book.categories.remove(cat)

    c = Category.objects.get(name=category)
    book.categories.add(c)
    book.save()


