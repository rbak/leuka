import cmd
from visualizer import Visualizer


class InputMonitor(cmd.Cmd):
    prompt = "> "

    # Used instead of overriding init
    def initialize(self, graph, manager):
        self.graph = graph
        self.manager = manager
        self.visualizer = None

    def do_print(self, line):
        "Display basic environment information\nEg. show tree, show Region region1"
        if line == "":
            print "Must provide an argument"
        else:
            args = line.split()
            node_type = args[0]
            node_name = args[1]
            if node_type in self.graph.registry:
                type_registry = self.graph.registry[node_type]
            elif node_type in self.graph.dynamic_registry:
                type_registry = self.graph.dynamic_registry[node_type]
            else:
                print 'Node type "%s" not found' % node_type
                return
            if node_name in type_registry:
                node = type_registry[node_name]
            else:
                print 'Node "%s" not found' % node_name
            print node.name

    def do_visual(self, line):
        "Visual display of environment\nOptions: start, show, stop"
        options = ["start", "show", "stop"]
        if line and line.lower() in options:
            if not self.visualizer:
                self.visualizer = Visualizer(self.graph, self.manager)
            method = getattr(self.visualizer, line.lower())
            method()
        else:
            print "Options:", ", ".join(options)

    def do_show(self, line):
        "Changes the visual display"
        options = ["type", "state", "neighbors"]
        if line and line.lower() in options:
            if not self.visualizer:
                print "Start visualizer before calling show"
            method = getattr(self.visualizer, "show_"+line.lower())
            method()
        else:
            print "Options:", ", ".join(options)

    def do_hide(self, line):
        "Changes the visual display"
        options = ["neighbors"]
        if line and line.lower() in options:
            if not self.visualizer:
                print "Start visualizer before calling hide"
            method = getattr(self.visualizer, "hide_"+line.lower())
            method()
        else:
            print "Options:", ", ".join(options)

    def do_trigger(self, line):
        "Trigger incident in environment"
        if line == "":
            print "Must provide an argument"
        else:
            self.manager.trigger(line)

    def do_exit(self, line):
        "Exit program"
        if self.visualizer:
            self.visualizer.stop()
        exit(0)

        # def monitor(self, monitor):
    #     monitormod = __import__(monitor)
    #     monitormod.monitor(self)

    # def alarm(self, alarm, **kwargs):
    #     print 'Alarm detected for ',alarm
    #     modname = alarm.replace(' ','_')
    #     try:
    #         alarmmod = __import__(modname)
    #         alarmmod.alarm(self,**kwargs)
    #     except Exception as e:
    #         print "No such alarm:",alarm
