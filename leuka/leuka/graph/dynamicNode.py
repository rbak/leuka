from node import Node


class DynamicNode(Node):
    def __init__(self, name, nodetype, children, parents, neighbors, checks=[], fixes={}, states={}, args={}, grouping=False):
        self.name = name
        self.type = nodetype
        self.children_names = children
        self.children = []
        self.parents_names = parents
        self.parents = set()
        self.neighbors_names = neighbors
        self.neighbors = set()
        self.checks = checks
        self.fixes = fixes
        self.states = states
        self.args = args
        self.grouping = grouping
        self.to_delete = False
