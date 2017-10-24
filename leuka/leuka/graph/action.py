import os
import sys


class Action(object):
    def __init__(self, name, config_dir):
        updater_path = os.path.join(config_dir, 'scripts')
        sys.path.append(updater_path)
        self.actionmod = __import__(name)
