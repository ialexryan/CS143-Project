import sys, Queue
import stats
from event import Event, FlowWakeEvent, RoutingUpdateEvent, PrintElapsedSimulationTimeEvent
from logger import Logger
from clock import Clock
from event_queue import EventQueue

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

    def __init__(self, links, flows, hosts, routers, verbose, fast_insteadof_reno):
        self.links = links
        self.flows = flows
        self.hosts = hosts
        self.routers = routers

        # Set up clocks
        self.clock = Clock()
        for item in flows.values():
            item.controller.clock = self.clock
        for item in hosts.values():
            item.clock = self.clock

        # Set up event schedulers
        self.event_queue = EventQueue(self.clock)
        for flow in flows.values() + links.values() + hosts.values():
            flow.event_scheduler = self.event_queue
        for flow in flows.values():
            flow.controller.event_scheduler = self.event_queue

        # Set up initial events
        for flow in flows.values():
            self.event_queue.delay_event(flow.start_time, FlowWakeEvent(flow))
        for host in hosts.values():
            self.event_queue.delay_event(0, RoutingUpdateEvent(host))

        # Set up logging
        self.logger = Logger(self.clock, verbose, fast_insteadof_reno)
        for item in flows.values() + links.values() + hosts.values() + routers.values():
            item.set_logger(self.logger)

        # Set up PrintElapsedSimulationTimeEvents
        if not verbose:  # combining this with verbose mode would be chaos.
            self.event_queue.delay_event(0, PrintElapsedSimulationTimeEvent(self.clock.current_time, self.event_queue))

        print "Simulation started..."

    """Performs a single event from the event queue."""
    def step(self):
        try:
            event = self.event_queue.dequeue_next_event()
            event.perform()
            return True
        except Queue.Empty:
            return False

    """Determines whether all flows have been completed."""
    def all_flows_finished(self):
        for flow in self.flows.values():
            if not flow.completed():
                return False
        return True

    """Repeatedly performs events from the queue until all flows have been completed."""
    def run(self):
        while not self.all_flows_finished():
            if not self.step():
                sys.exit("TCP deadlock: event queue empty but flows not complete")

        print "All flows finished transmitting!"
        print "Elapsed time in simulation world: " + str(self.clock)

    def __str__(self):
        return ("----LINKS----\n" + "\n".join(map(str, self.links.values())) + "\n"
                "----FLOWS----\n" + "\n".join(map(str, self.flows.values())) + "\n"
                "----HOSTS----\n" + "\n".join(map(str, self.hosts.values())) + "\n"
                "----ROUTERS----\n" + "\n".join(map(str, self.routers.values())))
