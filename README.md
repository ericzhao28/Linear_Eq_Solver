# Equation evaluator
A command-line program to evaluate a set of linear equations.

Author: Eric Zhao

Dependencies:
* Python 3+
* No external libraries

## Usage
Call the linear_solver module directly on a file of your choice: `python3 -m linear_solver tests/10\ 5.txt`
Alternatively, run `./run_tests`.
A `Dockerfile` is also provided for convenience. Run: `docker run $(docker build . -q)`.

### Input file format
An equation is defined by:
`<LHS> = <RHS>`

* Each equation is specified on a separate line.
* `<LHS>` is the left-hand side of the equation and is always a variable name.
* A variable name is composed of letters from the alphabet ( for which isalpha(c) is true ).
* `<RHS>` is the right hand side of the equation and can be composed of:
* variables
* unsigned integers
* the + operator

Here is one example set of equations:
```
offset = 4 + random + 1
location = 1 + origin + offset
origin = 3 + 5
random = 2
```

## Program Structure
I implemented a 2d matrix class in place of numpy in `matrix.py`. This wraps a list of Row objects (which are in themselves wrappers of lists). I added basic element-wise arithmetic and row swapping to support my Gaussian elimination logic. Below my class declarations, I include an implementation of Gauss-jordan elimination for obtaining a matrix's row echelon form and a wrapper that obtains a reduced row echelon form. Equation-solving-specific logic is in `solver.py`.
File and equation parsing is presented through a generator from `parser.py`.
The code for supporting command line usage is under the module's `__main__` while logger initialization can be found in `__init__`.



