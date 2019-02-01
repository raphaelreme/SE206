#!/usr/bin/env python3

import sys

import circuit.circuit as circ
from circuit.cnf import SatVar, Solver, Cnf
from circuit.circuit import Circuit

# Implementation hints:
#
# 1) For all inputs, outputs, and named signals of the circuit, it is
#    required that the variable names in the CNF are the same as the
#    signal names, i.e. after solving the CNF, it must be possible to
#    obtain the assignment of a circuit signal by indexing the
#    solution with the signal name: a = solution['a']. The variable
#    names for any other internal nodes can be chosen freely.  If a
#    prefix is given, then all variable names must begin with this
#    prefix.
#
# 2) In order to implement the transformation, you will need to
#    traverse the circuit graph for all outputs (and named internal
#    signals). Make sure that you do not forget any of the defined
#    node types. Check the file circuit.py to find out about the
#    possible node types. You can use the function node.getID() in
#    order to obtain a unique identifier for a node.
#
# 3) Test your code! There is a test script named test.py. If your
#    code passes all the tests, there is a good chance that it is
#    correct.

def transform(c: Circuit, prefix: str='') -> Cnf:
    '''The function transform takes a Circuit c and returns a Cnf obtained by the
    Tseitin transformation of c. The optional prefix string will be used for
    all variable names in the Cnf.

    '''

    # TODO: implement me
    pass

