# Both of these events should be added to the global event queue as
# (time, Event) tuples. Then we get comparison for free.
# The Simulation.add_event and Simulation.get_next_event functions are good

from flow import Flow

class Event:
    def perform(self):
        sys.exit("Abstract method perform not implemented")

class PacketArrivalEvent(Event):
    """This event represents the arrival of a packet
       to the other end of a link.

    Attributes:
        packet: the Packet that is being transmitted
        device: the Device on the other end of the link to which it's traveling
    """
    def __init__(self, packet, device):
        self.packet = packet
        self.device = device

    def perform(self):
        self.device.handle_packet(self.packet)

class LinkWakeEvent(Event):
    """This event represents the delay between when a links
        sends a given packet and when it can again send another
        packet. This event wakes the link up to continue sending.
        
    Attributes:
        link: the Link that's busy until the next wake
    """

    def __init__(self, link):
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
        self.flow = flow

    def perform(self):
        self.flow.wake()
