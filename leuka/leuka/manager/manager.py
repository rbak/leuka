from factory.factoryManager import FactoryManager
from incident.incidentManager import IncidentManager
from ui.inputMonitor import InputMonitor
from config import Config
import threading


class Manager(object):

    def start(self):
        self.config = Config('../config.yaml')
        factory_manager = FactoryManager(self.config)
        self.graph_manager = factory_manager.initialize()
        self.inputs = []
        self._start_inputs()
        self.outputs = []
        self._start_outputs()
        factory_manager.start_updaters()
        self.incident = None
        self._start_input_monitor(self.graph_manager)

    def _start_input_monitor(self, graph_manager):
        monitor = InputMonitor()
        monitor.initialize(graph_manager, self)
        monitor.cmdloop()

    def trigger(self, line):
        # TODO LOCK
        if not self.incident:
            self.incident = IncidentManager(self.config, self.graph_manager)
            t = threading.Thread(target=self._start_incident)
            t.daemon = True
            t.start()
        self.incident.trigger(line)

    def _start_incident(self):
        self.incident.run()
        self.incident = None

    def _start_inputs():
        inputs = self.config.get('Main', 'inputs')

    def _start_ouputs():
        outputs = self.config.get('Main', 'outputs')
        for output_type in outputs:
            # updater_path = os.path.join(config_dir, 'scripts')
            # sys.path.append(updater_path)
            self.outputmod = __import__(output_type)
            t = threading.Thread(target=self._start_incident)
            t.daemon = True
            t.start()
