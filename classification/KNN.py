from sklearn.neighbors import KNeighborsClassifier

from loading import loader


data, target = loader.all_evaluation_data()
training = loader.training_data()
test = loader.test_data()

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(training, target[:-100])

for course in test:
    print(str(knn.predict(course)))
