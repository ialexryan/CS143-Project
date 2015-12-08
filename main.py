import sys
import argparse
from parsing import read_testcases, generate_simulation_from_testcase

parser = argparse.ArgumentParser(description='Simulate a network.')
parser.add_argument('-v', action="store_true", dest="verbose", default=False)
parser.add_argument('-r', action="store_false", dest="fast_insteadof_reno", default=False)
parser.add_argument('-f', action="store_true", dest="fast_insteadof_reno", default=False)
parser.add_argument('testcase_id', action="store", type=int)

results = parser.parse_args()

testcase = read_testcases()[results.testcase_id]
sim = generate_simulation_from_testcase(testcase, results.verbose, results.fast_insteadof_reno)
sim.run()
