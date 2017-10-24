from incidentNode import IncidentNode
from algorithms.dfs import Strategy
import threading
import time
# import decision algorithm

WEIGHTS = {'low': 20, 'med': 50, 'high': 80}


class IncidentManager(object):
    def __init__(self, config, graph):
        self.config = config
        self.graph = graph
        self.nodes = {}  # key=node,value=incidentnode.  Allows reverse lookup of incident information
        self.start = time.time()
        self.last_update = time.time()

        self.incident_window = self.config.get('Main', 'incident_window')
        self.weights = self.config.getWeights()

    def run(self):
        self._diagnose()

    def trigger(self, trigger):
        self.last_update = time.time()
        path = trigger.split()
        if path[0] == '*':
            for node in self.graph.registry_iter():
                if node.name == path[1]:
                    self._trigger(node)
        else:
            nodes = self.graph.get_nodes(path[0], path[1])
            if len(nodes) == 0:
                print 'Node', trigger, 'not found'
            for node in nodes:
                self._trigger(node)
        print 'Incident registered for', trigger
            # for node in self.graph.get_sources():
            #     if node.name == path[0]:
            #         self._trigger_child(path[1:], self.sources[node])

    # def _search_for_trigger(self, path, node):
    #     if not path:
    #         self._trigger(node)
    #         return
    #     for child in node.children:
    #         if child.name == path[0]:
    #             self._search_for_trigger(path[1:], child)

    def _trigger(self, node):
        if node not in self.nodes:
            self.nodes[node] = IncidentNode(node)
        for child in node.children:
            self._trigger(child)

    def _diagnose(self):
        time_since_update = time.time() - self.last_update
        strategy = Strategy()
        while time_since_update < self.incident_window:
            best_check, node = strategy.run(self.nodes)
            if best_check == None:
                time.sleep(1)
            else:
                result = node.run_check(best_check, self.config)
                self._update_incident(node, best_check, result)
                self.last_update = time.time() # TODO REMOVE
                # depending on time run fixes? TODO
                    # reset diagonosis?
                # depeding on time generate report? TODO
            time_since_update = time.time() - self.last_update
        self._generate_report()

    def _update_incident(self, node, check, result):
        node.update_self_confidence(check.confidence)
        self._update_confidence(node)
        if not result:
            for state in check.states:
                weight = check.states[state]
                if type(weight) == str:
                    weight = self.weights[weight]
                node.update_state_suspicion(state, weight)
            self._update_suspicion(node)

    def _update_confidence(self, incident_node):
        node = incident_node.node
        confidence = incident_node.get_confidence()
        parents = node.parents
        for parent in parents:
            if parent in self.nodes:
                incident_parent = self.nodes[parent]
                children = parent.children
                child_confidence = []
                for child in children:
                    if child in self.nodes:
                        incident_child = self.nodes[child]
                        child_confidence.append(incident_child.get_confidence())
                incident_parent.update_child_confidence(child_confidence)
                self._update_confidence(incident_parent)

# TODO Doesn't account for multiple icident parents
    def _update_suspicion(self, incident_node):
        node = incident_node.node
        suspicion = incident_node.get_suspicion()
        children = node.children
        for child in children:
            incident_child = self.nodes[child]
            incident_child.update_parent_suspicion(suspicion)

    def _repair():
        pass # TODO

    def _generate_report(self):
        print '-'*30
        print 'Diagnostic complete'
        found = {}
        for node in self.nodes:
            states = self.nodes[node].get_suspicious_states(50)
            if len(states) > 0:
                found[node] = states
        if len(found) > 0:
            print 'Probable causes of incident'
            print '-'*30
            probable_state = None
            probable_node = None
            probable_suspicion = 0
            for node in found:
                print node.name, 'in state:'
                for state in found[node]:
                    state, suspicion = state
                    print '     -', state, suspicion
                    if suspicion >= probable_suspicion:
                        probable_suspicion = suspicion
                        probable_node = node
                        probable_state = state
            print '-'*30
            print 'Recommended fix:'
            action = probable_node.states[probable_state].actions[0]
            probable_node.fixes[action].tell()
        else:
            print 'No problems detected'
