#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in
# https://www.kaggle.com/eashish/bidirectional-lstm-with-convolution
import numpy as np
import pandas as pd

from keras.layers import Dense, Input, Bidirectional, Conv1D, GRU, Embedding, GlobalAveragePooling1D, GlobalMaxPooling1D, concatenate, SpatialDropout1D
from keras.preprocessing import text, sequence
from keras.models import Model
from keras.optimizers import Adam

data_path = './data/'

EMBEDDING_FILE = data_path + 'glove.840B.300d.txt'

train = pd.read_csv(data_path + 'train.csv')
test = pd.read_csv(data_path + 'test.csv')

x_train = train["content"].fillna("fillna")
x_test = test["content"].fillna("fillna")

x_train = x_train.str.lower()
x_test = x_test.str.lower()

y_train = train[["deleted"]].values

max_features = 100000
maxlen = 150
embed_size = 300

tok = text.Tokenizer(num_words=max_features, lower=True)

tok.fit_on_texts(list(x_train) + list(x_test))

x_train = tok.texts_to_sequences(x_train)
x_test = tok.texts_to_sequences(x_test)

x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = sequence.pad_sequences(x_test, maxlen=maxlen)

embeddings_index = {}
with open(EMBEDDING_FILE, encoding='utf8') as f:
    for line in f:
        values = line.rstrip().rsplit(' ')
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs

word_index = tok.word_index

# prepare embedding matrix
num_words = min(max_features, len(word_index) + 1)
embedding_matrix = np.zeros((num_words, embed_size))

for word, i in word_index.items():
    if i >= max_features:
        continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector

sequence_input = Input(shape=(maxlen,))

x = Embedding(max_features, embed_size, weights=[embedding_matrix], trainable=False)(sequence_input)

x = SpatialDropout1D(0.2)(x)
x = Bidirectional(GRU(128, return_sequences=True, dropout=0.3, recurrent_dropout=0.3))(x)
x = Conv1D(64, kernel_size=3, padding="valid", kernel_initializer="glorot_uniform")(x)

avg_pool = GlobalAveragePooling1D()(x)
max_pool = GlobalMaxPooling1D()(x)
x = concatenate([avg_pool, max_pool])

prediction = Dense(1, activation="sigmoid")(x)
model = Model(sequence_input, prediction)
model.compile(loss='binary_crossentropy', optimizer=Adam(lr=1e-3), metrics=['accuracy'])

batch_size = 32
epochs = 5

bst_model_path = 'model1.h5'
history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1)
y_pred = model.predict(x_test, verbose=1, batch_size=512)

model.save_weights(bst_model_path)

print(y_pred.shape)

data = pd.DataFrame(data=y_pred)

data.to_csv(data_path + "predictions.csv", index=False)
