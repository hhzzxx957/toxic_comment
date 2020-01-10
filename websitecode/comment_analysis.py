
import numpy as np
import pandas as pd

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

from keras.models import model_from_json
from keras import backend

import pickle

def com_analysis(comment):
    # max_features = 20000
    maxlen = 100

    test=pd.DataFrame([comment])
    test.columns=['comment_text']
    list_sentences_test = test["comment_text"].fillna("_na_").values

    # loading
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    # test token
    list_tokenized_test = tokenizer.texts_to_sequences(list_sentences_test)
    X_te = pad_sequences(list_tokenized_test, maxlen=maxlen)

    # open json file
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")

    # predicting
    loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    y_test = loaded_model.predict([X_te], batch_size=1024, verbose=1)

    backend.clear_session()
    return y_test

# comment='This is a good game!!'
# output=com_analysis(comment)
# print(output)
