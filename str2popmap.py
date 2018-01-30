#!/usr/bin/env python

import argparse
import sys

from datastruct import Struct

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
def get_unique_identifiers(pattern, hit, number):

    if not hit:
        hit[pattern] = number


    elif pattern not in hit:
        number += 1
        hit[pattern] = number

    return number

# Check to make sure input file exists or die
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

# Check if input file exists; if not, die
check_if_exists(arguments.file)

unique_ids = {}

popnum = 1

with open(arguments.file, "r") as fin, open(arguments.outfile, "w") as fout:

    for lines in fin:
        ids, loc = read_infile(lines)

        # Object to hold data structure: dataset.id = sample IDs, dataset.loci = all loci
        dataset = Struct(ids, loc)
        patt = dataset.id[arguments.start-1:arguments.end]

        popnum = get_unique_identifiers(patt, unique_ids, popnum)  # Returns popID

        popid = unique_ids[patt]   # dictionary with unique ids (key), popID (value)

        # Write modified file structure with popIDs inserted
        fout.write(str(dataset.id) + "\t" + str(popid) + "\t" + str(dataset.loci) + "\n")
