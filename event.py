# Both of these events should be added to the global event queue as
# (time, Event) tuples. Then we get comparison for free.
# The Simulation.add_event and Simulation.get_next_event functions are good

class PacketArrivalEvent:
    """This event represents the arrival of a packet
       to the other end of a link.

    Attributes:
        packet: the Packet that is being transmitted
        link: the Link that it's traveling on
    """
    def __init__(self, packet, link):
        self.packet = packet
        self.link = link


class FlowStartEvent:
    """This event represents the delayed beginning of a
       data flow in our simulation.

    Attributes:
        flow: the Flow that is being started
    """
    def __init__(self, flow):
        self.flow = flow
