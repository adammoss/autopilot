"""
.. module:: autopilot
   :synopsis: Main routine for autopilot package
.. moduleauthor:: Adam Moss <adam.moss@nottingham.ac.uk>
"""

import threading
import importlib
from autopilot.settings import api_settings

import cv2
import time


class AutoPilot:

    def __init__(self, capture=None, front_wheels=None, back_wheels=None, camera_control=None,
                 debug=False, mode='drive', model=None):
        """

        :param capture:
        :param front_wheels:
        :param back_wheels:
        :param camera_control:
        :param debug:
        :param mode:
        :param model:
        """

        try:
            from art import text2art
            print(text2art("MLiS AutoPilot"))
        except ModuleNotFoundError:
            print('MLiS AutoPilot')

        assert mode in ['test', 'camera', 'drive']

        # Try getting camera from already running capture object, otherwise get a new CV2 video capture object
        if mode != 'test':
            try:
                self.camera = capture.camera
            except:
                self.camera = cv2.VideoCapture(0)

        # These are picar controls
        self.front_wheels = front_wheels
        self.back_wheels = back_wheels
        self.camera_control = camera_control

        self.debug = debug
        self.mode = mode

        # Thread variables
        self._started = False
        self._terminate = False
        self._thread = None

        # NN Model
        if model is None:
            model = api_settings.MODEL
        print('Using %s model' % model)
        try:
            module = importlib.import_module('autopilot.models.%s.model' % model)
            self.model = module.Model()
        except:
            raise ValueError('Could not import model')

    def start(self):
        """
        Starts autopilot in separate thread
        :return:
        """
        if self._started:
            print('[!] Self driving has already been started')
            return None
        self._started = True
        self._terminate = False
        self._thread = threading.Thread(target=self._drive, args=())
        self._thread.start()

    def stop(self):
        """
        Stops autopilot
        :return:
        """
        self._started = False
        self._terminate = True
        if self._thread is not None:
            self._thread.join()

    def _drive(self):
        """
        Drive routine for autopilot. Processes frame from camera
        :return:
        """
        while not self._terminate:

            if self.mode == 'test':
                frame = cv2.imread(api_settings.TEST_IMAGE)
            else:
                ret, frame = self.camera.read()

            if frame is not None:

                start_time = time.time()
                angle, speed = self.model.predict(frame)

                angle = int(angle)
                speed = int(speed)

                if self.debug:
                    print('Inference time {0:0.2f} ms'.format(1000 * (time.time() - start_time)))
                    print('Angle: {0}, Speed: {1}'.format(angle, speed))

                if self.mode == 'test':

                    assert 70 <= angle <= 110, "The angle is not realistic for the test image"
                    assert 20 <= speed <= 35, "The speed is not realistic for the test image"

                elif self.model == 'drive':

                    # Do not allow angle or speed to go out of range
                    angle = max(min(angle, self.front_wheels._max_angle), self.front_wheels._min_angle)
                    speed = max(min(speed, 35), 0)

                    # Set picar angle and speed
                    self.front_wheels.turn(angle)
                    if speed > 0:
                        self.back_wheels.forward()
                        self.back_wheels.speed = speed
                    else:
                        self.back_wheels.backward()
                        self.back_wheels.speed = abs(speed)

            elif self.debug:
                print('Cannot get image')

            if self.mode == 'camera':
                self.back_wheels.speed = 0
