import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

dataset = ('/Users/sebastian/Desktop/EDM Hate Speech/output_utf8_small.csv')
data = pd.read_csv(dataset, sep=',', header=None)
data.columns = ["id", "content", "deleted"]
data.to_csv('/Users/sebastian/Desktop/EDM Hate Speech/' + "1000.csv", index=False)

X, y = data.iloc[:,:], data.iloc[:,:]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=34)

X_train.to_csv('/Users/sebastian/Desktop/EDM Hate Speech/' + "Train.csv", index=False)
X_test.to_csv('/Users/sebastian/Desktop/EDM Hate Speech/' + "Test.csv", index=False)

