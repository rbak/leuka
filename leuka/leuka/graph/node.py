class Node(object):
    def __init__(self, name, nodetype, children, neighbors, checks=[], fixes={}, states={}, args={}, grouping=False):
        self.name = name
        self.type = nodetype
        self.children = children
        self.parents = set()
        self.neighbors = set()
        self.checks = checks
        self.fixes = fixes
        self.states = states
        self.args = args
        self.grouping = grouping
