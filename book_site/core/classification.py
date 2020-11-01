import tensorflow as tf
from tensorflow import keras as ks
from core.models import *
import numpy as np


dimension = 20


i = tf.keras.Input(shape=(dimension))
x = ks.layers.Dense(2048, activation='relu')(i)
x = ks.layers.Dense(2048, activation='relu')(x)
x = ks.layers.Dense(2048, activation='relu')(x)
x = ks.layers.Dense(9, activation='sigmoid', name='prediction_layer')(x)
model = ks.Model(i, x)

weights_file = "/usr/classification.hdf5"

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




def convert(text):
    return [[0 for _ in range(dimension)]]


def classify(book_id):
    book_contents = BookContent.object.filter(book__id=book_id)
    text = " ".join([bc.content for bc in book_contents])

    result = model.predict(convert(text))[0]
    category = class_mapping[np.argmax(result)]

    book = Book.object.get(pk=book_id)
    before = book.categories
    for cat in before:
        book.categories.remove(cat)

    c = Category.objects.get(name=category)
    book.categories.add(c)
    book.save()


