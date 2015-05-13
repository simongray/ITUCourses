__author__ = 'Anders'

from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import SpectralClustering
from sklearn.cluster import Birch

from mpl_toolkits.mplot3d import Axes3D
from loading import loader

import numpy as np
import matplotlib.pyplot as plot


def course_data_clustering_plot():
    data, target = loader.numerical_course_data(eval_data=False)
    with_eval, throw_away = loader.numerical_course_data(eval_data=True)

    training = data[:-299]
    test_with_eval = with_eval[-300:]

    k_means = KMeans(n_clusters=5)
    k_means.fit(training)

    # centers = k_means.cluster_centers_
    # labels = k_means.labels_

    # clusters = [[], [], [], [], [], [], [], [], [], []]
    # i = 0
    # for label in labels:
    #     clusters[label].append(data[i])
    #     i += 1

    a = plot.figure().add_subplot(111, projection='3d')
    b = plot.figure().add_subplot(111, projection='3d')
    c = plot.figure().add_subplot(111, projection='3d')
    d = plot.figure().add_subplot(111, projection='3d')
    e = plot.figure().add_subplot(111, projection='3d')
    f = plot.figure().add_subplot(111, projection='3d')
    g = plot.figure().add_subplot(111, projection='3d')

    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k', 'w', (.92, 0.74, 0.63), (0.86, 0.182, 0.234)]

    for entry in test_with_eval:
        cluster = k_means.predict(entry[1:])  # <-        ->
        a.scatter(entry[6], entry[1], entry[0], c=colors[cluster])  # Studies   ECTS
        b.scatter(entry[2], entry[3], entry[0], c=colors[cluster])  # Exp.      Min.
        c.scatter(entry[5], entry[6], entry[0], c=colors[cluster])  # Lang.     Studies
        d.scatter(entry[4], entry[6], entry[0], c=colors[cluster])  # Time      Studies
        e.scatter(entry[2], entry[6], entry[0], c=colors[cluster])  # Exp.      Studies
        f.scatter(entry[3], entry[6], entry[0], c=colors[cluster])  # Min.      Studies
        g.scatter(entry[6], entry[7], entry[0], c=colors[cluster])  # Studies   Semester

    plot.show()


def print_cluster(cluster):
    print("\n CLUSTER \n")
    for entity in cluster:
        print(str(entity[1]) + "	" + str(entity[2]) + "	" + str(entity[0]))


def evaluation_data_clustering_plot():
    data = loader.numerical_evaluation_data(eval_data=True)

    training = data[:-300]
    test = data[-299:]

    # birch = Birch()
    # birch.fit(data)

    # spectral = SpectralClustering(n_clusters=3)
    # spectral.fit(data)

    # db_scan = DBSCAN(min_samples=30)
    # db_scan.fit(data)

    k_means = KMeans(n_clusters=5)
    k_means.fit(data)

    labels = k_means.labels_
    # labels = db_scan.labels_
    # labels = spectral.labels_
    # labels = birch.labels_

    clusters = [[], [], [], [], [], [], [], [], [], []]
    i = 0
    for label in labels:
        clusters[label].append(data[i])
        i += 1

    # for cluster in clusters:
    #     print_cluster(cluster)

    a = plot.figure().add_subplot(111, projection='3d')

    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k', 'w', (.92, 0.74, 0.63), (0.86, 0.182, 0.234)]

    color = 0
    # for entry in test:
    #     label = k_means.predict(entry)
    #     a.scatter(entry[1], entry[2], entry[0], c=colors[label])

    for cluster in clusters:
        for point in cluster:
            a.scatter(point[1], point[2], point[0], c=colors[color])
        color += 1

    a.set_xlabel('Time Evaluation')
    a.set_ylabel('Job Evaluation')
    a.set_zlabel('Overall Evaluation')
    plot.show()


if __name__ == '__main__':
    evaluation_data_clustering_plot()