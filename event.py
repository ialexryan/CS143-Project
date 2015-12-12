# Both of these events should be added to the global event queue as
# (time, Event) tuples. Then we get comparison for free.
# The Simulation.add_event and Simulation.get_next_event functions are good

import sys

class Event:
    """Function implemented by concrete base classes of Event to perform their function.

    Attributes:
        is_canceled: records whether an event has been canceled
    """
    def __init__(self):
        self.is_canceled = False

    def perform(self):
        sys.exit("Abstract method perform not implemented")

class PacketArrivalEvent(Event):
    """This event represents the arrival of a packet
       to the other end of a link.

    Attributes:
        packet: the Packet that is being transmitted
        device: the Device on the other end of the link to which it's traveling
        from_link: the Link on which the packet is arriving
    """
    def __init__(self, packet, device, from_link):
        Event.__init__(self)
        self.packet = packet
        self.from_link = from_link
        self.device = device

    def perform(self):
        self.device.handle_packet(self.packet, self.from_link)

class LinkReadyEvent(Event):
    """This event represents the delay between when a links
        sends a given packet and when it can again send another
        packet. This event wakes the link up to continue sending.

    Attributes:
        link: The Link that's busy until the next wake
    """

    def __init__(self, link):
        Event.__init__(self)
        self.link = link

    def perform(self):
        self.link.wake()


class FlowWakeEvent(Event):
    """This event represents the delayed beginning of a
       data flow in our simulation. It also is used to
       wake the flow back up after it waits for congestion
       control reasons.

    Attributes:
        flow: the Flow that is being started
    """
    def __init__(self, flow):
        Event.__init__(self)
        self.flow = flow

    def perform(self):
        self.flow.wake()

class RoutingUpdateEvent(Event):
    """This event triggers a routing table update by instructing
       its associated host to send a routing packet.

    Attributes:
        host: the host for which the routing information needs be updated
    """
    def __init__(self, host):
        Event.__init__(self)
        self.host = host

    def perform(self):
        self.host.send_routing_packet()

class PrintElapsedSimulationTimeEvent(Event):
    """This event is scheduled every 0.2 seconds (in simulation time) and updates
        the terminal with the amount of time that has elapsed."""

    def __init__(self, time, event_queue):
        Event.__init__(self)
        self.time = time
        self.event_queue = event_queue

    def perform(self):
        sys.stderr.write('\rSimulation time: {0:.1f}s'.format(self.time / 1000.0))
        self.event_queue.delay_event(200, PrintElapsedSimulationTimeEvent(self.time + 200, self.event_queue))
