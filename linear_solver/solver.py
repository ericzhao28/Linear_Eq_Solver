"""
FILE: solver.py
Linear equation solver. Assuming LHS is a single variable,
variable coefficients are always 1, all constants are positive
integers, and addition is the only operator.
"""

from .matrix import Matrix, Row, get_rref
from . import FormatError


def calc_vars(eq_generator):
    """
    Computes a list of variable values for a set of equations.
    :param eq_generator: generates tuples of shape ({v: -1...}, 9)
                         that correspond to variable coefficients and the
                         constant of a linear equation balanced s.t.
                         all variables are on the RHS and constants on
                         the LHS.
                         e.g. v = 9 + b -> ({v: -1, b: 1}, -9)
    :returns:
        Dictionary of variable assignments (eg {v: 4, b: 5})
        Raises ValueError(...) in case of invalid file format or
        lack of linear independence.
    """

    # Load variable coefficients and constant values into a matrix rep.
    seen_vars = []
    eqs = []
    for var_coeffs, constant in eq_generator:
        eqs.append([0 for _ in range(len(seen_vars) + 1)])
        eqs[-1][0] = -1 * constant
        for var, val in sorted(var_coeffs.items()):
            if var not in seen_vars:
                seen_vars.append(var)
                for eq in eqs:
                    eq.append(0)
            eqs[-1][seen_vars.index(var) + 1] = val
    eqs = [eq[1:] + [eq[0]] for eq in eqs]

    if not eqs:
        raise FormatError("No equations provided.")

    # Test linear independence and compute solution:
    m = Matrix([Row(r) for r in eqs], True)
    try:
        m = get_rref(m)
        var_vals = [r[-1] for r in m]
    except ValueError as e:
        raise ValueError("Equations are not linearly independent.") from e

    # Recorrelate var_vals w/ original variable names.
    return {seen_vars[i]: v for i, v in enumerate(var_vals)}
