# -*- coding: utf-8 -*-
"""Code.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HO5gg5LeS8TKisYplbxx0Cyh3lwsZQvq
"""

import numpy as np
from sklearn.linear_model import LogisticRegression

# Define your feature transformation function using Kronecker product with adjustable dimensions
def my_map(c):
    D = 1
    u = c.copy()
    v = np.ones(c.shape[0])

    for i in range(c.shape[0]):
        D *= 2
        u = np.kron(u, c[i])
        v = np.kron(v, np.array([[1, -1]]))

    return u @ v

# Define your fitting function
def my_fit(X, y):
    model = LogisticRegression(solver='liblinear')  # Choose a suitable solver
    model.fit(X, y)
    return model

# Load training and test data (assumed you have loaded them)
data_train = np.loadtxt('train.dat')
data_test = np.loadtxt('test.dat')

# Separate features (X) and labels (Y) for training data
X_train = data_train[:, :-1]  # All columns except the last one
y_train = data_train[:, -1]   # Last column

# Separate features (X) and labels (Y) for test data
X_test = data_test[:, :-1]    # All columns except the last one
y_test = data_test[:, -1]     # Last column

# Specify the desired dimension for feature vector (adjust as needed)
dimension = 3  # For example

# Apply feature transformation
X_train_transformed = np.array([my_map(challenge) for challenge in X_train])
X_test_transformed = np.array([my_map(challenge) for challenge in X_test])

# Train the model
model = my_fit(X_train_transformed, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test_transformed)

# Evaluate model performance
accuracy = np.mean(y_pred == y_test)
print("Test accuracy:", accuracy)

import numpy as np
from sklearn.linear_model import LogisticRegression
from scipy.linalg import khatri_rao
import time as tm


def my_map(data):
        # This is a simple example that uses the Khatri-Rao product.
        # The input data is assumed to be a 2D array where each row is a sample and each column is a feature.
        # The Khatri-Rao product is applied to each pair of columns in the data.
        mapped_data = []
        for i in range(data.shape[1]):
            for j in range(i+1, data.shape[1]):
                kr_product = khatri_rao(data[:, i:i+1], data[:, j:j+1])
                mapped_data.append(kr_product)
        return np.hstack(mapped_data)

def my_fit(X, y):
        X_transformed = my_map(X)
        model.fit(X_transformed, y)

Z_trn = np.loadtxt( "train.dat" )
Z_tst = np.loadtxt( "test.dat" )

n_trials = 5

d_size = 0
t_train = 0
t_map = 0
acc = 0
for t in range( n_trials ):
	tic = tm.perf_counter()
	w, b = my_fit( Z_trn[:, :-1], Z_trn[:,-1] )
	toc = tm.perf_counter()
	t_train += toc - tic

	d_size += w.shape[0]

	tic = tm.perf_counter()
	feat = my_map( Z_tst[:, :-1] )
	toc = tm.perf_counter()
	t_map += toc - tic

	scores = feat.dot( w ) + b
	pred = np.zeroes_like( scores )
	pred[scores > 0] = 1
	acc += np.average( Z_tst[ :, -1 ] == pred )
d_size /= n_trials
t_train /= n_trials
t_map /= n_trials
acc /= n_trials

print( d_size, t_train, t_map, 1 - acc )

"""# New Section"""

