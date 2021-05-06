from tensorflow import keras
import numpy as np
import tensorflow as tf
import os

class Model:
    def __init__(self):
        self.speed_model = tf.keras.models.load_model('autopilot/models/maggie/speed_model/')
        self.angle_model = tf.keras.models.load_model('autopilot/models/maggie/angle_model/')

    def preprocess(self, image):
        im = tf.image.convert_image_dtype(image, tf.float32)
        im = tf.image.resize(im, [100, 100])
        im = tf.expand_dims(im, axis=0)
        return im

    def predict(self, image):
        angles = np.arange(17)*5+50
        image = self.preprocess(image)
        
        pred_speed = self.speed_model.predict(image)[0]
        speed = pred_speed[0].astype(int)*35
        pred_angle = self.angle_model.predict(image)[0]
        angle = angles[np.argmax(pred_angle)]
        
        return angle, speed
