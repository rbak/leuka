from graphBuilder import GraphBuilder
import manager.loader as loader
from updater import Updater
from graphUpdater import GraphUpdater
import threading
import os


class FactoryManager(object):
    def __init__(self, config):
        self.config = config

    def initialize(self):
        config_dir = self.config.get('Main', 'config_dir')
        environment_path = os.path.join(config_dir, 'environment')
        self.environment = loader.walk(environment_path)
        self.builder = GraphBuilder()
        self.graph_manager = self.builder.build_graph(self.config, self.environment)
        return self.graph_manager

    def start_updaters(self):
        if 'Updater' in self.environment:
            for updater_name in self.environment['Updater']:
                args = self.environment['Updater'][updater_name]
                updater = Updater(updater_name, self.graph_manager, args['time'], self.config, self.builder)
                t = threading.Thread(target=updater.run)
                t.daemon = True
                t.start()
            graph_updater = GraphUpdater(self.graph_manager)
            t = threading.Thread(target=graph_updater.run)
            t.daemon = True
            t.start()
