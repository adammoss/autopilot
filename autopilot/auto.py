"""
.. module:: autopilot
   :synopsis: Main routine for autopilot package
.. moduleauthor:: Adam Moss <adam.moss@nottingham.ac.uk>
"""

import threading
import importlib
from autopilot.settings import api_settings
import collections
import cv2
import time
import logging


class AutoPilot:

    def __init__(self, capture=None, front_wheels=None, back_wheels=None, camera_control=None,
                 debug=False, mode='drive', model=None, width=320, height=240, capture_src="/dev/video0", max_speed=35):
        """

        :param capture:
        :param front_wheels:
        :param back_wheels:
        :param camera_control:
        :param debug:
        :param mode:
        :param model:
        :param width:
        :param height:
        :param capture_src:
        """

        try:
            from art import text2art
            print(text2art("MLiS AutoPilot"))
        except ModuleNotFoundError:
            print('MLiS AutoPilot')

        assert mode in ['test', 'camera', 'drive', 'ludicrous', 'plaid']

        # Try getting camera from already running capture object, otherwise get a new CV2 video capture object
        if mode != 'test':
            if capture is not None and hasattr(capture, 'camera'):
                self.camera = capture.camera
            else:
                self.camera = cv2.VideoCapture(capture_src)
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                if not self.camera.isOpened():
                    raise ValueError("Failed to open the camera")
        else:
            self.camera = None

        # These are picar controls
        self.front_wheels = front_wheels
        self.back_wheels = back_wheels
        self.camera_control = camera_control

        self.max_speed = max_speed

        self.debug = debug
        self.mode = mode

        # Thread variables
        self._started = False
        self._terminate = False
        self._drive_thread = None
        self._frame_thread = None

        # Latest frame
        self.current_frame = collections.deque(maxlen=1)

        # Logging
        self.inference_times = collections.deque(maxlen=10)

        logging.basicConfig(filename="autopilot.log", level=logging.INFO)

        # Load the model
        self.load_model(model)

    def load_model(self, model):
        # NN Model
        if model is None:
            model = api_settings.MODEL
        print('Using %s model' % model)
        logging.info('Using %s model' % model)
        module = importlib.import_module('autopilot.models.%s.model' % model)
        self.model = module.Model()
        logging.info('Loaded model')

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
        self._frame_thread = threading.Thread(target=self._update_frame, args=())
        self._frame_thread.start()
        self._drive_thread = threading.Thread(target=self._drive, args=())
        self._drive_thread.start()

    def stop(self):
        """
        Stops autopilot
        :return:
        """
        self._started = False
        self._terminate = True
        if self._frame_thread is not None:
            self._frame_thread.join()
        if self._drive_thread is not None:
            self._drive_thread.join()
        if self.back_wheels is not None:
            self.back_wheels.speed = 0
        # Release the video device
        if self.camera is not None:
            self.camera.release()

    def _update_frame(self):
        """
        Separate thread to continually update latest frame
        :return:
        """
        if self.mode == 'test':
            while not self._terminate:
                frame = cv2.imread(api_settings.TEST_IMAGE)
                self.current_frame.append(frame)
        else:
            while not self._terminate:
                ret, frame = self.camera.read()
                # Do not try to perform inference on a value of None
                if not ret:
                    # self.stop()
                    # raise ValueError("Failed to fetch the frame")
                    print("Failed to fetch the next frame.")
                    continue
                self.current_frame.append(frame)

    def _drive(self):
        """
        Drive routine for autopilot. Processes frame from camera
        :return:
        """
        while not self._terminate:

            if len(self.current_frame) > 0:

                frame = self.current_frame.pop()
                start_time = time.time()
                angle, speed = self.model.predict(frame)
                inference_time = 1000 * (time.time() - start_time)
                self.inference_times.append(inference_time)

                angle = int(angle)
                speed = max(min(int(speed), self.max_speed), 0)

                if self.debug:
                    if len(self.inference_times) > 0:
                        mean_inference_time = sum(self.inference_times) / len(self.inference_times)
                    else:
                        mean_inference_time = inference_time
                    print('Inference time {0:0.2f} ms, mean {1:0.2f} ms'.format(inference_time, mean_inference_time))
                    print('Angle: {0}, Speed: {1}'.format(angle, speed))

                if self.mode == 'test':

                    assert 70 <= angle <= 110, "The angle is not realistic for the test image"
                    assert 20 <= speed <= 35, "The speed is not realistic for the test image"

                elif self.mode in ['drive', 'ludicrous', 'plaid']:

                    # Do not allow angle or speed to go out of allowed range
                    angle = max(min(angle, self.front_wheels._max_angle), self.front_wheels._min_angle)
                    if self.mode == 'ludicrous':
                        speed = 50
                    elif self.mode == 'plaid':
                        speed = 100

                    # Set picar angle and speed
                    self.front_wheels.turn(angle)
                    if speed > 0:
                        self.back_wheels.forward()
                        self.back_wheels.speed = speed
                    else:
                        self.back_wheels.backward()
                        self.back_wheels.speed = abs(speed)
