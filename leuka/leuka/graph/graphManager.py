import threading


class GraphManager(object):
    def __init__(self, sources, registry):
        self.sources = sources
        self.registry = registry
        self._dynamic_registry = {}
        self.lock = threading.Lock()

    def get_nodes(self, nodetype, nodename):
        nodes = []
        if nodetype in self.registry:
            if nodename in self.registry[nodetype]:
                nodes += self.registry[nodetype][nodename]
        if nodetype in self._dynamic_registry:
            if nodename in self._dynamic_registry[nodetype]:
                nodes.append(self._dynamic_registry[nodetype][nodename])
        return nodes

    def get_dynamic_node(self, nodetype, nodename):
        if nodetype in self._dynamic_registry and nodename in self._dynamic_registry[nodetype]:
            return self._dynamic_registry[nodetype][nodename]
        else:
            return None

    def get_sources(self):
        return self.sources

    def registry_iter(self):
        for nodetype in self.registry:
            for nodename in self.registry[nodetype]:
                for node in self.registry[nodetype][nodename]:
                    yield node
        self.lock.acquire()
        for nodetype in self._dynamic_registry:
            for nodename in self._dynamic_registry[nodetype]:
                yield self._dynamic_registry[nodetype][nodename]
        self.lock.release()

    def dynamic_registry_iter(self):
        self.lock.acquire()
        for nodetype in self._dynamic_registry:
            for nodename in self._dynamic_registry[nodetype]:
                yield self._dynamic_registry[nodetype][nodename]
        self.lock.release()

    def add_dynamic_type(self, nodetype):
        self.lock.acquire()
        if nodetype not in self._dynamic_registry:
            self._dynamic_registry[nodetype] = {}
        self.lock.release()

    def add_dynamic_node(self, nodetype, nodename, node):
        self.lock.acquire()
        if nodename not in self._dynamic_registry[nodetype]:
            self._dynamic_registry[nodetype][nodename] = node
        else:
            print 'ERROR: Dyanmic node already exists'
        self.lock.release()

    def remove_dynamic_node(self, nodetype, nodename):
        self.lock.acquire()
        if nodetype in self._dynamic_registry:
            if nodename in self._dynamic_registry[nodetype]:
                del self._dynamic_registry[nodetype][nodename]
        self.lock.release()
