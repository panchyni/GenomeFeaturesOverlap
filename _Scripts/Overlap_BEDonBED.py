# IMPORTS
import sys
import OverlapFunctions as ov

# MAIN
print'''

Runs OverlapByIndexing pipeline on a pair of bedfiles

Takes a control file to specifie the arguments (see
BEDonBED.example.ctl) which should define the following:
   Ref = List of variables for the reference file
   Tar = List of variables for the target file
   Span = Span of the indexes in the overlap dict (in bp)
   LnOut = Name of the outfile reports the overlapping features
   NumOut = Name of the outfile reporting the # of overlaps per feature

'''

# Read arguments
ctl_file = sys.argv[1]
arg_dict = ov.ReadCtlFileForOverlap(ctl_file)

# Parse BED files
arg_dict["Ref"][0] = [ln.strip() for ln in open(arg_dict["Ref"][0],"r").readlines()] 
arg_dict["Tar"][0] = [ln.strip() for ln in open(arg_dict["Tar"][0],"r").readlines()]

# Run Overlap
[overlap_dict,sorted_keys] = ov.FindOverlapsByIndexing(arg_dict["Ref"],arg_dict["Tar"],arg_dict["Span"])

# Write Ouput
ov.WriteOverlapLines(overlap_dict,sorted_keys,arg_dict["LnOut"])
ov.WriteOverlapNumber(overlap_dict,sorted_keys,arg_dict["NumOut"])
