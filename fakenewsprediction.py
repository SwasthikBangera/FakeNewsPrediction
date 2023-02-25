# -*- coding: utf-8 -*-
"""FakeNewsPrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mN2rgU9seJykRO1QFNgrl0q8wySeDRy2

Import the dependencies
"""

import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import nltk
nltk.download('stopwords')

print(stopwords.words('english'))

"""Data Pre-processing"""

#Loading dataset to pandas dataframe
news_dataset = pd.read_csv('/content/train.csv')

news_dataset.shape

# Studying the dataset
news_dataset.head()

# Counting Missing Values in dataset
news_dataset.isnull().sum()

# Replace Null values with empty string
news_dataset = news_dataset.fillna('')

news_dataset.isnull().sum()

# Merging Authorname and News Title
news_dataset['content'] = news_dataset['author']+' '+news_dataset['title']

news_dataset['content'].head()

# Seperating the data and label
X = news_dataset.drop(columns='label', axis=1)
Y = news_dataset['label']

print(X)
print(Y)

"""Stemming: to reduce a word to its root word

worker, worked, working -> Work
"""

port_stem = PorterStemmer()

def stemming(text):
  stemmed_text = re.sub('[^a-zA-Z]',' ',text)
  stemmed_text = stemmed_text.lower()
  stemmed_text = stemmed_text.split()
  stemmed_text = [port_stem.stem(word) for word in stemmed_text if not word in stopwords.words('english')]
  stemmed_text = ' '.join(stemmed_text)
  return stemmed_text

news_dataset['content'] = news_dataset['content'].apply(stemming)

print(news_dataset['content'].head())

from hashlib import new
# Seperating data and labels
X = news_dataset['content'].values
Y = news_dataset['label'].values

print(X)

print(Y.shape)

# Converting the textual data to numerical data
vectorizer = TfidfVectorizer()
vectorizer.fit(X)

X = vectorizer.transform(X)

print(X)

"""Split dataset to Training and Test data"""

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

"""Training the model"""

model = LogisticRegression()

model.fit(X_train,Y_train)

"""Evaluating the metrics"""

# Accuracy of Training data
X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)

print('The accuracy of training dataset is ', training_data_accuracy)

# Accuracy of Test data
X_test_prediction = model.predict(X_test)
test_data_accuracy = accuracy_score(X_test_prediction, Y_test)

print('The accuracy of test dataset is ', test_data_accuracy)

"""Building a predictive function"""

X_new = X_test[0]

prediction = model.predict(X_new)
print(prediction)

if (prediction[0]==0):
  print('The news is real')
else:
  print('The news is fake')

