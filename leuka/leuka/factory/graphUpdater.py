from time import sleep


class GraphUpdater(object):
    def __init__(self, graph):
        self.graph = graph

    def run(self):
        while True:
            to_delete = []
            for node in self.graph.dynamic_registry_iter():
                self._update_node(node, to_delete)
            for node in to_delete:
                nodetype, nodename = node
                self.graph.remove_dynamic_node(nodetype, nodename)
            sleep(1)

    def _update_node(self, node, to_delete):
        nodetype = node.type
        nodename = node.name
        if node.to_delete:
            for child in node.children:
                child.parents.remove(node)
            for parent in node.parents:
                parent.children.remove(node)
            for neighbor in node.neighbors:
                neighbor.neighbors.remove(node)
            to_delete.append((nodetype, nodename))
        else:
            for nodetype, nodename in node.children_names:
                children = self.graph.get_nodes(nodetype, nodename)
                for child in children:
                    if child not in node.children:
                        node.children.append(child)
                        child.parents.add(node)
            for nodetype, nodename in node.parents_names:
                parents = self.graph.get_nodes(nodetype, nodename)
                for parent in parents:
                    if parent not in node.parents:
                        node.parents.add(parent)
                        parent.children.append(node)
            for nodetype, nodename in node.neighbors_names:
                neighbors = self.graph.get_nodes(nodetype, nodename)
                for neighbor in neighbors:
                    if neighbor not in node.neighbors:
                        node.neighbors.add(neighbor)
                        neighbor.neighbors.add(node)
