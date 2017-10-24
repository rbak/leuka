import threading
import time


class AbstractOutput(object):
    def __init__(self, config):
        self.config = config
        self.graph_manager = None
        self.total_nodes = 0
        self.incident_lock = threading.Lock()
        self.time_lock = threading.Lock()
        self._reset()

    # Add this method for outputs that update at intervals.
    # def run(self):
    #     pass

    def notify_incident_start(self, incident_manager):
        self.incident_manager = incident_manager
        with time_lock:
            if not self.start_time:
                self.start_time = time.time()

    def notify_incident_end(self):
        self._poll()
        self._reset()

    def notify_event(self, event):
        self.events.append((event, time.time()))

    def notify_run(self, run):
        self.runs.append((run, time.time()))

    def notify_failure(self, failure):
        self.failures.append((failure, time.time()))

    def notify_info(self, info):
        self.info.append((info, time.time()))

    def set_cause(self, cause):
        self.cause = cause

    def set_actions(self, actions):
        self.actions = actions

    def _poll(self):
        with incident_lock:
            if self.incident_manager:
                self._poll_explored_nodes()
                self._poll_failing_nodes()
                self._poll_confidence()
                self._poll_suspicion()

    def _poll_total_nodes(self):
        self.total_nodes = self.graph_manager.get_num_nodes()

    def _poll_failing_nodes(self):
        self.failing_nodes = self.incident_manager.get_num_nodes()

    def _poll_confidence(self):
        self.confidence = self.incident_manager.get_confidence()

    def _poll_suspicion(self):
        self.suspicion = self.incident_manager.get_suspicion()

    def _reset(self):
        with incident_lock:
            self.incident_manager = None
            self.start_time = None

            self.events = []
            self.runs = []
            self.failures = []
            self.info = []

            self.failing_nodes = 0
            self.confidence = 0
            self.suspicion = 0
