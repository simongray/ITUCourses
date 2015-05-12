__author__ = 'Anders'

from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from loading import loader

import numpy as np
import matplotlib.pyplot as plot


data, target = loader.numerical_evaluation_data(eval_data=False)
with_eval, throw_away = loader.numerical_evaluation_data(eval_data=True)

k_means = KMeans(n_clusters=10)
k_means.fit(data)

centers = k_means.cluster_centers_
labels = k_means.labels_

clusters = [[], [], [], [], [], [], [], [], [], []]
i = 0
for label in labels:
    clusters[label].append(data[i])
    i += 1

fig = plot.figure()
ax = fig.add_subplot(111, projection='3d')

colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k', 'w', (.92, 0.74, 0.63), (0.86, 0.182, 0.234)]

for entity in with_eval:
    cluster = k_means.predict(entity[1:])
    ax.scatter(entity[2], entity[4], entity[0], c=colors[cluster])

plot.show()
