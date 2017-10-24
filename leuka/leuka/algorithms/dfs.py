class Strategy(object):

    def run(self, nodes):
        if len(nodes) == 0:
            return None, None
        for node in nodes:
            checks = nodes[node].available_checks
            if len(checks) > 0:
                return checks[0], nodes[node]
        return None, None
