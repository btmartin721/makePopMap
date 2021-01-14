#!/usr/bin/env python

import argparse
import sys

from datastruct import Struct

# Uses argparse library to parse command-line arguments; argparse must be imported
def Get_Arguments():

    parser = argparse.ArgumentParser(description="Adds PopMap to structure file based on sample ID patterns"
                                                "Also can generate a popmap file from multiple input types."
                                                "Population IDs can be integers or characters.")

    required_args = parser.add_argument_group("required arguments:\n")
    required_args.add_argument("-f", "--file", type=str, required=True, help="Input filename")
    parser.add_argument("-o", "--outfile", type=str, required=False,
                        help="Output filename; Default = out.txt", nargs="?", default="out.txt")
    parser.add_argument("-s", "--start", type=int, required=False, nargs="?", default="1",
                        help="Specify first character of sample ID to be used as pattern for population ID; default=1")
    parser.add_argument("-e", "--end", type=int, required=False, nargs="?", default="4",
                        help="Specify last character of sample ID to be used as pattern for population ID; default=4")
    parser.add_argument("-p", "--popmap", action="store_true", help="Boolean; Just writes a popmap to file;"
                        "default is to add the popmap to the input file.\n")
    parser.add_argument("-t", "--phylip", action="store_true", help="Boolean; Specifies PHYLIP input/output file")
    parser.add_argument("-a", "--admixture", action="store_true", help="Boolean; Specifies .ped input/output file")
    parser.add_argument("-c", "--chars", action="store_true", help="Boolean; outputs population pattern instead of integer")
    parser.add_argument("-i", "--ignore_case", action="store_true", help="Boolean; Ignore case in setting populations")
    parser.add_argument("-u", "--underscore", action="store_true", help="Boolean; Use first underscore to get population pattern")
    args = parser.parse_args()

    return args

# Reads a file line by line and returns as a list of lists
def read_infile(line):

    line = line.rstrip("\r\n")
    ids_loci = line.strip().split(None, 1)
    ids = ids_loci[0]
    loc = ids_loci[1]

    return ids, loc

# Gets population identifiers and adds 1 if ID is not already in dictionary
# Returns popID number
def get_unique_identifiers(pattern, hit, number):

    if not hit:
        dataset.make_dict(number, hit, pattern)

    elif pattern not in hit:
        number += 1
        dataset.make_dict(number, hit, pattern)

    return number

# Check to make sure input file exists or else die
def check_if_exists(filename):

    try:
        file = open(filename, "r")
    except IOError:
        print("\nError: The file " + filename + " does not exist.\n")
        sys.exit(1)

def make_popmap(sample, pop):

    fout.write(str(sample) + "\t" + str(pop) + "\n")

def check_if_phylip(infile):

    f = open(infile, "r")
    first_line = f.readline()

    first_line = first_line.rstrip()
    cols = first_line.split()
    nInd = cols[0].strip()
    nLoci = cols[1].strip()

    f.close()

    if len(cols) == 2 and nInd.isdigit() and nLoci.isdigit():
        is_phylip = "phylip"
    else:
        is_phylip = "not_phylip"

    return is_phylip


################################################################################################################
##############################################    MAIN    ######################################################
################################################################################################################
# Gets command-line arguments using argparse; argparse must be imported
arguments = Get_Arguments()

# Check if input file exists; if not, die
check_if_exists(arguments.file)

unique_ids = {}

popnum = 1

file_type = check_if_phylip(arguments.file)

with open(arguments.file, "r") as fin:
    with open(arguments.outfile, "w") as fout:

        if arguments.phylip and file_type == "not_phylip":
            print("\n\nError: [-t] option requires phylip formatted infile\n\n")
            sys.exit(1)

        if file_type == "phylip":
            header = fin.readline()

        if arguments.phylip and not arguments.popmap:
            fout.write(str(header))

        linenum = 0
        for lines in fin:
            linenum += 1
            ids, loc = read_infile(lines)
            # Object to hold data structure: dataset.id = sample IDs, dataset.loci = all loci
            dataset = Struct(ids, loc)

            if arguments.underscore:
                try:
                    underscore_pos = dataset.id.index("_")
                    patt = dataset.id[arguments.start-1:underscore_pos]
                except ValueError:
                    print("Error on line " + str(linenum) + ": missing underscore when -u option was used.")
                    sys.exit(1)
            else:
                # pattern = characters arguments.start to arguments.end in dataset.id
                patt = dataset.id[arguments.start-1:arguments.end]

            if arguments.ignore_case:
                patt = patt.upper()

            popnum = get_unique_identifiers(patt, unique_ids, popnum)  # Returns popID and adds 1 for each unique ID

            popid = unique_ids[patt]   # dictionary with unique ids (key), popID (value)

            if arguments.admixture and not arguments.popmap:
                # Writes popIDs to file in .ped format
                fout.write(str(patt) + "\t" + str(dataset.loci) + "\n")

            elif arguments.admixture and arguments.popmap:
                # If popmap flag: Writes PopMap file only
                make_popmap(dataset.id, popid)

            elif arguments.popmap and arguments.chars:
                # Writes popmap with regex pattern for popID instead of integers
                make_popmap(dataset.id, str(patt))

            elif arguments.phylip and not arguments.popmap and arguments.chars:
                fout.write(dataset.id + "\t" + str(patt) + "\t" + dataset.loci + "\n")

            elif not arguments.phylip and not arguments.popmap and arguments.chars:
				fout.write("{}\t{}\t{}\n".format(dataset.id, patt, dataset.loci))

            elif arguments.popmap:
                # if -p flag: Only writes two-column popmap to file
                make_popmap(dataset.id, popid)

            else:
                # Write STRUCTURE file with popIDs inserted
                fout.write(str(dataset.id) + "\t" + str(popid) + "\t" + str(dataset.loci) + "\n")
