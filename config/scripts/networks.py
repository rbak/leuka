from factory.abstract_updater import AbstractUpdater
import neutronclient.v2_0.client as ntclient


class Networks(AbstractUpdater):
    TYPES = ['Network']

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
        networks = neutron.list_networks()
        for network in networks['networks']:
            neighbors = []
            for subnet in network['subnets']:
                neighbors.append(subnet)
            node_config = {'Template': {'Resource': ['network']},
                           'Neighbors': {'Subnet': neighbors},
                           'Parents': {'Tenant': [network['tenant_id']]}}
            node = {'Network': {network['id']: node_config}}
            self.current[('Network', network['id'])] = node

    def toAdd(self):
        to_add = [self.current[x] for x in self.current if x not in self.previous]
        for network in to_add:
            yield network

    def toRemove(self):
        to_remove = [x for x in self.previous if x not in self.current]
        for network in to_remove:
            yield network
