from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Generate some example data
X_train = [[22, 23, 24, 25, 26, 2, 1, 0],
          [23, 24, 25, 26, 27, 2, 1, 0],
          [21, 24, 26, 28, 30, 3, 1, 0],
          [24, 25, 26, 27, 28, 1, 1, 1],
          [23, 24, 25, 26, 27, 1, 1, 1],
          [24, 25, 26, 27, 28, 5, 1, 1],
          [29, 30, 31, 32, 33, 3, 1, 1],
          [28, 29, 30, 31, 32, 2, 1, 1],
          [18, 19, 20, 21, 22, 4, 1, 1],
          [14, 15, 16, 17, 18, 3, 0, 1], 
          [30, 31, 32, 33, 34, 1, 1, 1],
          [20, 21, 22, 23, 24, 4, 0, 1],
          [18, 19, 20, 21, 22, 4, 0, 1],
          [19, 20, 21, 22, 23, 4, 0, 1],
          [23, 24, 25, 26, 27, 1, 1, 0],
          [22, 23, 24, 25, 26, 2, 1, 0],
          [25, 26, 27, 28, 29, 2, 1, 0],
          [17, 18, 19, 20, 21, 1, 0, 1],
          [16, 17, 18, 19, 20, 1, 0, 1],
          [25, 26, 27, 28, 29, 1, 0, 1],]
y_train = ["okra",
            "patola",
            "talong",
            "upo",
            "luya",
            "ampalaya",
            "kamatis",
            "sitaw",
            "pechay",
            "labanos",
            "repolyo",
            "mustasa",
            "spinach",
            "kalabasa",
            "mais",
            "pinya",
            "kamote",
            "sibuyas",
            "bawang",
            "patatas",]
X_test = [[28, 29, 27, 27, 28, 3, 0, 1]]
# y_test = ['hot', 'cold', 'hot']

# Normalize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create and fit the model
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)



# Find the three closest neighbors to the test instance
distances, indices = model.kneighbors(X_test)

# Print the three closest neighbors and their distances
for i in range(3):
    print('Neighbor', i+1, 'distance:', distances[0][i], 'class:', y_train[indices[0][i]])


# Predict the labels of the test data
# y_pred = model.predict(X_test)
# print(y_pred)

# Calculate the accuracy of the model on the test data
# accuracy = accuracy_score(y_test, y_pred)
# print("Accuracy:", accuracy)  # Output: Accuracy: 0.6666666666666666
