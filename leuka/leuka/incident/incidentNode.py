class IncidentNode(object):
    def __init__(self, node):
        self.node = node
        self.self_confidence = 0
        self.child_confidence = 0
        self.total_confidence = 0
        self.self_suspicion = 0
        self.parent_suspicion = 0
        self.total_suspicion = 0
        self.state_suspicion = {}
        for state in node.states:
            self.state_suspicion[state] = 0
        self.available_checks = list(node.checks)
        self.available_fixes = list(node.fixes)

    def get_suspicion(self):
        return self.total_suspicion

    def update_self_suspicion(self, new_suspicion):
        self.self_suspicion += ((100 - self.self_suspicion) * new_suspicion) / 100
        self.update_suspicion()

    def update_parent_suspicion(self, parent_suspicion):
        self.parent_suspicion = parent_suspicion
        self.update_suspicion()

    def update_state_suspicion(self, state, state_suspicion):
        self.state_suspicion[state] += ((100 - self.state_suspicion[state]) * state_suspicion) / 100
        self.update_suspicion()

    def update_suspicion(self):
        total_suspicion = self.self_suspicion
        for state in self.state_suspicion:
            total_suspicion += self.state_suspicion[state]
        total_suspicion = total_suspicion / (len(self.state_suspicion) + 1)
        self.total_suspicion = (total_suspicion + self.parent_suspicion) / 2

    def get_confidence(self):
        return self.total_confidence

    def update_self_confidence(self, new_confidence):
        self.self_confidence += ((100 - self.self_confidence) * new_confidence) / 100
        self.update_confidence()

    def update_child_confidence(self, child_confidence):
        self.child_confidence = sum(child_confidence)/len(child_confidence)
        self.update_confidence()

    def update_confidence(self):
        if len(self.node.children) > 0:
            self.total_confidence = (self.self_confidence + self.child_confidence) / 2
        else:
            self.total_confidence = self.self_confidence

    def run_check(self, check, config):
        self.available_checks.remove(check)
        args = config.get_args()
        print 'Running', check.name, 'for', self.node.name
        return check.run(node=self.node, **args)

    def reset_checks(self):
        self.available_checks = self.node.checks

    def get_suspicious_states(self, limit):
        suspicious_states = []
        for state in self.state_suspicion:
            suspicion = self.state_suspicion[state]
            if suspicion >= limit:
                suspicious_states.append((state, suspicion))
        return suspicious_states


