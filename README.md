# GenomeFeaturesOverlap
Python functions and scripts for finding overlap between genomic features files in different formats

#Overview:
1. The folder "_Functions" contains modules defining basic functions for the pipeline
  * For the sake of simplicity, all generic functions are currently contained in "OverlapFunctions.pyc"
  * Functions in this file are divided as follows include:
    1. Indexed Overlapping Functions
    2. Bisect Overlap Functions
    3. Generic Utility Functions
2. The folder "_Parsers" contains scripts for pasrsing non-generic files into a tab-delimited format

   Note: Parser functions should not be written for "generic" feature folder, defined here as any table seperated
   by a common delimeter. Parsers should be written for specific non-tabular or exotic tables that require a unique
   praser to be process. Examples of this include *.wig files or pre-processing a *.gff file to extract a value 
   from the information string

3. The folder "_Scripts" contains scritps for running overlaps between certains standard genome-feature file types

   Note: Also included in this folder are example control files
