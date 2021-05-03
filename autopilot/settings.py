import os
import json


DEFAULTS = {
    'MODEL': 'base',
    'TEST_IMAGE': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test.png')
}


class APISettings:

    def __init__(self, defaults=None):
        self.defaults = defaults or DEFAULTS
        if os.path.isfile('/home/pi/autopilot.json'):
            with open('/home/pi/autopilot.json', 'r') as f:
                self.user_settings = json.load(f)
        else:
            self.user_settings = {}

    def __getattr__(self, attr):
        if attr in self.__dict__['user_settings']:
            val = self.__dict__['user_settings'][attr]
        elif attr in self.__dict__['defaults']:
            val = self.__dict__['defaults'][attr]
        else:
            raise AttributeError("Invalid API setting: '%s'" % attr)
        return val


api_settings = APISettings(DEFAULTS)
