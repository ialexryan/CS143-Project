import sys
import argparse
import stats
from parsing import read_testcase, generate_simulation_from_testcase

parser = argparse.ArgumentParser(description='Simulate a network.')
parser.add_argument('-v', '--verbose', action="store_true", dest="verbose", default=False, help="increase verbosity")
parser.add_argument('-r', '--reno', action="store_false", dest="fast_insteadof_reno", default=False, help="TCP Reno (default)")
parser.add_argument('-f', '--fast', action="store_true", dest="fast_insteadof_reno", default=False, help="TCP Fast")
parser.add_argument('-n', '--no-graphs', action="store_false", dest="show_graphs", default=True, help="don't display graphs")
parser.add_argument('testcase_file', action="store", type=argparse.FileType('r'))
results = parser.parse_args()

sim = generate_simulation_from_testcase(read_testcase(results.testcase_file), results.verbose, results.fast_insteadof_reno)
sim.run()
print "Generating graphs..."
if results.show_graphs:
    stats.show_graphs(sim.logger)
