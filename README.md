Author: 
Bradley T. Martin, University of Arkansas
E-mail: btm002@email.uark.edu

Python 2.7 Script to add a population map to a structure file.
By default, it uses the first four letters of each sample name to designate populations.
However, the user can specify a range of characters for the popID search pattern (e.g., 2-5).

The popID characters to use as the search pattern can be specified with -s (start) and -e (end).
-s and -e are command-line arguments.


Usage: ./str2popmap.py -f INFILE

Optional arguments:

[-o OUTFILE (string); default = out.str] 
[-s STARTCHAR (integer); default = 1] 
[-e ENDCHAR (integer); default = 4]


