import cv2
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt


globalIndex = 0

files = [f for f in listdir('./nails/') if isfile(join('./nails/', f))]
for f in files:
    im = cv2.imread(join('./nails/',f))
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret,masks = cv2.threshold(im_gray,254,255,cv2.THRESH_BINARY_INV)


    ret,labels = cv2.connectedComponents(masks)

    for label in range(np.max(labels) + 1):
        labelMat = np.where(labels==label)
        xmin = np.min(labelMat[0])
        ymin = np.min(labelMat[1])
        xmax = np.max(labelMat[0])
        ymax = np.max(labelMat[1])
        if xmin!=0:
            croppedIm = im[xmin:xmax,ymin:ymax,:]
            cv2.imwrite("./nails_out/nail-" + str(globalIndex) + ".png", croppedIm)
            globalIndex = globalIndex + 1
        # plt.axis("off")
        # plt.imshow(cv2.cvtColor(croppedIm, cv2.COLOR_BGR2RGB))
        # plt.show()