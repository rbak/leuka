import os
import yaml


def load(file):
    stream = open(file, 'r')
    return yaml.load(stream)


def walk(path):
    env = {}
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            if file[0] != '.':
                env[os.path.splitext(file)[0]] = load(file_path)
        else:
            env[file] = walk(file_path)
    return env
