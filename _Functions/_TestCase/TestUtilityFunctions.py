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

control_file = "test.ctl"

# Test ReadCtlFileForOverlap
argument_dict = over.ReadCtlFileForOverlap(control_file)

if verbosity > 0:
    print "ReadCtlFileForOverlap Ran"

result = "Failed"
if argument_dict['Ref'] == ["aligned_blocks.bed.test","0","1","2"] and argument_dict['Span'] == 10000 and argument_dict['Aux'] == 'Test':
    result = "Passed"

if verbosity > 0:
    print "ReadCtlFileForOverlap " + result
if verbosity > 1:
    print "\tResult: " + str(argument_dict)
    print "\tExpected:  {'Span': 10000, 'Ref': ['aligned_blocks.bed.test', '0', '1', '2'], 'Tar': ['head_regions.test', '0', '1', '2'], 'Aux': 'Test'}"

# Test WriteOverlapLines
argument_dict['Ref'][0] = [ln.strip() for ln in open(argument_dict['Ref'][0],"r").readlines()]
argument_dict['Tar'][0] = [ln.strip() for ln in open(argument_dict['Tar'][0],"r").readlines()]
[overlap_dict,sorted_key] = over.FindOverlapsByIndexing(argument_dict['Ref'],argument_dict['Tar'],argument_dict['Span'])
over.WriteOverlapLines(overlap_dict,sorted_key,"test.out")

if verbosity > 0:
    print "FindOverlapsByIndexing Ran"

result = "Failed"
outlines = [ln.strip() for ln in open("test.out","r").readlines()]
if outlines[0].split("\t")[0] == "Chr1" and outlines[3].split("\t")[1:4] == ["5928","6427","AT1G01020"] and outlines[4].split("\t")[4:] == ["11649","12148","AT1G01030"]:
    result = "Passed"

if verbosity > 0:
    print "WriteOverlapLines " + result
if verbosity > 1:
    print "\tResult: " + str(outlines[0].split("\t")[0]) + " " + str(outlines[3].split("\t")[1:4]) + " " + str(outlines[4].split("\t")[4:])
    print "\tExpected: Chr1 [5928,6427,AT1G01020] [11649,12148,AT1G01030] "

# Test WriteOverlapNumber
over.WriteOverlapNumber(overlap_dict,sorted_key,"numb.out")

if verbosity > 0:
    print "WriteOverlapNumber Ran"

result = "Failed"
outlines = [ln.strip() for ln in open("numb.out","r").readlines()]
if outlines[0].split("\t")[0] == "Chr1" and outlines[3].split("\t")[1:3] == ["5928","6427"] and outlines[4].split("\t")[3:] == ["AT1G01030","1"]:
    result = "Passed"

if verbosity > 0:
    print "WriteOverlapLines " + result
if verbosity > 1:
    print "\tResult: " + str(outlines[0].split("\t")[0]) + " " + str(outlines[3].split("\t")[1:3]) + " " + str(outlines[4].split("\t")[3:])
    print "\tExpected: Chr1 [5928,6427] [AT1G01030,1]"

# Test KeepLines 
gff_lines = [ln.strip() for ln in open("GFF.test","r").readlines()]

filter_gff_lines = over.FilterLines(gff_lines,[0,2,3,4,8])

if verbosity > 0:
    print "FilterLines Ran"

result = "Failed"
if filter_gff_lines[0] == "chromosome_10\tgene\t3314\t5025\tID=Cre10.g417426.v5.5;Name=Cre10.g417426" and filter_gff_lines[-1] == "chromosome_9\tgene\t53436\t57227\tID=Cre09.g386161.v5.5;Name=Cre09.g386161":
    result = "Passed"

if verbosity > 0:
    print "FilterLines " + result
if verbosity > 1:
    print "\tResult: " + str(filter_gff_lines[0]) + "\t " + str(filter_gff_lines[-1])
    print "\tExpected: chromosome_10\tgene\t3314\t5025\tID=Cre10.g417426.v5.5;Name=Cre10.g417426 \n chromosome_9\tgene\t53436\t57227\tID=Cre09.g386161.v5.5;Name=Cre09.g386161 "

# Test WriteOverlapLines with Bisect
ref_lines = [ln.strip() for ln in open("GFF.test","r").readlines()]
tar_lines = [ln.strip() for ln in open("SNP_positions.test","r").readlines()]
[overlap_dict,sorted_key] = over.FindOverlapByBisection([ref_lines,0,3,4],[tar_lines,0,1])
over.WriteOverlapLines(overlap_dict,sorted_key,"bisect_test.out")

if verbosity > 0:
    print "WriteOverlapLines with Bisect Ran"

result = "Failed"
outlines = [ln.strip() for ln in open("bisect_test.out","r").readlines()]
if outlines[0].split("\t")[0:3] == ["chromosome_10","3314","5025"] and outlines[1].split("\t")[3] == "phytozomev10,gene,.,-,.,ID=Cre10.g417450.v5.5;Name=Cre10.g417450" and outlines[2].split("\t")[4:] == ["NA","NA"]:
    result = "Passed"

if verbosity > 0:
    print "WriteOverlapLines with Bisect " + result
if verbosity > 1:
    print "\tResult: " + str(outlines[0].split("\t")[0:3]) + " " + str(outlines[1].split("\t")[3]) + " " + str(outlines[2].split("\t")[4:])
    print "\tExpected ['chromosome_10','3314','5025'] phytozomev10,gene,.,-,.,ID=Cre10.g417450.v5.5;Name=Cre10.g417450 ['NA','NA']"
