import loader

defaults = {}


class Config(object):
    def __init__(self, config_file):
        self.config = loader.load('../config.yaml')

    def get(self, category, key):
        if category in self.config and key in self.config[category]:
            return self.config[category][key]
        elif key in defaults[category]:
            return defaults[category][key]
        else:
            return None

    def get_args(self):
        return self.config['Args']
