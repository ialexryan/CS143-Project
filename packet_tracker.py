import Queue

class PacketTracker:
    def __init__(self):
        self.next_packet = 0
        self.early_packets = Queue.PriorityQueue()

    def account_for_packet(self, packet_id):
        if packet_id == self.next_packet:
            self.next_packet += 1
            while not self.early_packets.empty() and self.next_packet == self.early_packets.queue[0]:
                self.next_packet += 1
                self.early_packets.get_nowait()
        elif packet_id > self.next_packet:
            self.early_packets.put(packet_id)
        else:
            pass
            #received packet again - do nothing
        return self.next_packet
