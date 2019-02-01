#!/usr/bin/env python3

import sys

import circuit.circuit as circ
from circuit.cnf import SatVar, Solver, Solution, Cnf
from circuit.circuit import Circuit
from transform import transform

# Implementation hints:
#
# 1) You need to build a *miter circuit* (or rather a miter CNF) in order to
#    compare the two circuits. For the circuit part, you can just use the
#    transform function from Exercise 2 (make sure to use different prefixes
#    for the two circuits, as they will usually have overlapping variable
#    names).
#
# 2) Make sure you cover the following error conditions:
#    * The two circuits have different number of inputs or outputs
#    * The inputs and outputs of the two circuits do not have the same names
#    In these cases you can return (False, None).
#
# 3) Run the test script to see if your code works!

def check(c1: Circuit, c2: Circuit) -> (bool, Solution):
    '''The function check() takes two Circuits as input and performs an equivalence
    check using a SAT solver. it returns a tuple, where the first entry is a
    Boolean value (True for equivalent, False for different) and the second
    value is -- in case of a difference found -- a Solution to the underlying
    SAT problem, representing a counterexample. If the circuits are indeed
    equivalent, the second entry will be None.

    '''

    # TODO: implement me
    pass

