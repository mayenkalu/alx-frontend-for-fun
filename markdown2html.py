#!/usr/bin/python3

"""
Markdown script using python.
"""
import sys
import os.path

if __name__ == '__main__':
    # Check if the number of arguments is less than 2
    if len(sys.argv) < 3:
        print('Usage: {} <input_file> <output_file>'.format(
            sys.argv[0]), file=sys.stderr)
        exit(1)

    # Get the input and output file names from the command-line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the input file exists
    if not os.path.isfile(input_file):
        print('Missing {}'.format(input_file), file=sys.stderr)
        exit(1)

    # Exit with a success status code
    exit(0)
