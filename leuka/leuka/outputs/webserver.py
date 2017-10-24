import time
import jinja2
from abstractOutput import AbstractOutput

INCIDENT_TEMPLATE = 'incident.html.tmpl'
RESTING_TEMPLATE = 'resting.html.tmpl'
FILE_NAME = 'index.html'


class Webserver(AbstractOutput):
    def run(self):
        self.web_dir = self.config.get('Output', 'web_dir')
        while True:  # TODO Exit cleanly
            self._generate_page()
            time.sleep(5)

    def _reset(self):
        pass

    def _generate_page(self):
        env = {}
        env[total_nodes] = self.total_nodes

        with incident_lock:
            if self.incident_manager:
                self._load_incident_env(env)
                template = INCIDENT_TEMPLATE
            else:
                self._load_resting_env(env)
                template = RESTING_TEMPLATE

        templateLoader = jinja2.FileSystemLoader(searchpath="./web_templates/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(template)
        outputText = template.render(env)

        with open(FILE_NAME, 'w') as f_out:
            f_out.write(outputText)

    def _load_incident_env(self, env):
        env['start_time'] = self.start_time
        env['run_time'] = time.time() - self.start_time
        env['events'] = self.events
        env['runs'] = self.runs
        env['failures'] = self.failures
        env['info'] = self.info
        env['failing_nodes'] = self.failing_nodes
        env['confidence'] = self.confidence
        env['suspicion'] = self.suspicion

    def _load_resting_env(self, env):
        # last incident info
        pass
