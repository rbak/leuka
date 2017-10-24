import xmlrpclib
import random
import subprocess
import threading
from time import sleep


class Visualizer(object):
    COLOR_MAX = 200

    def __init__(self, net, manager):
        self.net = net
        self.manager = manager
        self.server = None
        self.conn = None
        self.graph = None
        self.initialized = False
        self.update = True
        self.quick_change = True
        self.colorize = True

    def start(self):
        self._server_start()
        self.run = True
        t = threading.Thread(target=self._run_visualizer)
        t.daemon = True
        t.start()

    def show(self):
        self.run = False
        self._server_start()
        self._initialize_graph()
        self._update_graph()

    def stop(self):
        self.run = False
        self._server_stop()

    def show_type(self):
        self.colorize = True
        self.quick_change = True
        self.update = True

    def show_state(self):
        self.colorize = False
        self.quick_change = True
        self.update = True

    def show_neighbors(self):
        print 'IMPLEMENT'

    def hide_neightbors(self):
        print 'IMPLEMENT'

    def _server_start(self):
        if not self.server:
            self.server = subprocess.Popen(["./ui/ubigraph_server"])
            sleep(1)

    def _server_stop(self):
        if self.server:
            self.server.terminate()
            self.server = None
            self.conn = None
            self.graph = None
            self.initialized = False

    def _run_visualizer(self):
        self._initialize_graph()
        self.color_current = {}
        self.color_goal = {}
        x = 0
        while self.run:
            x += 1
            if x == 50:
                self.update = True
            if self.update or self.manager.incident:
                self._update_graph()
                self.update = False
                x = 0
            sleep(.1)

    def _initialize_graph(self):
        if not self.initialized:
            server_url = 'http://127.0.0.1:20738/RPC2'
            self.conn = xmlrpclib.Server(server_url)
        self.conn.ubigraph.clear()

        self.graph = self.conn.ubigraph
        self.graph.set_edge_style_attribute(0, "oriented", "true")

        self.previous_nodes = set()
        self.vertices = {}
        self.child_edges = {}
        self.styles = self._load_styles()
        self.initialized = True

    def _load_styles(self):
        styles = {}
        with open('../../styles.txt') as f:
            for line in f:
                style_args = line.split('# ')[0].split(',')
                nodetype = style_args[0]
                style = [int(x) for x in style_args[1:]]
                styles[nodetype] = tuple(style)
        return styles

    def _update_graph(self):
        current_nodes = set()
        for node in self.net.registry_iter():
            current_nodes.add(node)
        to_remove = self.previous_nodes.difference(current_nodes)
        to_add = current_nodes.difference(self.previous_nodes)
        to_update = current_nodes.intersection(self.previous_nodes)
        for node in to_remove:
            self.graph.remove_vertex(self.vertices[node])
        for node in to_add:
            vertex = self.graph.new_vertex()
            self.graph.set_vertex_attribute(vertex, "shape", "sphere")
            label = node.name
            self.graph.set_vertex_attribute(vertex, "label", label)
            self.vertices[node] = vertex
            self._update_node(node, vertex)
        for node in to_update:
            vertex = self.vertices[node]
            self._update_node(node, vertex)
        self.quick_change = False
        self.previous_nodes = current_nodes

    def _update_node(self, node, vertex):
        self._set_style(node, vertex)
        self._update_color(self.vertices[node])
        for child in node.children:
            vertex = self.vertices[node]
            if child in self.vertices:
                vertex_c = self.vertices[child]
                if (vertex, vertex_c) not in self.child_edges:
                    self.child_edges[(vertex, vertex_c)] = self.graph.new_edge(vertex,vertex_c)

    def _update_color(self, vertex):
        if self.quick_change or vertex not in self.color_current:
            goal = self.color_goal[vertex]
            self.graph.set_vertex_attribute(vertex, "color", ('#%02X%02X%02X' % goal))
            self.color_current[vertex] = goal

            return
        current = self.color_current[vertex]
        goal = self.color_goal[vertex]

        if current == goal:
            return
        r_dif = goal[0] - current[0]
        g_dif = goal[1] - current[1]
        b_dif = goal[2] - current[2]
        if abs(r_dif) >= abs(g_dif) and abs(r_dif) >= abs(b_dif):
            r_change, g_change, b_change =  self._calculate_color_change(r_dif, g_dif, b_dif)
        elif abs(g_dif) >= abs(r_dif) and abs(g_dif) >= abs(b_dif):
            g_change, r_change, b_change =  self._calculate_color_change(g_dif, r_dif, b_dif)
        elif abs(b_dif) >= abs(g_dif) and abs(b_dif) >= abs(r_dif):
            b_change, g_change, r_change =  self._calculate_color_change(b_dif, g_dif, r_dif)
        else:
            print 'COLOR ERROR'
        r_new = current[0] + r_change
        g_new = current[1] + g_change
        b_new = current[2] + b_change
        self.graph.set_vertex_attribute(vertex, "color", ('#%02X%02X%02X' % (r_new,g_new,b_new)))
        self.color_current[vertex] = (r_new, g_new, b_new)

    def _calculate_color_change(self, color1_dif, color2_dif, color3_dif):
        MAX_CHANGE = 20
        if abs(color1_dif) > MAX_CHANGE:
            if color1_dif > 0:
                color1_change = MAX_CHANGE
            else:
                color1_change = -MAX_CHANGE
        else:
            color1_change = color1_dif
        color2_change = int(color2_dif*(abs(color2_dif)/abs(color1_dif)))
        color3_change = int(color3_dif*(abs(color3_dif)/abs(color1_dif)))
        return color1_change, color2_change, color3_change

    def _set_style(self, node, vertex):
        if self.colorize:
            nodetype = node.type
            if nodetype in self.styles:
                style = self.styles[nodetype]
            else:
                r = lambda: random.randint(0,255)
                style = (r(),r(),r())
                self.styles[nodetype] = style
            self.color_goal[vertex] = style
        else:
            if self.manager.incident and node in self.manager.incident.nodes:
                incident_node = self.manager.incident.nodes[node]
                suspicion = incident_node.get_suspicion()
                confidence = incident_node.get_confidence()
                value = 50 - (confidence/2) + suspicion
                if value > 50:
                    red = self.COLOR_MAX
                    green = (self.COLOR_MAX * 2) - ((value * self.COLOR_MAX)/50)
                else:
                    green = self.COLOR_MAX
                    red = (value * self.COLOR_MAX)/50
                self.color_goal[self.vertices[node]] = (red, green, 0)
            else:
                self.color_goal[vertex] = (0, self.COLOR_MAX, 0)

            # if node.incident:
            #     suspicion = node.incident.get_suspicion()
            #     confidence = node.incident.get_confidence()
            #     value = 50 - (confidence/2) + suspicion
            #     if value > 50:
            #         red = self.COLOR_MAX
            #         green = (self.COLOR_MAX * 2) - ((value * self.COLOR_MAX)/50)
            #     else:
            #         green = self.COLOR_MAX
            #         red = (value * self.COLOR_MAX)/50
            #     self.color_goal[self.vertices[node]] = (red, green, 0)
            # else:
