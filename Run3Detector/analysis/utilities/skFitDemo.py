#this file is used to demonstrate how SK linear fit work

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.linear_model import LinearRegression

# Load the diabetes dataset
X, y = datasets.load_diabetes(return_X_y=True)
print(f"X inital {X}")
print(f"X size {X.shape}")
print(f"Y inital {y}")
print(f"Y size {y.shape}")
n_samples = 20

# Use only one feature and sort
X = X[:, np.newaxis, 2][:n_samples]

y = y[:n_samples]

p = X.argsort(axis=0)
X = X[p].reshape((n_samples, 1))
y = y[p]

print(X)
print(y)
# Create equal weights and then augment the last 2 ones
sample_weight = np.ones(n_samples) * 20
sample_weight[-2:] *= 30

plt.scatter(X, y, s=sample_weight, c='grey', edgecolor='black')

# The unweighted model
regr = LinearRegression()
regr.fit(X, y)
plt.plot(X, regr.predict(X), color='blue', linewidth=3, label='Unweighted model')

# The weighted model
regr = LinearRegression()
regr.fit(X, y, sample_weight)
plt.plot(X, regr.predict(X), color='red', linewidth=3, label='Weighted model')

# The weighted model - scaled weights
regr = LinearRegression()
sample_weight = sample_weight / sample_weight.max()
regr.fit(X, y, sample_weight)
plt.plot(X, regr.predict(X), color='yellow', linewidth=2, label='Weighted model - scaled', linestyle='dashed')
plt.xticks(());plt.yticks(());plt.legend();

plt.show()