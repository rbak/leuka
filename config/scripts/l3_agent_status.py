import neutronclient.v2_0.client as ntclient


def run(**kwargs):
    node = kwargs['node']
    username = kwargs['username']
    password = kwargs['password']
    tenant = kwargs['tenant']
    auth_url = kwargs['auth_url']
    region = kwargs['region']
    neutron = ntclient.Client(username=username, password=password, auth_url=auth_url, tenant_name=tenant, region_name=region)
    agent = neutron.show_agent(node.name)
    if agent['agent']['alive']:
        print '-- L3 agent is alive'
        return True
    else:
        print '-- L3 agent is down'
        return False
