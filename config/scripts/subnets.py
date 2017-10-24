from factory.abstract_updater import AbstractUpdater
import neutronclient.v2_0.client as ntclient


class Subnets(AbstractUpdater):
    TYPES = ['Subnet']

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
        subnets = neutron.list_subnets()
        for subnet in subnets['subnets']:
            node_config = {'Template': {'Resource': ['subnet']},
                           'Neighbors': {'Network': [subnet['network_id']]},
                           'Parents': {'Tenant': [subnet['tenant_id']]}}
            node = {'Subnet': {subnet['id']: node_config}}
            self.current[('Subnet', subnet['id'])] = node

    def toAdd(self):
        to_add = [self.current[x] for x in self.current if x not in self.previous]
        for subnet in to_add:
            yield subnet

    def toRemove(self):
        to_remove = [x for x in self.previous if x not in self.current]
        for subnet in to_remove:
            yield subnet
