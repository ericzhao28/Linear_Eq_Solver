"""
FILE: parsing.py
Functions for parsing strings and files
for variable assignments.
"""

from . import FormatError

import re


def parse_file(fname):
    """
    Generator for parsed lines from a file at fname.
    :param fname: string-like obj pointing to file.
    :returns:
        Generator yielding outputs from parse_equation.
        Raises FormatError if invalid format and
        FileNotFoundError or IsADirectoryError if
        fname is invalid.
    """

    with open(fname, "r") as f:
        for i, line in enumerate(f.readlines()):
            if not line.strip():
                continue
            if line[:2].strip() == "//":
                continue
            try:
                yield parse_equation(line)
            except ValueError:
                raise FormatError("Invalid format on %s line %d" % (fname, i))


def parse_equation(eq_str):
    """
    Parses a string holding an equation of form: x = a + 3 + b + c.
    Balances variables to RHS and constants to LHS.
    :param eq_str: string-like obj holding the equation.
    :returns:
        var_coeff: dictionary mapping each variable to its coefficient
                   when balanced to the RHS.
        total_constant: total integer value on the LHS.
        Raises an assertion error if the eq_str is not valid.
    """

    def format_assert(condition):
        if not condition:
            raise ValueError()

    # Coefficients of variables if LHS moved to RHS.
    # Ex: (x = a + 3 + b + b) -> {x: -1, a = 1, b = 2}
    var_coeffs = {}
    # Sum of constant values on the RHS.
    total_constant = 0

    eq_parts = eq_str.split("=")
    format_assert(len(eq_parts) == 2)
    lhs = eq_parts[0].strip().split("+")
    rhs = eq_parts[1].strip().split("+")

    # Ensure one alphanumeric variable exists on LHS.
    format_assert(len(lhs) == 1)
    format_assert(lhs[0].isalpha())
    var_coeffs[lhs[0]] = -1

    # Parse RHS for constant values and more coeffs.
    for token in rhs:
        token = token.strip()
        if token.isalpha():
            if token not in var_coeffs:
                var_coeffs[token] = 0
            var_coeffs[token] += 1
        else:
            try:
                total_constant += int(token)
            except ValueError:
                format_assert(False)

    return var_coeffs, total_constant
