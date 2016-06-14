# IMPORT
import sys

# FUNCTIONS
# Note: Currently, there is only one pipeline to process .wig files, but the process
# has been broken into the following functions, allowing for future extension
#  -ReadWigtoDict(lines)
#  -WigDictToSeqDict(wig_dict)
#  -CondenseSeqDict(seq_dict)
#  -SeqDictForWriting(seq_dict) 
#  -WriteSeqDictToTable(seq_dict,outfile,sep="\t")

def ReadWigtoDict(lines):
    '''Reads a wig file into a dictionary

    Input:
         -lines = the lines from a wig file
    
    Output:
         -wig_dict = a dictonary of wig lines key by a tuple of chrom/start/step

    '''

    # Read lines into a dictionary
    wig_dict = {}
    key = "Dummy"
    key_values = []
    for ln in lines:
        
        # If it is annotation line
        if ln.startswith("fixedStep"):
            
            # Store previous set of lines
            wig_dict[key] = key_values
            key_values = []

            # Make a new key
            split_ln = ln.split(" ")
            chrom = [v.split("=")[1] for v in split_ln if v.split("=")[0] == "chrom"]
            start = [v.split("=")[1] for v in split_ln if v.split("=")[0] == "start"]
            step = [v.split("=")[1] for v in split_ln if v.split("=")[0] == "step"]
            
            key = (chrom[0],start[0],step[0])

        else:
            key_values.append(ln)

    # Add the last key and remove dummy variable
    wig_dict[key] = key_values
    del wig_dict["Dummy"]

    return wig_dict

def WigDictToSeqDict(wig_dict):
    ''' Takes a wig dictioanry and convert it a dictionary of position,value tuples 
    keyed by sequence/contig/chromosome

    Input:
         -wig_dict = a wig dictioanry from "ReadWigFiles"

    Output:
         -seq_dict a dictionary of postions and values keyed by sequencee
    
    '''

    seq_dict = {}
    for key in wig_dict.keys():
        # Parse sequence arguments out of the key
        [seq,start,step] = key
        start = int(start)
        step = int(step)
        values = wig_dict[key]
        
        # Assign a position to each value
        position_list = []
        for i in range(len(values)):
            position_list.append(start + i*step)

        # Update dictionary
        if seq in seq_dict.keys():
            seq_dict[seq][0].extend(position_list)
            seq_dict[seq][1].extend(values)
        else:
            seq_dict[seq] = [position_list,values]   

    return seq_dict

def CondenseSeqDict(seq_dict):
    '''Takes a seq_dict and condenses consecutive single position features
    with the same value to a single feature

    Input:
         -seq_dict = a seq dictionary from WigDictToSeqDict

    Output:
         -cond_dict = the dictionary of condense values keyed by sequence

    '''

    cond_dict = {}

    for seq in seq_dict.keys():
        [positions,values] = seq_dict[seq]

        # Sort values by position
        sort_positions = [s for (s,v) in sorted(zip(positions,values), key=lambda pair: pair[0])]
        sort_values = [v for (s,v) in sorted(zip(positions,values), key=lambda pair: pair[0])]

        # Define region with similar values
        regions = []

        start = sort_positions[0]
        current_value = sort_values[0]
        stop = sort_positions[0]

        for index in range(len(sort_positions[1:])):

            # Get the current position and value
            position = sort_positions[index+1]
            value = sort_values[index+1]

            # Compare value to current value
            if value == current_value:
                stop = position
            else:
                regions.append([start,stop,current_value])
                start = position
                stop = position
                current_value = value

        cond_dict[seq] = regions 

    return cond_dict

def SeqDictForWriting(seq_dict):
    '''Alter the a sequence dictionary for writing
 
    Input:
         -seq_dict = a seq_dict from "WigDictToSeqDict"
 
    Output:
         -seq_out_dict = a modified seq_dict ready for writing by "WriteSeqDictToTable"

    '''
 
    seq_out_dict = {}
    for key in seq_dict.keys():
        [positions,values] = seq_dict[key]

        # Pair and sort
        sort_pairs = [(s,v) for (s,v) in sorted(zip(positions,values), key=lambda pair: pair[0])]

        # Pair and the sorted values and add to dict
        seq_out_dict[key] = sort_pairs

    return seq_out_dict
        

def WriteSeqDictToTable(seq_dict,outfile,sep="\t"):
    ''' Write the features of a seq_dict to a table

    Input:
         -seq_dict = a seq_dict from "SeqDictForWriting" and "CondenseSeqDict"
         -outfile = the name of the outfile which the table will be written to

    Optional:
         -sep = the seperator character for columns in the outfile
    
    Output:
         -Writes results to a file

    '''

    outlines = []
    for key in seq_dict.keys():
        base_line = key + sep
        outlines.extend([base_line + sep.join([str(i) for i in feature]) + "\n" for feature in seq_dict[key]])
    output = open(outfile,"w")
    output.write("".join(outlines))
    output.close()

# MAIN

print'''

Parses a *.wig file into a table

Takes the following inputs:
    -infile = input wig file
    -outfile = root name of the output table file (Optional,default=infile)
    -sep = seperator charecter for the table file (Optional,default="\t")
    -positional = output a table of positions (seq,position) instead of regions (seq,start,stop) (Optional,default=False)

'''

# Read parameters
infile = ""
outfile = ""
sep = "\t"
positional = False
for i in range(len(sys.argv)):
    if sys.argv[i] == "-infile":
        infile = sys.argv[i+1]
    if sys.argv[i] == "-outfile":
        outfile = sys.argv[i+1]
    if sys.argv[i] == "-sep":
        sep =  sys.argv[i+1]
    if sys.argv[i] == "-positional":
        positional =  bool(sys.argv[i+1])

if outfile == "":
    outfile = infile

# Check parameters
try:
   lines = [ln.strip() for ln in open(infile,"r").readlines()]
except IOError as e:
   print "Error: Missing input *.wig file"
   raise e

# Parse wig lines and write output
wig_dict = ReadWigtoDict(lines)
seq_dict = WigDictToSeqDict(wig_dict)

# Define output based on "positional" flag
if positional == True:
    outfile = outfile + ".positional.out"
    seq_out_dict = SeqDictForWriting(seq_dict)
    WriteSeqDictToTable(seq_out_dict,outfile,sep)
elif positional == False:
    outfile = outfile + ".regions.out"
    cond_dict = CondenseSeqDict(seq_dict)
    WriteSeqDictToTable(cond_dict,outfile,sep)
else:
    print "Unreognized value " + str(positional) + " for positional flag"
