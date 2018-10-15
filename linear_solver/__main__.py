"""
FILE: __main__.py
Handles direct linear_solver call from CLI.
"""

import sys
import logging

from .parsing import parse_file
from .solver import calc_vars
from . import FormatError


def main():
    # Print usage if necessary.
    if len(sys.argv) < 2:
        logging.info("Usage: python -m linear_solver filename.txt")
        sys.exit(1)

    # Parse equations file.
    try:
        eqs = list(parse_file(sys.argv[1]))
    except FormatError as e:
        logging.error("FormatError:", e)
        sys.exit(1)
    except (FileNotFoundError, IsADirectoryError):
        logging.error("File %s could not be opened." % sys.argv[1])
        sys.exit(1)

    # Calculate assignments.
    try:
        assignments = calc_vars(eqs)
    except ValueError as e:
        logging.error("ValueError:", e)
        with open(sys.argv[1], "r") as f:
            print(f.read())
        sys.exit(1)
    except FormatError as e:
        logging.error("FormatError:", e)
        sys.exit(1)

    # Return assignments.
    for key in sorted(assignments.keys()):
        print("%s = %d" % (key, assignments[key]))


# Redundant but for explicicity
if __name__ == "__main__":
    main()
