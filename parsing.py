import json
from link import Link
from flow import Flow
from host import Host
from router import Router
from simulation import Simulation
from congestion_controller import CongestionControllerReno, CongestionControllerFast

BYTES_PER_KILOBYTE = 1024
BYTES_PER_MEGABYTE = 1048576
BYTES_PER_MEGABIT = 131072

def read_testcases():
    with open('testcases.json') as testcases_file:
        return json.load(testcases_file)

def generate_simulation_from_testcase(input_dict):
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
        link = Link(l["id"], l["rate"] * BYTES_PER_MEGABIT, l["delay"], l["buffer"] * BYTES_PER_KILOBYTE, deviceA, deviceB)
        deviceA.attach_link(link)
        deviceB.attach_link(link)
        links[l["id"]] = link
    
    testcase_num = input_dict["testcase_num"];
    generate_routing_table(testcase_num, routers, links)

    flows = {}
    for f in flows_info:
        source_id = f["source"]
        destination_id = f["destination"]
        source = hosts.get(source_id)
        destination = hosts.get(destination_id)
        controller = CongestionControllerReno()
        flow = Flow(f["id"], source, destination, f["amount"] * BYTES_PER_MEGABYTE, f["start"], controller)
        controller.flow = flow
        flows[f["id"]] = flow
        source.flow = flow

    return Simulation(links, flows, hosts, routers, True) # verbose

def generate_routing_table(testcase_num, routers, links):
    if (testcase_num == 1):
        routers["R1"].add_table_entry("H1", links.get("L0"))
        routers["R1"].add_table_entry("H2", links.get("L1"))
        routers["R2"].add_table_entry("H1", links.get("L1"))
        routers["R2"].add_table_entry("H2", links.get("L3"))
        routers["R3"].add_table_entry("H1", links.get("L2"))
        routers["R3"].add_table_entry("H2", links.get("L4"))
        routers["R4"].add_table_entry("H1", links.get("L4"))
        routers["R4"].add_table_entry("H2", links.get("L5"))
    elif (testcase_num == 2):
        routers["R1"].add_table_entry("T1", links.get("L1"))
        routers["R1"].add_table_entry("T2", links.get("L1"))
        routers["R1"].add_table_entry("S1", links.get("L4"))
        routers["R1"].add_table_entry("S2", links.get("L5"))
        
        routers["R2"].add_table_entry("T1", links.get("L2"))
        routers["R2"].add_table_entry("T2", links.get("L6"))
        routers["R2"].add_table_entry("S1", links.get("L1"))
        routers["R2"].add_table_entry("S2", links.get("L1"))
        
        routers["R3"].add_table_entry("T1", links.get("L3"))
        routers["R3"].add_table_entry("T3", links.get("L3"))
        routers["R3"].add_table_entry("S1", links.get("L2"))
        routers["R3"].add_table_entry("S3", links.get("L7"))
        
        routers["R4"].add_table_entry("T1", links.get("L8"))
        routers["R4"].add_table_entry("T3", links.get("L9"))
        routers["R4"].add_table_entry("S1", links.get("L3"))
        routers["R4"].add_table_entry("S3", links.get("L3"))
