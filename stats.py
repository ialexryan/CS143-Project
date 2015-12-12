import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import Counter
from operator import itemgetter

BYTES_PER_KILOBYTE = 1024.0
BYTES_PER_MEGABYTE = 1048576.0
BYTES_PER_MEGABIT = 131072.0


def block_average(input_times, input_values):   # input_times in milliseconds, return times in seconds
    assert(len(input_times) == len(input_values))

    output_times = []
    output_values = []

    # add first data point
    output_times.append(input_times.pop(0) / 1000.0)
    output_values.append(input_values.pop(0))

    last_interval_start = 0;
    window_size = 100;   # milliseconds
    current_window_count = 0.0;
    current_window_total = 0;

    # add the rest of the averaged data points
    for i in range(len(input_times)):
        time = input_times[i]
        if time - last_interval_start > window_size:
            if current_window_count > 0:
                output_times.append((last_interval_start + (window_size / 2)) / 1000.0)
                output_values.append(current_window_total / current_window_count)
            current_window_count = 0.0
            current_window_total = 0
            last_interval_start += window_size
        current_window_count += 1
        current_window_total += input_values[i]

    # add last data point
    output_times.append(input_times[-1] / 1000.0)
    output_values.append(current_window_total / current_window_count)

    return (output_times, output_values)

def block_sum(input_times, input_values):
    assert(len(input_times) == len(input_values))

    output_times = []
    output_values = []

    last_interval_start = 0;
    window_size = 100;   # milliseconds
    current_window_total = 0;

    for i in range(len(input_times)):
        time = input_times[i]
        if time - last_interval_start > window_size:
            output_times.append((last_interval_start + (window_size / 2)) / 1000.0)
            output_values.append(current_window_total)
            current_window_total = 0
            last_interval_start += window_size
        current_window_total += input_values[i]

    return (output_times, output_values)


def display_free_buffers_space(logger, num_plots, index):
    plt.subplot(num_plots / 2 + 1, 2, index)

    graphs = {}  # keys are link_id, values are [(time, available_space)]
    for log in logger.link_buffer_available_space_logs:
        graphs.setdefault(log["link_id"], []).append((log["time"], log["available_space"] / BYTES_PER_KILOBYTE))
    for link_id, link_data in graphs.iteritems():
        times, spaces = [list(c) for c in zip(*link_data)]  # convert [(time, available_space)] to [time] and [available_space]
        x, y = block_average(times, spaces)
        plt.plot(x, y, label=link_id)
    plt.xlabel("time, seconds")
    plt.ylabel("free buffer space, KB")
    plt.xlim(xmin=0)
    plt.ylim(ymin=0)
    plt.legend(loc='lower left', fontsize=8, ncol=3, fancybox=True)

def display_amounts_left(logger, num_plots, index):
    plt.subplot(-(-num_plots // 2), 2, index)
    graphs = {}  # keys are flow_id, values are [(time, amount_left)]
    for log in logger.flow_received_acknowledgement_logs:
        graphs.setdefault(log["flow_id"], []).append((log["time"], log["amount_left"] / BYTES_PER_MEGABYTE))
    for flow_id, flow_data in graphs.iteritems():
        times, remaining = [list(c) for c in zip(*flow_data)]   # convert [(time, amount_left)] to [time] and [amount_left]
        x, y = block_average(times, remaining)
        plt.plot(x, y, label=flow_id)
    plt.xlabel("time, seconds")
    plt.ylabel("amount left to transmit, MB")
    plt.xlim(xmin=0)
    plt.ylim(ymin=0)
    plt.legend(loc='upper right', fontsize=8, fancybox=True)

def display_packet_round_trip_time(logger, num_plots, index):
    plt.subplot(-(-num_plots // 2), 2, index)

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
    plt.xlim(xmin=0)
    plt.ylim(ymin=0)
    plt.legend(loc="center right", fontsize=8, fancybox=True)

def display_dropped_packets(logger, num_plots, index):
    sp = plt.subplot(-(-num_plots // 2), 2, index)

    graphs = {}  # keys are link_id/router_id, values are [(time, num_dropped)]
    for log in logger.router_dropped_packet_unknown_path_logs:
        graphs.setdefault(log["router_id"], []).append((log["time"], 1))
    for log in logger.router_sending_packet_logs:
        if log["router_id"] in graphs:  # we only want to log unlost packets for links/routers that lost some packets
            graphs[log["router_id"]].append((log["time"], 0))
    for log in logger.link_dropped_packet_buffer_full_logs:
        graphs.setdefault(log["link_id"], []).append((log["time"], 1))
    for log in logger.link_sent_packet_immediately_logs + logger.link_sent_packet_from_buffer_logs:
        if log["link_id"] in graphs:  # we only want to log unlost packets for links/routers that lost some packets
            graphs[log["link_id"]].append((log["time"], 0))

    for dropper_id, dropper_data in graphs.iteritems():
        dropper_data.sort(key=itemgetter(0))   # sort by time
        times, drops = [list(c) for c in zip(*dropper_data)]  # convert [(time, num_dropped)] to [time] and [num_dropped]
        x, y = block_average(times, drops)
        plt.plot(x, y, label=dropper_id)
    plt.xlabel("time, seconds")
    plt.ylabel("fraction of packets dropped")
    plt.xlim(xmin=0)
    # sp.yaxis.set_major_locator(MaxNLocator(integer=True))  # only show integer y-axis ticks
    plt.legend(loc="upper right", fontsize=8, fancybox=True)

def display_link_rate(logger, num_plots, index):
    sp = plt.subplot(-(-num_plots // 2), 2, index)

    graphs = {}  # keys are link_id, values are [(time, bytes_sent)]
    for log in logger.link_sent_packet_immediately_logs + logger.link_sent_packet_from_buffer_logs:
        graphs.setdefault(log["link_id"], []).append((log["time"], log["packet"].size))

    for dropper_id, dropper_data in graphs.iteritems():
        dropper_data.sort(key=itemgetter(0))   # sort by time
        times, bytes_sent = [list(c) for c in zip(*dropper_data)]  # convert [(time, bytes_sent)] to [time] and [bytes_sent]
        x, y = block_sum(times, bytes_sent)
        y = [i * 10 / BYTES_PER_MEGABIT for i in y]  # Convert the graph from bytes/100ms to Mb/s
        plt.plot(x, y, label=dropper_id)
    plt.xlabel("time, seconds")
    plt.ylabel("Mb/s")
    plt.xlim(xmin=0)
    # sp.yaxis.set_major_locator(MaxNLocator(integer=True))  # only show integer y-axis ticks
    plt.legend(loc="lower center", fontsize=8, ncol=3, fancybox=True)

graph_functions = [display_free_buffers_space, display_amounts_left, display_packet_round_trip_time, display_dropped_packets, display_link_rate]

def show_graphs(logger):
    i = 1
    num_plots = len(graph_functions)
    for f in graph_functions:
        f(logger, num_plots, i)
        i += 1
    fig = plt.gcf()
    fig.canvas.set_window_title("TCP Fast" if logger.fast_insteadof_reno else "TCP Reno")
    plt.show()
