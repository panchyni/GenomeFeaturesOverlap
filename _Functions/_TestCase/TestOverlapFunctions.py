# IMPORT
import sys
import OverlapFunctions as over

# MAIN
print'''
 This is a test module for functions in OverlapFunctions.py 

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

test_lines1 = [ln.strip() for ln in open("aligned_blocks.bed.test","r").readlines()]
test_lines2 = [ln.strip() for ln in open("head_regions.test","r").readlines()]
span = 10000

# Test FindSeqMax
seq_max_dict = {}
over.FindSeqMax(test_lines1,0,2,seq_max_dict)

if verbosity > 0:
    print "FindSeqMax Ran"

result = "Failed"
if seq_max_dict['Chr1'] == 28393285 and seq_max_dict['Chr3'] == 19612773 and seq_max_dict['Chr5'] == 23748651:
    result = "Passed"

if verbosity > 0:
    print "FindSeqMax: " + result
if verbosity > 1:
    print "\tResult: " + str(seq_max_dict)
    print "\tExpexted: {'Chr5': 23748651, 'Chr4': 7634614, 'Chr3': 19612773, 'Chr2': 11160619, 'Chr1': 28393285}"

# Test IndexSequences
seq_index_dict = over.IndexSequences(seq_max_dict,span)

if verbosity > 0: 
    print "IndexSequences Ran"

result = "Passed"
try:
   test1 = seq_index_dict["Chr1"]["28390000_28400000"]
   test2 = seq_index_dict["Chr1"]["0_10000"]
   test3 = seq_index_dict["Chr5"]["23740000_23750000"]
except:
    result = "Failed"

if verbosity > 0:
    print "IndexSequences: " + result

# Test Get Indexes
indexes = over.GetIndexes(143500,1567000,span)

if verbosity > 0:
    print "GetIndexes Ran"

result = "Failed"
if "140000_150000" in indexes and "1560000_1570000" in indexes and "610000_620000" in indexes:
    result = "Passed"

if verbosity > 0:
    print "GetIndexes: " + result

# Test AddtoIndex
over.AddToIndex([test_lines1,0,1,2],seq_index_dict,span)

if verbosity > 0:
    print "AddToIndex Ran"

result = "Failed"
if ("20875055","20875554","Ps007391") in seq_index_dict["Chr5"]["20870000_20880000"] and ("17143007","17143506","Ps007364") in seq_index_dict["Chr1"]["17140000_17150000"]:
    result = "Passed"

if verbosity > 0:
    print "AddToIndex: " + result
if verbosity > 1:
    print "\tResult: " + str(seq_index_dict["Chr5"]["20870000_20880000"])
    print "\tResult: " + str(seq_index_dict["Chr1"]["17140000_17150000"])
    print "\tExpected: set([('20875055', '20875554', 'Ps007391')])"
    print "\tExpected: set([('17143007', '17143506', 'Ps007364')])"

# Test TestOverlap
should_be_true = over.TestOverlap(100,400,200,500)
should_be_false = over.TestOverlap(100,200,300,400)
should_be_true_hard = over.TestOverlap(100,400,400,500)
should_be_false_hard = over.TestOverlap(100,399,400,500)

if verbosity > 0:
    print "TestOverlap Ran"

result = "Failed"
if should_be_true == True and should_be_false == False and should_be_true_hard == True and should_be_false_hard == False:
    result = "Passed"

if verbosity > 0:
    print "TestOverlap: " + result
if verbosity > 1:
    print "\tEasy True Test: " + str(should_be_true)
    print "\tEasy False Test: " + str(should_be_false)
    print "\tHard True Test: " + str(should_be_true_hard)
    print "\tHard False Test: " + str(should_be_false_hard)

# Test FindOverlapsByIndexing
ref = [test_lines1,0,1,2]
target = [test_lines2,0,1,2]
[overlap_dict,sorted_keys] = over.FindOverlapsByIndexing(ref,target,span)

if verbosity > 0:
    print "FindOverlapsByIndexing Ran"

result = "Failed"
if overlap_dict[("Chr1","3631","4130",0)][0] == "AT1G01010" and overlap_dict[("Chr1","3631","4130",0)][1] == ("3631","4130","AT1G01010") and sorted_keys[-1] == ("Chr5","20875055","20875554",101):
    result = "Passed"

if verbosity > 0:
    print "FindOverlapsByIndexing: " + result
if verbosity > 1:
    print "\tResult: " + str(overlap_dict[("Chr1","3631","4130",0)])
    print "\tResult: " + str(sorted_keys[-1])
    print "\tExpected: ['AT1G01010', ('3631', '4130', 'AT1G01010'), 1]" 
    print "\tExpected: ('Chr5', '20875055', '20875554',101)"
