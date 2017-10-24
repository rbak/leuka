from factory.abstract_updater import AbstractUpdater
import neutronclient.v2_0.client as ntclient


class Floatingips(AbstractUpdater):
    TYPES = ['Floatingip']

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
        floatingips = neutron.list_floatingips()
        for floatingip in floatingips['floatingips']:
            node_config = {'Template': {'Resource': ['floatingip']},
                           'Neighbors': {'Network': [floatingip['floating_network_id']]},
                           'Parents': {'Tenant': [floatingip['tenant_id']]}}
            node = {'Floatingip': {floatingip['floating_ip_address']: node_config}}
            self.current[('Floatingip', floatingip['floating_ip_address'])] = node

    def toAdd(self):
        to_add = [self.current[x] for x in self.current if x not in self.previous]
        for floatingip in to_add:
            yield floatingip

    def toRemove(self):
        to_remove = [x for x in self.previous if x not in self.current]
        for floatingip in to_remove:
            yield floatingip
