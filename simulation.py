import Queue
from event import Event

class Simulation:
    """An instance of this class contains the data necessary
       for an entire simulation.

    Attributes:
        event_queue: the priority queue that stores events
        global_time: the global timer in simulation time, in milliseconds.
                     This must be updated whenever an event is dequeued.
        links: dictionary of links (key is the ID, value is the Link object)
        flows: dictionary of flows (key is the ID, value is the Flow object)
        hosts: dictionary of hosts (key is the ID, value is the Host object)
        routers: dictionary of routers (key is the ID, value is the Router object)
    """

    def __init__(self, links, flows, hosts, routers):
        self.event_queue = Queue.PriorityQueue()
        self.global_time = 0
        self.links = links
        self.flows = flows
        self.hosts = hosts
        self.routers = routers

    def add_event(self, time, event):
        self.event_queue.put((time, event))

    def get_next_event(self):
        # This function gets an event from the queue, updates
        # the global timer accordingly, and returns the event
        x = self.event_queue.get_nowait()
        assert x[0] >= self.global_time
        self.global_time = x[0]
        return x[1]
    
    def step():
        try:
            event = get_next_event()
            event.perform()
            return True
        except Queue.Empty:
            return False
    
    def run():
        while step():
            pass

    def __str__(self):
        return ("----LINKS----\n" + "\n".join(map(str, self.links.values())) + "\n"
                "----FLOWS----\n" + "\n".join(map(str, self.flows.values())) + "\n"
                "----HOSTS----\n" + "\n".join(map(str, self.hosts.values())) + "\n"
                "----ROUTERS----\n" + "\n".join(map(str, self.routers.values())))
