# Both of these events should be added to the global event queue as
# (time, Event) tuples. Then we get comparison for free.
# The Simulation.add_event and Simulation.get_next_event functions are good

class Event:
    def perform(self):
        sys.exit("Abstract method perform not implemented")

class PacketArrivalEvent(Event):
    """This event represents the arrival of a packet
       to the other end of a link.

    Attributes:
        packet: the Packet that is being transmitted
        link: the Link that it's traveling on
        device: the Device on the other end of the link to which it's traveling
    """
    def __init__(self, packet, link, device):
        self.packet = packet
        self.link = link
        self.device = device

    def perform(self):
        pass


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
        pass
