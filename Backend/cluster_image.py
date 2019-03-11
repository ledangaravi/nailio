from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import cv2
import numpy as np

image = cv2.imread('test.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.figure()
plt.axis("off")
plt.imshow(image)

width = image.shape[0]
height = image.shape[1]

image = image.reshape((image.shape[0] * image.shape[1], 3))

clt = KMeans(n_clusters = 5)
clt.fit(image)

colors = np.reshape(clt.labels_,(width,height))

plt.figure()
plt.axis("off")
plt.imshow(colors)
plt.show()