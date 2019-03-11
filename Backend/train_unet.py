from segmentation_models import Unet
from segmentation_models.backbones import get_preprocessing
from segmentation_models.losses import bce_jaccard_loss
from segmentation_models.metrics import iou_score
from tensorflow.keras import optimizers

import cv2
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

BACKBONE = 'resnet34'
preprocess_input = get_preprocessing(BACKBONE)


x_train = []
y_train = []

files = [f for f in listdir('./unet_train/') if isfile(join('./unet_train/', f))]
for f in files:
    im = cv2.imread(join('./unet_train/',f))
    im[:, :, 0] = cv2.equalizeHist(im[:, :, 0])
    im[:, :, 1] = cv2.equalizeHist(im[:, :, 1])
    im[:, :, 2] = cv2.equalizeHist(im[:, :, 2])
    im = cv2.resize(im, (224, 224), interpolation = cv2.INTER_CUBIC)

    x_train.append(im)
    label0 = cv2.imread(join('./unet_label/',f.replace('.png','_mask_0.png')))
    label0 = cv2.cvtColor(label0, cv2.COLOR_BGR2GRAY)
    label1 = cv2.imread(join('./unet_label/',f.replace('.png','_mask_1.png')))
    label1 = cv2.cvtColor(label1, cv2.COLOR_BGR2GRAY)
    label2 = cv2.imread(join('./unet_label/',f.replace('.png','_mask_2.png')))
    label2 = cv2.cvtColor(label2, cv2.COLOR_BGR2GRAY)
    label3 = cv2.imread(join('./unet_label/',f.replace('.png','_mask_3.png')))
    label3 = cv2.cvtColor(label3, cv2.COLOR_BGR2GRAY)

    labels = np.stack( [label0,label1,label2,label3], axis=2 )
    print(labels.shape)

    y_train.append(labels)


x_train = np.stack( x_train, axis=0 )
y_train = np.reshape(np.stack( y_train, axis=0 ),(15,224,224,4))

x_train = preprocess_input(x_train)

x_val = np.reshape(x_train[-2:,:,:,:],(2,224,224,3))
y_val = np.reshape(y_train[-2:,:,:,:],(2,224,224,4))

x_train = x_train[:-2,:,:,:]
y_train = y_train[:-2,:,:,:]

print(x_train.shape)
print(y_train.shape)

model = Unet(BACKBONE, input_shape=(224, 224, 3),classes=4,encoder_weights='imagenet')
adam = optimizers.Adam(lr=0.0005,
    beta_1=0.9,
    beta_2=0.999,
    epsilon=None,
    decay=1e-6,
    amsgrad=True
)
model.compile('Adam', loss=bce_jaccard_loss, metrics=[iou_score])

model.fit(
    x=x_train,
    y=y_train,
    batch_size=8,
    epochs=30,
    validation_data=(x_val, y_val)
)

model.save('nail_unet.h5',include_optimizer=False)