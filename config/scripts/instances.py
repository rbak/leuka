from factory.abstract_updater import AbstractUpdater
import novaclient.v1_1.client as nvclient


class Instances(AbstractUpdater):
    TYPES = ['Instance']

    def __init__(self, **kwargs):
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.tenant = kwargs['tenant']
        self.auth_url = kwargs['auth_url']
        self.region = kwargs['region']
        self.current = {}

    def update(self):
        self.previous = self.current
        self.current = {}
        nova = nvclient.Client(self.username, self.password, self.tenant, auth_url=self.auth_url, service_type="compute", region_name = self.region)
        instances = nova.servers.list(search_opts={'all_tenants': 1})
        for instance in instances:
            node_config = {'Template': {'Resource': ['instance']},
                           'Children': {'Node': [getattr(instance, 'OS-EXT-SRV-ATTR:host')]},
                           'Parents': {'Tenant': [instance.tenant_id]}}
            node = {'Instance': {instance.id: node_config}}
            self.current[('Instance', instance.id)] = node

    def toAdd(self):
        to_add = [self.current[x] for x in self.current if x not in self.previous]
        for instance in to_add:
            yield instance

    def toRemove(self):
        to_remove = [x for x in self.previous if x not in self.current]
        for instance in to_remove:
            yield instance
