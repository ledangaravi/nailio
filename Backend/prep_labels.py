import cv2
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

files = [f for f in listdir('./unet_train/') if isfile(join('./unet_train/', f))]
for f in files:
    label = cv2.imread(join('./unet_label/',f.replace('.png','_mask.png')))
    image = cv2.cvtColor(label, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224), interpolation = cv2.INTER_CUBIC)


    width = image.shape[0]
    height = image.shape[1]

    image = image.reshape((image.shape[0] * image.shape[1], 3))

    clt = KMeans(n_clusters = 4)
    clt.fit(image)

    colors = np.reshape(clt.labels_,(width,height))
    labels = np.zeros((224,224,4))
    labels[colors == 0,0] = 1
    labels[colors == 1,1] = 1
    labels[colors == 2,2] = 1
    labels[colors == 3,3] = 1

    plt.figure()
    plt.axis("off")
    plt.subplot(221)
    plt.imshow(np.reshape(labels[:,:,0],(224,224)))
    plt.axis("off")
    plt.subplot(222)
    plt.imshow(np.reshape(labels[:,:,1],(224,224)))
    plt.axis("off")
    plt.subplot(223)
    plt.imshow(np.reshape(labels[:,:,2],(224,224)))
    plt.axis("off")
    plt.subplot(224)
    plt.imshow(np.reshape(labels[:,:,3],(224,224)))
    plt.show()

    text = input("labels: ")

    labels[colors == 0,0] = int(text[0])
    labels[colors == 1,1] = int(text[1])
    labels[colors == 2,2] = int(text[2])
    labels[colors == 3,3] = int(text[3])

    cv2.imwrite(f.replace('.png','_mask_0.png'),np.reshape(labels[:,:,0],(224,224)))
    cv2.imwrite(f.replace('.png','_mask_1.png'),np.reshape(labels[:,:,1],(224,224)))
    cv2.imwrite(f.replace('.png','_mask_2.png'),np.reshape(labels[:,:,2],(224,224)))
    cv2.imwrite(f.replace('.png','_mask_3.png'),np.reshape(labels[:,:,3],(224,224)))