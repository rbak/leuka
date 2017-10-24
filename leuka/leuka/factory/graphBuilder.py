import manager.loader
from graph.graphManager import GraphManager
from nodeframe import NodeFrame


class GraphBuilder(object):
    RESERVED_TYPES = ['Template', 'Updater']

    def build_graph(self, config, environment):
        self.config_dir = config.get('Main', 'config_dir')
        nodeframes = self._generate_nodeframes(environment)
        sources = self._find_sources(nodeframes)
        trees = self._generate_trees(sources, nodeframes)
        registry = {}
        for source in trees:
            self._register(trees[source], registry)
        self._tie_trees(trees, nodeframes, registry)
        # Check for cycles in graph?
        for node in trees:
            self._notify_children(trees[node])
        graph = GraphManager(trees, registry)
        return graph

    def _generate_nodeframes(self, environment):
        self.checks = {}
        self.fixes = {}
        if 'Template' in environment:
            self.templates = environment['Template']
        else:
            self.templates = {}
        nodeframes = {}
        for nodetype in environment:
            if nodetype in self.RESERVED_TYPES:
                continue
            instances = environment[nodetype]
            for instance in instances:
                instance_info = instances[instance]
                nodeframes[(nodetype, instance)] = NodeFrame(instance, nodetype, instance_info, self)
        return nodeframes

    def _find_sources(self, nodeframes):
        sources = set()
        for node in nodeframes:
            if nodeframes[node].source:
                sources.add(node)
        return sources

    def _generate_trees(self, sources, nodeframes):
        trees = {}
        for source in sources:
            trees[source] = nodeframes[source].expand_node(nodeframes)
        return trees

    def _register(self, node, registry):
        if node.type not in registry:
            registry[node.type] = {}
        if node.name not in registry[node.type]:
            registry[node.type][node.name] = []
        registry[node.type][node.name].append(node)
        for child in node.children:
            self._register(child, registry)

    def _tie_trees(self, trees, nodeframes, registry):
        for nodename in nodeframes:
            node = nodeframes[nodename]
            if node.tie:
                level = node.tie['level']
                for childtype in node.tie:
                    if childtype == 'level':
                        continue
                    for childname in node.tie[childtype]:
                        knot = {'level': level, 'parent': (node.type, node.name), 'child': (childtype, childname)}
                        # print knot
                        self._tie(knot, registry)

    def _tie(self, knot, registry):
        level = knot['level']
        nodes = registry[level]
        for name in nodes:
            for node in nodes[name]:
                children = self._tie_child(node, knot['child'])
                self._tie_parent(node, knot['parent'], children)

    def _tie_child(self, node, knot_child):
        children = set()
        for child in node.children:
            children = children.union(self._tie_child(child, knot_child))
        if knot_child == (node.type, node.name):
            children.add(node)
        return children

    def _tie_parent(self, node, parent_name, children):
        if parent_name == (node.type, node.name):
            node.children = node.children.union(children)
        for child in node.children:
            self._tie_parent(child, parent_name, children)

    def _notify_children(self, node):
        for child in node.children:
            child.args.update(node.args)
            child.parents.add(node)
            self._notify_children(child)
