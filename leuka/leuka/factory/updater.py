from factory.nodeframe import NodeFrame
from time import sleep
import sys
import os
import copy


class Updater(object):
    def __init__(self, name, graph, time, config, builder):
        self.name = name
        self.graph = graph
        self.time = time
        self.config_dir = config.get('Main', 'config_dir')
        updater_path = os.path.join(self.config_dir, 'scripts')
        sys.path.append(updater_path)
        self.args = config.get_args()
        self.builder = builder

    def run(self):
        self._initialize()
        while True:
            self.instance.update()
            self._add()
            self._remove()
            sleep(self.time)

    def _initialize(self):
        mod = __import__(self.name.lower())
        targetclass = getattr(mod, self.name)
        self.instance = targetclass(**self.args)
        for node_type in targetclass.TYPES:
            self.graph.add_dynamic_type(node_type)

    def _add(self):
        for nodes in self.instance.toAdd():
            new_node_list = {}
            for node_type in nodes:
                for node_name in nodes[node_type]:
                    node_config = nodes[node_type][node_name]
                    nodeframe = NodeFrame(node_name, node_type, node_config, self.builder)
                    new_node = nodeframe.get_node()
                    self.graph.add_dynamic_node(node_type, node_name, new_node)
                    new_node_list[(node_type, node_name)] = new_node
            for node_type in nodes:
                for node_name in nodes[node_type]:
                    node_config = nodes[node_type][node_name]
                    if 'GroupChildren' in node_config: #Use to create logical sets of sets of nodes.
                        node = new_node_list[(node_type, node_name)]
                        for child in node_config['GroupChildren']:
                            child_type = child['type']
                            child_name = child['name']
                            child = new_node_list[(child_type, child_name)]
                            node.children.append(child)
                            child.parents.append(node)

    def _remove(self):
        for node in self.instance.toRemove():
            node_type, node_name = node
            node = self.graph.get_dynamic_node(node_type, node_name)
            if node:
                node.to_delete = True
