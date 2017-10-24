from graph.node import Node
from graph.dynamicNode import DynamicNode
from graph.state import State
from graph.check import Check
from graph.fix import Fix


class NodeFrame(object):
    def __init__(self, name, nodetype, nodeconfig, builder):
        self.name = name
        self.type = nodetype
        self.children = []
        self.parents = [] # Only used by dynamic nodes
        self.neighbors = []
        self.checks = []
        self.fixes = {}
        self.states = {}
        self.args = {}
        self.source = False
        self.grouping = False
        self.tie = None
        self.builder = builder
        self._parse_config(nodeconfig)

    def _parse_config(self, nodeconfig):
        if not nodeconfig:
            return
        if 'Template' in nodeconfig:
            templates = self.builder.templates
            for templatetype in nodeconfig['Template']:
                for template in nodeconfig['Template'][templatetype]:
                    nodeconfig.update(templates[templatetype][template])
        if 'Children' in nodeconfig:
            for nodetype in nodeconfig['Children']:
                for nodename in nodeconfig['Children'][nodetype]:
                    self.children.append((nodetype, nodename))
        if 'Parents' in nodeconfig:
            for nodetype in nodeconfig['Parents']:
                for nodename in nodeconfig['Parents'][nodetype]:
                    self.parents.append((nodetype, nodename))
        if 'Neighbors' in nodeconfig:
            for nodetype in nodeconfig['Neighbors']:
                for nodename in nodeconfig['Neighbors'][nodetype]:
                    self.neighbors.append((nodetype, nodename))
        if 'Checks' in nodeconfig:
            for check in nodeconfig['Checks']:
                cost = nodeconfig['Checks'][check]['cost']
                confidence = nodeconfig['Checks'][check]['confidence']
                states = nodeconfig['Checks'][check]['states']
                self.checks.append(Check(check, self.builder.config_dir, cost, confidence, states))
        if 'Fixes' in nodeconfig:
            for fix in nodeconfig['Fixes']:
                self.fixes[fix] = Fix(fix, self.builder.config_dir)
        if 'States' in nodeconfig:
            for state in nodeconfig['States']:
                self.states[state] = State(nodeconfig['States'][state])
        if 'Tie' in nodeconfig:
            self.tie = nodeconfig['Tie']
        if 'Source' in nodeconfig:
            if nodeconfig['Source']:
                self.source = True
        if 'Grouping' in nodeconfig:
            if nodeconfig['Grouping']:
                self.grouping = True
        if 'Args' in nodeconfig:
            self.args = nodeconfig['Args']

    def get_node(self):
        return DynamicNode(self.name, self.type, self.children, self.parents, self.neighbors, self.checks, self.fixes, self.states, self.args, self.grouping)

    def expand_node(self, nodeframes):
        real_children = set()
        for child in self.children:
            real_children.add(nodeframes[child].expand_node(nodeframes))
        return Node(self.name, self.type, real_children, self.neighbors, self.checks, self.fixes, self.states, self.args, self.grouping)
