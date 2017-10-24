import neutronclient.v2_0.client as ntclient


def run(**kwargs):
    node = kwargs['node']
    username = kwargs['username']
    password = kwargs['password']
    tenant = kwargs['tenant']
    auth_url = kwargs['auth_url']
    region = kwargs['region']
    neutron = ntclient.Client(username=username, password=password, auth_url=auth_url, tenant_name=tenant, region_name=region)
    children = node.children
    needed_ports = {22: False}
    needed_icmp = False
    for child in children:
        if child.type == 'Securitygroup':
            print '-- Found security group', child.name
            group = neutron.show_security_group(child.name)
            for rule in group['security_group']['security_group_rules']:
                minport = rule['port_range_min']
                maxport = rule['port_range_max']
                direction = rule['direction']
                protocol = rule['protocol']
                if direction == 'ingress' and protocol == 'tcp':
                    for port in needed_ports:
                        if port >= minport and port <= maxport:
                            needed_ports[port] = True
                            print '-- Found allowed ingress for port', port
                if direction == 'ingress' and (protocol == 'icmp' or protocol == None):
                    needed_icmp = True
                    print '-- Found allowed ingress for icmp'
    for port in needed_ports:
        if not needed_ports[port]:
            return False
    if not needed_icmp:
        return False
    return True
