import Queue, sys
from event import Event, FlowWakeEvent, RoutingUpdateEvent
from logger import Logger
from clock import Clock

# Remove once TCP algorithm works
TEMP_LARGE_VALUE = 10000

class Simulation:
    """An instance of this class contains the data necessary
       for an entire simulation.

    Attributes:
        event_queue: the priority queue that stores events
        clock: the clock that must be updated whenever an event is dequeued
        links: dictionary of links (key is the ID, value is the Link object)
        flows: dictionary of flows (key is the ID, value is the Flow object)
        hosts: dictionary of hosts (key is the ID, value is the Host object)
        routers: dictionary of routers (key is the ID, value is the Router object)
    """

    def __init__(self, links, flows, hosts, routers, verbose):
        self.event_queue = Queue.PriorityQueue()
        self.clock = Clock()
        self.links = links
        self.flows = flows
        self.hosts = hosts
        self.routers = routers
        
        event_scheduler = EventScheduler(self)
        
        # Set up event schedulers
        for flow in flows.values():
            flow.event_scheduler = event_scheduler
        for link in links.values():
            link.event_scheduler = event_scheduler
        for host in hosts.values():
            host.event_scheduler = event_scheduler
        
        # Set up initial events
        for flow in flows.values():
            event_scheduler.delay_event(flow.start_time + TEMP_LARGE_VALUE, FlowWakeEvent(flow))
        for host in hosts.values():
            event_scheduler.delay_event(0, RoutingUpdateEvent(host))
        
        # Set up logging
        self.logger = Logger(self.clock, verbose)
        for object in flows.values() + links.values() + hosts.values() + routers.values():
            object.logger = self.logger

        # Set up clocks
        for object in hosts.values():
            object.clock = self.clock

    def add_event(self, time, event):
        self.event_queue.put((time, event))

    def get_next_event(self):
        # This function gets an event from the queue, updates
        # the global timer accordingly, and returns the event
        x = self.event_queue.get_nowait()
        assert x[0] >= self.clock.current_time
        self.clock.current_time = x[0]
        return x[1]

    def step(self):
        try:
            event = self.get_next_event()
            event.perform()
            return True
        except Queue.Empty:
            return False

    def all_flows_finished(self):
        for flow in self.flows.values():
            if not flow.completed():
                return False
        return True
        
    def run(self):
        while not self.all_flows_finished():
            if not self.step():
                sys.exit("TCP deadlock: event queue empty but flows not complete")
    
        print "All flows finished transmitting!"
        print "Elapsed time in simulation world: " + str(self.clock)
        exit()

    def __str__(self):
        return ("----LINKS----\n" + "\n".join(map(str, self.links.values())) + "\n"
                "----FLOWS----\n" + "\n".join(map(str, self.flows.values())) + "\n"
                "----HOSTS----\n" + "\n".join(map(str, self.hosts.values())) + "\n"
                "----ROUTERS----\n" + "\n".join(map(str, self.routers.values())))

class EventScheduler:
    def __init__(self, simulation):
        self.simulation = simulation

    def delay_event(self, delay, event):
        self.simulation.add_event(self.simulation.clock.current_time + delay, event)
