from factory.abstract_updater import AbstractUpdater
import keystoneclient.v2_0.client as ksclient


class Tenants(AbstractUpdater):
    TYPES = ['Tenant']

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
        keystone = ksclient.Client(username=self.username, password=self.password, tenant_name=self.tenant, auth_url=self.auth_url)
        tenants = keystone.tenants.list()
        for tenant in tenants:
            node_config = {'Template': {'Resource': ['tenant']}}
            node = {'Tenant': {tenant.id: node_config}}
            self.current[('Tenant', tenant.id)] = node

    def toAdd(self):
        to_add = [self.current[x] for x in self.current if x not in self.previous]
        for tenant in to_add:
            yield tenant

    def toRemove(self):
        to_remove = [x for x in self.previous if x not in self.current]
        for tenant in to_remove:
            yield tenant
