import json
from link import Link
from flow import Flow
from host import Host
from router import Router
from simulation import Simulation
from congestion_controller import CongestionControllerReno, CongestionControllerFast

BYTES_PER_KILOBYTE = 1024.0
BYTES_PER_MEGABYTE = 1048576.0
BYTES_PER_MEGABIT = 131072.0

def read_testcase(file):
    return json.load(file)

def generate_simulation_from_testcase(input_dict, verbose, fast_insteadof_reno):
    links_info = input_dict["links"]
    flows_info = input_dict["flows"]
    hosts_info = input_dict["hosts"]
    routers_info = input_dict["routers"]

    # This is where we actually create all our objects for this simulation
    hosts = {}
    for h in hosts_info:
        hosts[h["id"]] = Host(h["id"])

    routers = {}
    for r in routers_info:
        routers[r["id"]] = Router(r["id"])

    links = {}
    for l in links_info:
        deviceA_id = l["endpoints"][0]
        deviceB_id = l["endpoints"][1]
        deviceA = [ d.get(deviceA_id) for d in [hosts, routers] if deviceA_id in d ][0]
        deviceB = [ d.get(deviceB_id) for d in [hosts, routers] if deviceB_id in d ][0]
        link = Link(l["id"], l["rate"] * BYTES_PER_MEGABIT / 1000, l["delay"], l["buffer"] * BYTES_PER_KILOBYTE, deviceA, deviceB)
        deviceA.attach_link(link)
        deviceB.attach_link(link)
        links[l["id"]] = link

    flows = {}
    for f in flows_info:
        source_id = f["source"]
        destination_id = f["destination"]
        source = hosts.get(source_id)
        destination = hosts.get(destination_id)
        controller = CongestionControllerFast() if fast_insteadof_reno else CongestionControllerReno()
        flow = Flow(f["id"], source, destination, f["amount"] * BYTES_PER_MEGABYTE, f["start"] * 1000, controller)
        controller.flow = flow
        flows[f["id"]] = flow
        source.flows[f["id"]] = flow

    return Simulation(links, flows, hosts, routers, verbose, fast_insteadof_reno) # verbose
