import sys
from parsing import read_testcases, generate_simulation_from_testcase

if len(sys.argv) == 1:
    print "Please provide a test case number"
    exit()
if len(sys.argv) > 2:
    print "Too many commandline arguments"
    exit()
if int(sys.argv[1]) not in [0, 1, 2]:
    print "We don't have a test case with that number"
    exit()

testcase_num = int(sys.argv[1])
testcase = read_testcases()[testcase_num]
sim = generate_simulation_from_testcase(testcase)
sim.run()
