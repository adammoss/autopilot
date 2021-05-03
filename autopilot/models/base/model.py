from tensorflow import keras
import numpy as np
import imutils
import cv2
import os


class Model:

    saved_model = 'autopilot.h5'

    def __init__(self):
        self.model = keras.models.load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.saved_model))
        self.model.summary()

    def preprocess(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV) / 255.0
        image = imutils.resize(image, width=80)
        image = image[int(image.shape[0] / 4):, :, :]
        return image

    def predict(self, image):
        image = self.preprocess(image)
        angle, speed = self.model.predict(np.array([image]))[0]
        # Training data was normalised so convert back to car units
        angle = 80 * np.clip(angle, 0, 1) + 50
        speed = 35 * np.clip(speed, 0, 1)
        return angle, speed
