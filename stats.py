import sys
import matplotlib.pyplot as plt

BYTES_PER_MEGABYTE = 1048576.0

def get_times(logs):
    t = []
    for log in logs:
        t.append(log["time"] / 1000)
    return t

def display_total_buffer_space(logger, size, index):
    plt.subplot(size, 1, index)
    x = get_times(logger.link_buffer_available_space_logs)
    y = []
    for log in logger.link_buffer_available_space_logs:
        y.append(log["available_space"])
    plt.plot(x, y, "ro")
    plt.xlabel("time, seconds")
    plt.ylabel("total free buffer space, bytes")

def display_total_amount_left(logger, size, index):
    plt.subplot(size, 1, index)
    graphs = {}  # keys are flow_id, values are [(time, amount_left)]
    for log in logger.flow_received_acknowledgement_logs:
        graphs.setdefault(log["flow_id"], []).append((log["time"] / 1000, log["amount_left"] / BYTES_PER_MEGABYTE))
    for flow_id, flow_data in graphs.iteritems():
        times = []
        remaining = []
        for d in flow_data:
            times.append(d[0])
            remaining.append(d[1])
        plt.plot(times, remaining, label=flow_id)
    plt.xlabel("time, seconds")
    plt.ylabel("total amount left to transmit, MB")
    plt.legend(loc='upper right')

def display_packet_round_trip_time(logger, size, index):
    plt.subplot(size, 1, index)

    # The tricky bit here is that we have to account for sending
    # the same packet id multiple times in the case of dropped packets.
    # Packet ID's are also not unique across flows, so we use (packet_id, flow_id) as
    # a unique(ish, see first sentence) identifier.

    trips = {}  # keys are (packet_id, flow_id)'s, values are [start, finish] times
    for log in logger.flow_received_acknowledgement_logs:
        k = (log["packet"].identifier, log["packet"].flow_id)
        # We should only ever receive an ack packet once
        assert(k not in trips)
        trips[k] = [143143143143, log["time"]]
    for log in logger.flow_send_packet_logs:
        # We might have sent a packet 179 times, but we only care about the first time
        k = (log["packet"].identifier, log["packet"].flow_id)
        assert(k in trips)
        if log["time"] < trips[k][0]:
            trips[k][0] = log["time"]
        assert(trips[k][0] != 143143143143)
        assert(trips[k][1] - trips[k][0] > 0)

    graphs = {}  # keys are flow_id, values are [(time, packet)]
    for log in logger.flow_received_acknowledgement_logs:
        graphs.setdefault(log["flow_id"], []).append((log["time"] / 1000, log["packet"]))
    for flow_id, flow_data in graphs.iteritems():
        if (flow_id) is "F1":
            continue
        times = []
        rtts = []
        for d in flow_data:
            trip = trips[(d[1].identifier, d[1].flow_id)]
            times.append(d[0])
            rtts.append(trip[1]-trip[0])
        plt.plot(times, rtts, label=flow_id)
    plt.xlabel("time, seconds")
    plt.ylabel("RTT, ms")
    plt.ylim(ymin=0)
    plt.legend(loc="upper left")


graph_functions = [display_total_buffer_space, display_total_amount_left, display_packet_round_trip_time]

def show_graphs(logger):
    i = 1
    size = len(graph_functions)
    for f in graph_functions:
        f(logger, size, i)
        i += 1
    plt.show()
