#!/usr/bin/env python

import argparse
import re
import sys
import os.path

from datastruct import Struct

from collections import Counter

# Uses argparse library to parse command-line arguments; argparse must be imported
def Get_Arguments():

    parser = argparse.ArgumentParser(description="Adds PopMap to structure file based on sample ID patterns")

    parser.add_argument("-f", "--file", type=str, required=True, help="Input filename")
    parser.add_argument("-o", "--outfile", type=str, required=False,
                        help="Output filename; Default = out.str", nargs="?", default="out.str")
    parser.add_argument("-s", "--start", type=int, required=False, nargs="?", default="1",
                        help="Specify first character of sample ID to be used as pattern for population ID; default=1")
    parser.add_argument("-e", "--end", type=int, required=False, nargs="?", default="4",
                        help="Specify last character of sample ID to be used as pattern for population ID; default=4")

    args = parser.parse_args()

    return args

# Reads a file line by line and returns as a list of lists
def read_infile(line):



    line = line.rstrip("\r\n")
    ids_loci = line.strip().split(None, 1)
    ids = ids_loci[0]
    loc = ids_loci[1]


    return ids, loc

# Gets the population identifier from sampleIDs in a column
# The first X letters of the string in the specified column are extracted
# Characters to extract are specified by the command-line flags -s and -e	
def get_unique_identifiers(input_obj, startchar, endchar, found=None):

    if found is None:
        def found(string):
            return string

    hit = {}
    unique_ID = []

    for obj in input_obj:
        pattern = obj.id[startchar-1:endchar]
        marker = found(pattern)

        if marker in hit:
            continue

        hit[marker] = 1

        unique_ID.append(pattern)

    return unique_ID

# Function to count each popID and associate the count with the sampleID
def sum_popids(uniqueIDs, sampleIDs):

    for popcount, uniq in enumerate(uniqueIDs, 1):
        for sample in range(len(sampleIDs)):
            if re.search(uniq, sampleIDs[sample]):
                whole_line[sample].insert(1, str(popcount))

    #return whole_line

# Writes the modified structure file
def write_popID_2_file(listoflists, outfile):

    if os.path.isfile(outfile) == True:
        answer = raw_input("\nThe outfile " + outfile + " already exists. Do you wish to overwrite it [Y/N]?: ").upper()

        if answer.strip() == "Y" or answer.strip() == "YES":
            write_to_file(listoflists, outfile)

        elif answer.strip() == "N" or answer.strip() == "NO":
            print("\nOutfile not overwritten; program aborted.\n")
            sys.exit(1)

        else:
            answer = raw_input("\nError: Could not understand user input. Please answer with 'Y' or 'N', or type 'exit' to cancel: ").upper()
            if answer.strip() == "EXIT":
                print("\nProgram terminated by user\n")
                sys.exit(1)

            elif answer.strip() == "Y" or answer.strip() == "YES":
                write_to_file(listoflists, outfile)

            elif answer.strip() =="N" or answer.strip() =="NO":
                print("\nOutfile not overwritten; program aborted.\n")
                sys.exit(1)

            else:
                print("\nError: Could not understand user input; program aborted\n")
                sys.exit(1)

    else:
        write_to_file(listoflists, outfile)

# Test to make sure input file exists           
def check_if_exists(filename):

    try:
        file = open(filename, "r")
    except IOError:
        print("\nError: The file " + filename + " does not exist.\n")
        sys.exit(1)

def write_to_file(listoflists, file):

    with open(file, "w") as fout:
        for row in range(len(listoflists)):
            for col in range(len(listoflists[row])):
                fout.write(listoflists[row][col] + "\t")

            fout.write("\n")


################################################################################################################
##############################################    MAIN    ######################################################
################################################################################################################

# Gets command-line arguments using argparse; argparse must be imported
arguments = Get_Arguments()

# Reads a file line by line and returns as a list of lists
#samples, whole_line, numcols =
#data = []
check_if_exists(arguments.file)

samples = []
samp_dict = {}
id_set = set()

with open(arguments.file, "r") as fin:
    for lines in fin:
        ids, loc = read_infile(lines)

        dataset = Struct(ids, loc)
        samples.append(dataset.id)
        id_set.add(dataset.id[arguments.start-1:arguments.end])
        patt = dataset.id[arguments.start-1:arguments.end]

        #if patt not in samp_dict:
            #samp_dict.update(patt)

#print(samp_dict)
# Extracts the population identifier from sampleIDs in a column
# The start (-s flag) to end (-e flag) characters of the string in the specified column are extracted
#unique_IDs = get_unique_identifiers(data_structure, arguments.start, arguments.end)

# Function to count each popID and associate the count with the sampleID
#popID =
#sum_popids(id_set, samples)

# Writes the modified structure file
#write_popID_2_file(popID, arguments.outfile)










