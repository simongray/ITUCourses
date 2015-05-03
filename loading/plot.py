import numpy as np

from matplotlib import pyplot
from sklearn import cluster
from loading import loader

data, target = loader.all_evaluation_data()

k = 3
k_means = cluster.KMeans(n_clusters=k)
k_means.fit(data)

labels = k_means.labels_
centroids = k_means.cluster_centers_

first_attribute = 1
second_attribute = 10

index = 0

for i in range(0, len(data)):
    dot = ''

    if i == 0:
        dot = 'bo'
    elif i == 1:
        dot = 'go'
    else:
        dot = 'ro'

    # plot the data observations
    pyplot.plot(data[:, first_attribute],
                data[:, second_attribute],
                dot)
    # plot the centroids
    # lines = pyplot.plot(centroids[i, 0], centroids[i, 1], 'kx')
    # make the centroid x's bigger
    # pyplot.setp(lines, ms=5.0)
    # pyplot.setp(lines, mew=2.0)

# set labels
pyplot.xlabel(loader.get_labels()[first_attribute])
pyplot.ylabel(loader.get_labels()[second_attribute])

# set axis scale
pyplot.autoscale(enable=True)

pyplot.show()