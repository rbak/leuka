import random


class Strategy(object):

    def run(self, nodes):
        if len(nodes) == 0:
            return None, None
        node = nodes[random.choice(nodes.keys())]
        if len(node.available_checks) == 0:
            return None, None
        check = random.choice(node.available_checks)
        return check, node
