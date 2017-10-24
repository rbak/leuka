from factory.abstractUpdater import AbstractUpdater
import random


class Routers(AbstractUpdater):
    TYPES = ['Router']

    def __init__(self, **kwargs):
        self.current = {}
        self.update()

    def update(self):
        self.previous = self.current
        self.current = {}
        router_id = "%0.5d" % random.randint(0, 99999)
        node_config = {'Children': {'Node': ["compute-00%d" % random.randint(1, 3)]},
                       'Template': {'Resource': ['router']}}
        node = {'Router': {router_id: node_config}}
        self.current[('Router', router_id)] = node

    def toAdd(self):
        to_add = [self.current[x] for x in self.current if x not in self.previous]
        for router in to_add:
            yield router

    def toRemove(self):
        to_remove = [x for x in self.previous if x not in self.current]
        for router in to_remove:
            yield router
