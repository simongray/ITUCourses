__author__ = 'Anders'

from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from loading import loader

import matplotlib.pyplot as plot


data, target = loader.numerical_evaluation_data()

k_means = KMeans(n_clusters=8)
k_means.fit(data)

centers = k_means.cluster_centers_
labels = k_means.labels_


clusters = [[], [], [], [], [], [], [], []]
i = 0
for label in labels:
    clusters[label].append(data[i])
    i += 1


# fig = plot.figure()
# ax = fig.add_subplot(111, projection='2d')

colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k', 'w']
color = 0
for cluster in clusters:
    for item in cluster:
        plot.scatter(item[0], item[2], c=colors[color])
    color += 1


plot.show()
