from keras.models import load_model
import cv2
import numpy as np
import matplotlib.pyplot as plt


model = load_model('nail_unet.h5')

im = cv2.imread('test.png')
im = cv2.resize(im, (224, 224), interpolation = cv2.INTER_CUBIC)

pred = model.predict(np.reshape(im,(1,224,224,3)))

ret,middle = cv2.threshold(np.reshape(pred[0,:,:,1],(224,224)),0.7,1.0,cv2.THRESH_BINARY)
ret,front = cv2.threshold(np.reshape(pred[0,:,:,2],(224,224)),0.7,1.0,cv2.THRESH_BINARY)
ret,back = cv2.threshold(np.reshape(pred[0,:,:,3],(224,224)),0.7,1.0,cv2.THRESH_BINARY)

middle = np.uint8(middle*255.0)
front = np.uint8(front*255.0)
back = np.uint8(back*255.0)

def getAverageColor(image,mask):

    kernel = np.ones((5,5), np.uint8) 

    m = cv2.erode(mask, kernel, iterations=1) 

    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(m, connectivity=8)
    sizes = stats[:, -1]

    max_label = -1
    max_size = 0
    for i in range(0, nb_components):
        if sizes[i] > max_size and np.mean(m[output == i]) > 100.0:
            max_label = i
            max_size = sizes[i]

    return (np.mean(image[output == max_label,2]),np.mean(image[output == max_label,1]),np.mean(image[output == max_label,0]))

def rgb2hue(colour):
    r, g, b = colour[0]/255.0, colour[1]/255.0, colour[2]/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h

midC = rgb2hue(getAverageColor(im,middle))
froC = rgb2hue(getAverageColor(im,front))
bacC = rgb2hue(getAverageColor(im,back))

yellowScore = (3*np.tanh(np.abs(froC-60.0)/10.0))

midScore = (2-2*np.tanh(np.abs(midC-16)/10.0))
bacScore = (2-2*np.tanh(np.abs(bacC-14)/10.0))

