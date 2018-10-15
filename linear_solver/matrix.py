"""
FILE: matrix.py
Helper classes and functions for matrix representations.

Could just use Numpy instead of this but...
"""

import operator
import copy


class Matrix:
    def __init__(self, rows, check_dim=False):
        """
        Wrapper of 2d matrices stored as nested lists.
        :param rows:        list of Row objects.
        :param check_dim:   should row dimensions be validated.
        """
        if not rows:
            raise NotImplementedError("Empty matrices not supported.")
        self.rows = rows
        self.shape = (len(rows), len(rows[0]))
        if check_dim and any([len(r) != self.shape[1] for r in rows]):
            raise ValueError("Rows of inconsistent length.")

    def __repr__(self):
        return "[" + ",\n ".join([repr(r) for r in self.rows]) + "]"

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        yield from self.rows

    def __copy__(self):
        return Matrix([copy.copy(r) for r in self.rows])

    def __getitem__(self, key):
        # Allow standard index/slicing, but permit row objects
        # to be passed instead of integer indices.
        ind = lambda r: self.index(r) if isinstance(r, Row) else r
        if isinstance(key, slice):
            key = slice(ind(key.start), ind(key.stop), ind(key.step))
            return Matrix(
                [self.rows[i] for i in range(*key.indices(len(self.rows)))]
            )
        elif isinstance(key, int) or isinstance(key, Row):
            return self.rows[ind(key)]
        else:
            raise TypeError("Matrix indices must be integers or slices.")

    def __setitem__(self, key, value):
        ind = lambda r: self.index(r) if isinstance(r, Row) else r
        self.rows[ind(key)] = value

    def index(self, r):
        if not isinstance(r, Row):
            raise TypeError("Matrices only contain objects of type Row.")
        return self.rows.index(r)

    def swap(self, l_row, r_row):
        """
        Swap rows in this matrix.
        :param l_row: either row index or object in self.
        :param r_row: either row index or object in self.
        """
        ind = lambda r: self.index(r) if isinstance(r, Row) else r
        l = ind(l_row)
        r = ind(r_row)
        self.rows[l], self.rows[r] = self.rows[r], self.rows[l]


class Row:
    def __init__(self, values):
        """
        Wrapper of 2d matrices stored as nested lists.
        :param values:      list of values.
        """
        self.values = values.copy()

    def __repr__(self):
        return "[" + ", ".join([repr(v) for v in self.values]) + "]"

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        yield from self.values

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __neg__(self):
        return Row([-1 * v for v in self.values])

    def __copy__(self):
        return Row(self.values)

    def is_zero(self, epsilon=0.00001):
        return all([abs(v) < epsilon for v in self.values])

    def _piecewise_operator(self, operator, other):
        if isinstance(other, int) or isinstance(other, float):
            return Row([operator(float(v), other) for v in self])
        if isinstance(other, Row):
            return Row(
                [operator(float(v), float(w)) for v, w in zip(self, other)]
            )
        raise NotImplementedError(
            "Only row, row and row, constant operations supported."
        )

    def __mul__(self, other):
        return self._piecewise_operator(operator.mul, other)

    def __truediv__(self, other):
        return self._piecewise_operator(operator.truediv, other)

    def __add__(self, other):
        return self._piecewise_operator(operator.add, other)

    def __sub__(self, other):
        return self._piecewise_operator(operator.sub, other)


def get_rref(m):
    """
    Calculate reduced row echelon format.
    Mutates matrix m.
    :param m:  Matrix object to transform into rref.
    :returns:
        New Matrix object in rref form. Number of
        rows may have been changed.
    """
    # Get ref format.
    m = copy.copy(m)
    gauss_jordan(m)
    # Back substitutions.
    for i in range(m.shape[1] - 2, -1, -1):
        m[i] /= m[i][i]
        for j in range(0, i):
            m[j][-1] -= m[j][i] * m[i][-1]
            m[j][i] = 0

    return m[: m.shape[1] - 1]


def gauss_jordan(m, epsilon=0.00001):
    """
    Applies gauss jordan to transform matrix
    m into row echelon form. Mutates m.
    :param m:       Matrix object to be transformed into ref.
    :param epsilon: Float permitted precision error.
    :returns:
        None.
        Raises ValueError if rows are not linearly independent.
    """

    # Ensure dimensions permit linearly independence.
    if (m.shape[1] < 2) or (m.shape[0] < m.shape[1] - 1):
        raise ValueError()

    # Reduce rows from top->down, left->right.
    top_row_i = 0
    for col_i in range(m.shape[1] - 1):
        # Select row where column value is non-zero.
        max_row = max(m[top_row_i:], key=lambda x: abs(x[col_i]))
        if abs(max_row[col_i]) < epsilon:
            raise ValueError()
        # Move selected row to top.
        m.swap(max_row, m[top_row_i])
        # Reduce coefficients.
        top_row_i = m.index(max_row) + 1
        if top_row_i == len(m):
            return
        for child_row in m[top_row_i:]:
            m[child_row] -= max_row * child_row[col_i] / max_row[col_i]

    # Check if equations are contradictory.
    if not all([row.is_zero() for row in m[top_row_i:]]):
        raise ValueError()
