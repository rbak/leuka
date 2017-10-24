from factory.abstract_updater import AbstractUpdater
import neutronclient.v2_0.client as ntclient


class Agents(AbstractUpdater):
    TYPES = ['L3Agent']

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
        agents = neutron.list_agents()
        for agent in agents['agents']:
            if agent['agent_type'] == 'L3 agent':
                routers = self._get_agent_routers(neutron, agent['id'])
                node_config = {'Template': {'Resource': ['agent']},
                               'Parents': {'Router': routers},
                               'Children': {'Node': [agent['host']]}}
                node = {'L3Agent': {agent['id']: node_config}}
                self.current[('L3Agent', agent['id'])] = node

    def _get_agent_routers(self, neutron, agent):
        routers = neutron.list_routers_on_l3_agent(agent)
        neighbors = []
        for router in routers['routers']:
            neighbors.append(router['id'])
        return neighbors

    def toAdd(self):
        to_add = [self.current[x] for x in self.current if x not in self.previous]
        for agent in to_add:
            yield agent

    def toRemove(self):
        to_remove = [x for x in self.previous if x not in self.current]
        for agent in to_remove:
            yield agent
