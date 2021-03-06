# IMPORT
import sys
import OverlapFunctions as over

# MAIN
print'''
 This is a test module for functions in  OverlapFunctions.py #

 Run with -v for more output

 Run with -n for no output

'''

# Set the enviroment
verbosity = 1
for i in range(len(sys.argv)):
    if sys.argv[i] == "-v":
        verbosity = 2
    if sys.argv[i] == "-n":
        verbosity = 0

test_lines1 = [ln.strip() for ln in open("GFF.test","r").readlines()]
test_lines2 = [ln.strip() for ln in open("SNP_positions.test","r").readlines()]

# Test UpdateSeqDict
seq_dict = {}
over.UpdateSeqDict(test_lines1,0,seq_dict)
over.UpdateSeqDict(test_lines2,0,seq_dict)
expected = [ln.split("\t")[0] for ln in test_lines1]
expected.extend([ln.split("\t")[0] for ln in test_lines2])
expected = list(set(expected))

if verbosity > 0:
    print "UpdateSeqDict Ran"

result = "Passed"
for seq in expected:
    if not seq in seq_dict.keys():
        results = "Failed"

if verbosity > 0:
    print "UpdateSeqDict: " + result

# Test SortPairedList
listA = [0,6,2,5,4,1,7,3]
listB = ['h','b','f','c','d','g','a','e']

[sortA,sortB] = over.SortPairedLists(listA,listB)

if verbosity > 0:
    print "SortPairedList Ran"

result = "Failed"
if sortA == [0,1,2,3,4,5,6,7] and sortB == ['h','g','f','e','d','c','b','a']:
   result = "Passed"

if verbosity > 0:
    print "SortPairedList: " + result
if verbosity > 1:
    print "\tResult: " + str(sortA) + " ; " + str(sortB)
    print "\tExpected: [0,1,2,3,4,5,6,7] ; [h,g,f,e,d,c,b,a]" 

# Test AddtoSeq
over.AddtoSeq([test_lines2,0,1],seq_dict)

if verbosity > 0:
    print "AddtoSeq Ran"

result = "Failed"
if 87 in seq_dict["chromosome_8"][0] and 194590 in  seq_dict["chromosome_1"][0] and 87 not in seq_dict["chromosome_8"][1]:
    result = "Passed"

if verbosity > 0:
    print "AddtoSeq: " + result

# Test BisectFeatures
bf_1 = over.BisectFeature(3,5,[sortA,sortB])
bf_2 = over.BisectFeature(3,3,[sortA,sortB])
bf_3 = over.BisectFeature(3,7,[sortA,sortB])
bf_4 = over.BisectFeature(3,5,[[1,2,3,4,5,5,5,5,6,7],['a','b','c','d','e','f','g','h','i','j']])
bf_5 = over.BisectFeature(3,7,[[1,2,3,4,5,6,7,7,7,7],['a','b','c','d','e','f','g','h','i','j']])

if verbosity > 0:
    print "BisectFeatures Ran"

result = "Failed"
if bf_1[1] == ['e', 'd', 'c'] and bf_2[1] == ['e'] and bf_3[1] ==  ['e', 'd', 'c', 'b', 'a'] and bf_4[1] == ['c', 'd', 'e', 'f', 'g', 'h'] and bf_5[1] == ['c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']:
    result = "Passed"

if verbosity > 0:
    print "BisectFeatures: " + result
if verbosity > 1:
      print "\tResult: " + str(bf_1) + " ; " + str(bf_2) + " ; " + str(bf_3) + " ; " + str(bf_4) + " ; " + str(bf_5)
      print "\tExpected: ['e', 'd', 'c'] ; ['e'] ; ['e', 'd', 'c', 'b', 'a'] ; ['c', 'd', 'e', 'f', 'g', 'h'] ; ['c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']"

# Test FindOverlapByBisection
[overlap_dict,sorted_keys] = over.FindOverlapByBisection([test_lines1[-20:-10],0,3,4],[test_lines2[-10:],0,1])

if verbosity > 0:
    print "FindOverlapByBisection Ran"

result = "Failed"
if overlap_dict[sorted_keys[4]][-2] == ('11070', '') and overlap_dict[sorted_keys[5]][-3] == ('17830', '') and overlap_dict[sorted_keys[5]][-2] == ('17860', ''):
    result = "Passed"   

if verbosity > 0:
    print "FindOverlapByBisection: " + result
if verbosity > 1:
    print "\tResult: " + str(overlap_dict[sorted_keys[4]][-2]) + " ; " + str(overlap_dict[sorted_keys[5]][-3]) + " ; " + str(overlap_dict[sorted_keys[5]][-2])
    print "\tExpected:  ('11070', '') ;  ('17830', '') ; ('17860', '')"
