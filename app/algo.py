import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

# Define the training data

def predict_KNN(x_t, y_t, x_te):
	# Convert training data to numpy array
	x_train = np.array(x_t)
	y_train = np.array(y_t)

	# Scale the training data
	scaler = StandardScaler()
	x_train_scaled = scaler.fit_transform(x_train)


	# Scale the test data
	x_test_scaled = scaler.transform(x_te)

	# Create a KNN classifier with k = 3
	knn = KNeighborsClassifier(n_neighbors=3)

	# Train the classifier on the scaled training set
	knn.fit(x_train_scaled, y_train)

	# Find the three nearest neighbors to the test sample
	distances, indices = knn.kneighbors(x_test_scaled)

	# Get the corresponding plant names of the nearest neighbors
	nearest_neighbors = y_train[indices.flatten()]

	# print("Closest plants:", nearest_neighbors)
	return nearest_neighbors