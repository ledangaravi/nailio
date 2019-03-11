from http.server import BaseHTTPRequestHandler,HTTPServer
import base64
import cv2
from io import BytesIO
import numpy as np
import os
import sys
import tensorflow as tf
import glob
from PIL import Image
from tensorflow.python.saved_model import loader
import json
from keras.models import load_model


PORT_NUMBER = 6065


class nailIOServer(HTTPServer):

     def __init__(self,*args):
        HTTPServer.__init__(self,*args)
        path = '/home/udvardi_peter98/'

        self.unet_model = load_model('nail_unet.h5')

        frozen_graph_exists = glob.glob(os.path.join(path, "*.pb"))

        if (len(frozen_graph_exists) > 0):
            print('loading ' + frozen_graph_exists[0])
            self.graph = tf.get_default_graph()
            self.sess = tf.Session(graph=self.graph)
            loader.load(self.sess, ['train'],
                        os.path.join(path, ""))
            self.inputVar = self.graph.get_tensor_by_name("resnet152:0")
            self.outputVar = self.graph.get_tensor_by_name("prob:0")


class nailIOHandler(BaseHTTPRequestHandler):
	
    def _getAverageColor(self,image,mask):

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

    def _rgb2hue(self,colour):
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

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'Application/json')
        self.end_headers()

    def _readb64(self,base64_string):
        sbuf = BytesIO()
        sbuf.write(base64.b64decode(base64_string))
        pimg = Image.open(sbuf)
        return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    def do_POST(self):
        self._set_headers()
        print('Captured POST request')
        data_file = self.rfile.read(int(self.headers['Content-Length']))

        jsonData = json.loads(data_file.decode("utf-8"))

        im = self._readb64(jsonData['Image'])
        
        im = cv2.resize(im, (224, 224), interpolation = cv2.INTER_CUBIC)

        im2 = np.copy(im)

        im[:, :, 0] = cv2.equalizeHist(im[:, :, 0])
        im[:, :, 1] = cv2.equalizeHist(im[:, :, 1])
        im[:, :, 2] = cv2.equalizeHist(im[:, :, 2])

        im = im - np.mean(im)

        predictions = self.server.sess.run(self.server.outputVar,feed_dict={self.server.inputVar: np.reshape(im,(1,224,224,3))})[0]

        pred = self.server.unet_model.predict(np.reshape(im2,(1,224,224,3)))

        ret,middle = cv2.threshold(np.reshape(pred[0,:,:,1],(224,224)),0.7,1.0,cv2.THRESH_BINARY)
        ret,front = cv2.threshold(np.reshape(pred[0,:,:,2],(224,224)),0.7,1.0,cv2.THRESH_BINARY)
        ret,back = cv2.threshold(np.reshape(pred[0,:,:,3],(224,224)),0.7,1.0,cv2.THRESH_BINARY)

        middle = np.uint8(middle*255.0)
        front = np.uint8(front*255.0)
        back = np.uint8(back*255.0)

        midC = self._rgb2hue(self._getAverageColor(im2,middle))
        froC = self._rgb2hue(self._getAverageColor(im2,front))
        bacC = self._rgb2hue(self._getAverageColor(im2,back))

        yellowScore = (2*np.tanh(np.abs(froC-60.0)/10.0))

        midScore = (2-2*np.tanh(np.abs(midC-16)/10.0))
        bacScore = (2-2*np.tanh(np.abs(bacC-14)/10.0))

        nailioScore = yellowScore + midScore + bacScore
        
        if predictions[1] > 0.7:
            nailioScore = nailioScore + 4.0

        conditions = ['Onychomycosis','Normal','Nail dystrophy','Melanonychia','Onycholysis','Other']

        return_json = {'nailioscore' : str(int(np.round(nailioScore))),
                    'condition' : str(conditions[np.argmax(predictions)]),
                    'confidence' : str(np.amax(predictions))}

        self._set_headers()
        self.wfile.write(json.dumps(return_json).encode('utf-8'))

        return
        

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = nailIOServer(('', PORT_NUMBER), nailIOHandler)
	print('Started httpserver on port ' + str(PORT_NUMBER))
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print('^C received, shutting down the web server')
	server.socket.close()