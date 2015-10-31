class Simulation:
    """An instance of this class contains the data necessary
       for an entire simulation.

    Attributes:
        links: dictionary of links (key is the ID, value is the Link object)
        flows: dictionary of flows (key is the ID, value is the Flow object)
        hosts: dictionary of hosts (key is the ID, value is the Host object)
        routers: dictionary of routers (key is the ID, value is the Router object)
    """

    def __init__(self, links, flows, hosts, routers):
        self.links = links
        self.flows = flows
        self.hosts = hosts
        self.routers = routers
        #self.event_queue = EventQueue() or something like that

    def __str__(self):
        return ("----LINKS----\n" + "\n".join(map(str, self.links.values())) + "\n"
                "----FLOWS----\n" + "\n".join(map(str, self.flows.values())) + "\n"
                "----HOSTS----\n" + "\n".join(map(str, self.hosts.values())) + "\n"
                "----ROUTERS----\n" + "\n".join(map(str, self.routers.values())))
