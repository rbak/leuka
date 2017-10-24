from factory.abstract_updater import AbstractUpdater
import neutronclient.v2_0.client as ntclient


class Routers(AbstractUpdater):
    TYPES = ['Router']

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
        routers = neutron.list_routers()
        for router in routers['routers']:
            subnets = []
            network = []
            if 'external_gateway_info' in router and router['external_gateway_info']:
                gateway_info = router['external_gateway_info']
                if 'network_id' in gateway_info:
                    network = [gateway_info['network_id']]
                if 'external_fixed_ips' in gateway_info:
                    for subnet in gateway_info['external_fixed_ips']:
                        subnets.append(subnet['subnet_id'])
            node_config = {'Template': {'Resource': ['router']},
                           'Neighbors': {'Subnet': subnets,
                                         'Networks': network},
                           'Parents': {'Tenant': [router['tenant_id']]}}
            node = {'Router': {router['id']: node_config}}
            self.current[('Router', router['id'])] = node

    def toAdd(self):
        to_add = [self.current[x] for x in self.current if x not in self.previous]
        for router in to_add:
            yield router

    def toRemove(self):
        to_remove = [x for x in self.previous if x not in self.current]
        for router in to_remove:
            yield router
