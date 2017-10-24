from factory.abstract_updater import AbstractUpdater
import neutronclient.v2_0.client as ntclient


class Securitygroups(AbstractUpdater):
    TYPES = ['Securitygroup']

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
        neutron = ntclient.Client(username=self.username, password=self.password, auth_url=self.auth_url, tenant_name=self.tenant, region_name=self.region)
        securitygroups = neutron.list_security_groups()
        for securitygroup in securitygroups['security_groups']:
            node_config = {'Template': {'Resource': ['securitygroup']},
                           'Parents': {'Tenant': [securitygroup['tenant_id']]}}
            node = {'Securitygroup': {securitygroup['id']: node_config}}
            self.current[('Securitygroup', securitygroup['id'])] = node

    def toAdd(self):
        to_add = [self.current[x] for x in self.current if x not in self.previous]
        for securitygroup in to_add:
            yield securitygroup

    def toRemove(self):
        to_remove = [x for x in self.previous if x not in self.current]
        for securitygroup in to_remove:
            yield securitygroup
