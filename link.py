from __future__ import division
import sys
import Queue
from event import LinkReadyEvent, PacketArrivalEvent

class Buffer:
    """A buffer that holds packets that are waiting to send.

    Attributes:
        available_space: how much space in the buffer is free, in bytes
        link: the link this buffer belongs to
        queue: the Queue of packets waiting in the buffer
        logger: the Logger used by the buffer
    """

    def __init__(self, size, link):
        self.available_space = size
        self.link = link
        self.queue = Queue.Queue()
        self.logger = None

    def set_logger(self, logger):
        self.logger = logger
        self.logger.log_link_buffer_available_space(self.link.identifier, self.available_space)

    """Places a packet in the buffer, or drops the packet if no space is available."""
    def put(self, packet, destination):
        if self.available_space >= packet.size:
            self.queue.put((packet, destination))
            self.available_space -= packet.size
            self.logger.log_link_buffer_available_space(self.link.identifier, self.available_space)
        # Otherwise, drop the packet
        else:
            self.logger.log_link_dropped_packet_buffer_full(self.link.identifier, packet)

    """Retrieves the next packet from the buffer in FIFO order."""
    def get(self):
        (packet, destination) = self.queue.get_nowait()
        self.available_space += packet.size
        self.logger.log_link_buffer_available_space(self.link.identifier, self.available_space)
        return (packet, destination)

class Link:
    """A network link between two Devices.

    Attributes:
        identifier: The unique identification of the link
        rate: The rate at which the link sends packets in bytes per second
        delay: The transmission delay between ends of the link in ms
        buffer: The Buffer storing packets
        deviceA: instance of Device
        deviceB: instance of Device
        busy: true when the link is actively transmitting
        event_scheduler: reference to global event scheduler
        logger: the Logger used by the link
    """

    def __init__(self, identifier, rate, delay, buffer_size, deviceA, deviceB):
        self.identifier = identifier
        self.rate = rate
        self.delay = delay
        self.buffer = Buffer(buffer_size, self)
        self.deviceA = deviceA
        self.deviceB = deviceB
        self.busy = False
        self.event_scheduler = None
        self.logger = None

    def __str__(self):
        return ("Link ID   " + self.identifier + "\n"
                "rate:     " + str(self.rate) + " bytes/s\n"
                "delay:    " + str(self.delay) + " ms\n"
                "buffer:   " + str(self.buffer.available_space) + " bytes\n"
                "device A: " + self.deviceA.identifier + "\n"
                "device B: " + self.deviceB.identifier) + "\n"

    def set_logger(self, logger):
        self.logger = logger
        self.buffer.set_logger(logger)

    """Given a device attached to this link, returns the other device attached to the link."""
    def other_device(self, device):
        if device == self.deviceA:
            return self.deviceB
        elif device == self.deviceB:
            return self.deviceA
        else:
            sys.exit("Device {0} not attached to link {1}".format(device.identifier, self.identifier))

    """Send a packet from one sender attached to the link to the other sender attached."""
    # Sends a packet instantly if the link is not busy
    # or enqueues the packet in the buffer if the link is busy
    def send_packet(self, packet, sender):

        # The recipient is whatever device is not the sender
        recipient = self.other_device(sender)

        # Place in buffer if busy, otherwise send now
        if not self.busy:
            self._send_packet_now(packet, recipient)
            self.logger.log_link_sent_packet_immediately(self.identifier, packet)
        else:
            self.buffer.put(packet, recipient)

    # Called internally to send a packet by scheduling the relevant events
    def _send_packet_now(self, packet, recipient):
        assert not self.busy
        self.busy = True

        sending_delay = packet.size / self.rate
        self.event_scheduler.delay_event(sending_delay + self.delay, PacketArrivalEvent(packet, recipient, self))
        self.event_scheduler.delay_event(sending_delay, LinkReadyEvent(self))

    """Send a packet from the buffer, if possible."""
    # Called by LinkReadyEvent when the link is no longer busy
    def wake(self):
        self.busy = False
        try:
            # If there are any packets in the buffer, send one
            (packet, destination) = self.buffer.get()
            self._send_packet_now(packet, destination)
            self.logger.log_link_sent_packet_from_buffer(self.identifier, packet)
        except Queue.Empty:
            pass
