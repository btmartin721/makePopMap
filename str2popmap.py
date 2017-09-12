#!/usr/bin/env python

import argparse
import re
import sys
import os.path

# Uses argparse library to parse command-line arguments; argparse must be imported
def Get_Arguments():

    parser = argparse.ArgumentParser(description="Adds PopMap to structure file based on sample IDs")
    
    parser.add_argument("-f", "--file", type=str, required=True, help="Input filename")
    parser.add_argument("-o", "--outfile", type=str, required=False, 
                        help="Output filename; Default = out.str", nargs="?", default="out.str")
    parser.add_argument("-c", "--char", type=int, required=False, nargs="?", default="4",
                        help="Specify the number of characters at beginning of sample ID that identify populations; default=4")
                        
    args = parser.parse_args()
    
    return args

# Reads a file line by line and returns as a list of lists
def read_infile(infile):

    check_if_exists(infile)
    whole_line = []
    with open(infile, "r") as fin:
        col = []
        for line in fin:
            line = line.rstrip("\r\n")
            columns = line.split()
            whole_line.append(line.strip().split())
            col.append(columns[0])
    
    return col, whole_line
	
# Gets the population identifier from sampleIDs in a column
# The first X letters of the string in the specified column are extracted
# Number of letters to extract is specified by the command-line flag -c	
def get_pop_identifier(input_list, numchar, found=None):

    if found is None:
        def found(x):
            return x
    
    hit = {}
    unique_ID = []
    temp_list = []    
    
    for item in input_list:
        temp_list = item[:numchar]
        marker = found(temp_list)
        
        if marker in hit:
            continue
        
        hit[marker] = 1
        
        unique_ID.append(temp_list)
        
    return unique_ID

# Function to count each popID and associate the count with the sampleID
def add_popID(uniqueIDs, sampleIDs, whole_line):
          
    popcount = 0
    for popcount, uniq in enumerate(uniqueIDs, 1):
        for sample in range(len(sampleIDs)):
            if re.match(uniq, sampleIDs[sample]):
                whole_line[sample].insert(1, str(popcount))
    
    return whole_line

# Writes the modified structure file
def insert_popID_2_file(listoflists, outfile):

    if os.path.isfile(outfile) == True:
        print("\nError: The file " + outfile + " already exists.\n")
        sys.exit(1)        
    
    with open(outfile, "a") as fout:
        for row in range(len(listoflists)):
            for col in range(len(listoflists[row])):
                fout.write(listoflists[row][col] + "\t")
        
            fout.write("\n")

# Test to make sure input file exists           
def check_if_exists(filename):

    try:
        file = open(filename, "r")
    except IOError:
        print("\nError: The file " + filename + " does not exist.\n")
        sys.exit(1)
          
    
################################################################################################################
##############################################    MAIN    ######################################################
################################################################################################################
    
# Gets command-line arguments using argparse; argparse must be imported
arguments = Get_Arguments()

# Reads a file line by line and returns as a list of lists
samples, whole_line = read_infile(arguments.file)


# Extracts the population identifier from sampleIDs in a column
# The first X letters (-c flag) of the string in the specified column are extracted
filter = get_pop_identifier(samples, arguments.char)

# Function to count each popID and associate the count with the sampleID
popID = add_popID(filter, samples, whole_line)

# Writes the modified structure file
insert_popID_2_file(popID, arguments.outfile)










