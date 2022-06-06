import numpy as np
import tensorflow as tf
import os
import time

class Model:
    os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices' #enable gpu
    my_model = 'converted_model.tflite'

    def __init__(self):
        try: #load edge TPU model
            delegate = tf.lite.experimental.load_delegate('libedgetpu.so.1') #'libedgetpu.1.dylib' for mac or 'libedgetpu.so.1' for linux
            print('Using TPU')
            self.interpreter = tf.lite.Interpreter(model_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                             self.my_model),experimental_delegates=[delegate])
                                                                             
        except ValueError:
            print('Fallback to CPU')
            self.interpreter = tf.lite.Interpreter(model_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                             self.my_model))
        self.interpreter.allocate_tensors()
        
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
    def preprocess(self, image):
        #im = tf.image.convert_image_dtype(image, tf.float32)
        im = tf.image.resize(image, (120,160))
        im = tf.divide(im, 255)  # Normalize, need to check if needed
        im = tf.expand_dims(im, axis=0) #add batch dimension
        return im

    def predict(self, image):
        image = self.preprocess(image)

        self.interpreter.set_tensor(self.input_details[0]['index'], image) #original might work
        self.interpreter.invoke()

        pred_speed = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        pred_angle = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        speed = np.around(pred_speed[0]).astype(int)*35
        angle = pred_angle[0]*80+50
        
        return angle, speed
