"""
FILE: __init__.py
Linear Solver.
We assume the left hand side (LHS) is a single
variable, variable coefficients are always 1, all constants are positive
integers, and addition is the only operator.
"""

import logging

logging.getLogger().setLevel(50)


class FormatError(Exception):
    """ Custom error for erronous input format. """

    pass
