import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

#https://www.datahubbs.com/deep-learning-101-building-a-neural-network-from-the-ground-up/

np.random.seed(0)
X, Y = make_moons(500, noise=0.1)

# Split into test and training data
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.25, random_state=73)

# Plot results
plt.figure(figsize=(12,8))
plt.scatter(X_train[:,0], X_train[:,1], c=Y_train, 
            cmap=plt.cm.cividis, s=50)
plt.xlabel('X1')
plt.ylabel('X2')
plt.title('Random Training Data')
plt.show()