import Queue, sys
from event import Event, FlowWakeEvent

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
        for flow in flows.values():
            flow.event_scheduler = EventScheduler(self)
            self.add_event(flow.start_time, FlowWakeEvent(flow))
        for link in links.values():
            link.event_scheduler = EventScheduler(self)

    def add_event(self, time, event):
        self.event_queue.put((time, event))

    def get_next_event(self):
        # This function gets an event from the queue, updates
        # the global timer accordingly, and returns the event
        x = self.event_queue.get_nowait()
        assert x[0] >= self.global_time
        self.global_time = x[0]
        return x[1]

    def step(self):
        try:
            event = self.get_next_event()
            event.perform()
            return True
        except Queue.Empty:
            return False

    def all_flows_complete(self):
        # there has got to be a cleaner one-line way to do this
        all_complete = True
        for flow in self.flows.values():
            if not flow.complete:
                all_complete = False
        return all_complete

    def run(self):
        while self.step():
            if self.all_flows_complete():
                sys.exit("All flows finished transmitting")

    def __str__(self):
        return ("----LINKS----\n" + "\n".join(map(str, self.links.values())) + "\n"
                "----FLOWS----\n" + "\n".join(map(str, self.flows.values())) + "\n"
                "----HOSTS----\n" + "\n".join(map(str, self.hosts.values())) + "\n"
                "----ROUTERS----\n" + "\n".join(map(str, self.routers.values())))

class EventScheduler:
    def __init__(self, simulation):
        self.simulation = simulation

    def delay_event(self, delay, event):
        self.simulation.add_event(self.simulation.global_time + delay, event)
