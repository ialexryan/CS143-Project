import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import Counter

BYTES_PER_MEGABYTE = 1048576.0


def block_average(input_times, input_values):   # input_times in milliseconds
    assert(len(input_times) == len(input_values))

    output_times = []
    output_values = []

    last_interval_start = 0;
    window_size = 50;   # milliseconds
    current_window_count = 0;
    current_window_total = 0;
    for i in range(len(input_times)):
        time = input_times[i]
        current_window_count += 1
        current_window_total += input_values[i]
        if time - last_interval_start > window_size:
            output_times.append((time - (window_size / 2)) / 1000.0)
            output_values.append(current_window_total / current_window_count)
            current_window_total = 0
            current_window_count = 0
            last_interval_start = time
    return (output_times, output_values)

def display_total_buffer_space(logger, size, index):
    plt.subplot(size, 1, index)
    time = []
    space = []
    for log in logger.link_buffer_available_space_logs:
        time.append(log["time"])
        space.append(log["available_space"])
    x, y = block_average(time, space)
    plt.plot(x, y)
    plt.xlabel("time, seconds")
    plt.ylabel("total free buffer space, bytes")
    plt.title("100ms average of total free buffer space")

def display_total_amount_left(logger, size, index):
    plt.subplot(size, 1, index)
    graphs = {}  # keys are flow_id, values are [(time, amount_left)]
    for log in logger.flow_received_acknowledgement_logs:
        graphs.setdefault(log["flow_id"], []).append((log["time"], log["amount_left"] / BYTES_PER_MEGABYTE))
    for flow_id, flow_data in graphs.iteritems():
        times = []
        remaining = []
        for d in flow_data:
            times.append(d[0])
            remaining.append(d[1])
        x, y = block_average(times, remaining)
        plt.plot(x, y, label=flow_id)
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
        # assert(k not in trips)
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
        graphs.setdefault(log["flow_id"], []).append((log["time"], log["packet"]))
    for flow_id, flow_data in graphs.iteritems():
        times = []
        rtts = []
        for d in flow_data:
            trip = trips[(d[1].identifier, d[1].flow_id)]
            times.append(d[0])
            rtts.append(trip[1]-trip[0])
        x, y = block_average(times, rtts)
        plt.plot(x, y, label=flow_id)
    plt.xlabel("time, seconds")
    plt.ylabel("RTT, ms")
    plt.title("100ms average of RTT time per flow")
    plt.ylim(ymin=0)
    plt.legend(loc="lower right")

def display_dropped_packets(logger, size, index):
    sp = plt.subplot(size, 1, index)

    graphs = {}  # keys are link_id/router_id, values are [time]
    for log in logger.link_dropped_packet_buffer_full_logs:
        graphs.setdefault(log["link_id"], []).append(log["time"] / 1000.0)
    for log in logger.router_dropped_packet_unknown_path_logs:
        graphs.setdefault(log["router_id"], []).append(log["time"] / 1000.0)
    for flow_id, flow_data in graphs.iteritems():
        c = Counter(flow_data)  # keys are times, values are number of dropped packets
        plt.plot(c.keys(), c.values(), "o", label=flow_id)
    plt.xlabel("time, seconds")
    plt.ylabel("# of dropped packets")
    sp.yaxis.set_major_locator(MaxNLocator(integer=True))  # only show integer y-axis ticks
    plt.legend(loc="upper right")

graph_functions = [display_total_buffer_space, display_total_amount_left, display_packet_round_trip_time, display_dropped_packets]

def show_graphs(logger):
    i = 1
    size = len(graph_functions)
    for f in graph_functions:
        f(logger, size, i)
        i += 1
    fig = plt.gcf()
    fig.canvas.set_window_title("TCP Fast" if logger.fast_insteadof_reno else "TCP Reno")
    plt.show()
