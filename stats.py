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

    trips = {}  # keys are (packet_id, flow_id)'s, values are ack times
    for log in logger.flow_received_acknowledgement_logs:
        trips[(log["packet"].identifier, log["packet"].flow_id)] = log["time"]
    for log in logger.flow_send_packet_logs:
        # just kidding, now the values are RTT's
        assert((log["packet"].identifier, log["packet"].flow_id) in trips)
        trips[(log["packet"].identifier, log["packet"].flow_id)] -= log["time"]
        assert(trips[(log["packet"].identifier, log["packet"].flow_id)] > 0)

    graphs = {}  # keys are flow_id, values are [(time, packet)]
    for log in logger.flow_received_acknowledgement_logs:
        graphs.setdefault(log["flow_id"], []).append((log["time"] / 1000, log["packet"]))
    for flow_id, flow_data in graphs.iteritems():
        if (flow_id) is "F1":
            continue
        times = []
        rtts = []
        for d in flow_data:
            rtt = trips[(d[1].identifier, d[1].flow_id)]
            times.append(d[0])
            rtts.append(rtt)
        plt.plot(times, rtts, label=flow_id)
    plt.xlabel("time, seconds")
    plt.ylabel("RTT, ms")
    plt.ylim(ymin=0)
    plt.legend(loc="upper right")


graph_functions = [display_total_buffer_space, display_total_amount_left, display_packet_round_trip_time]

def show_graphs(logger):
    i = 1
    size = len(graph_functions)
    for f in graph_functions:
        f(logger, size, i)
        i += 1
    plt.show()
