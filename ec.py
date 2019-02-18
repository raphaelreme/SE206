#!/usr/bin/env python3

import sys

import circuit.circuit as circ
from circuit.cnf import SatVar, Solver, Solution, Cnf
from circuit.circuit import Circuit
from transform import transform
from adder import *

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

    if not (c1.getInputs() == c2.getInputs() and c1.getOutputs() == c2.getOutputs()):
        return (False, None)

    cnf1 = transform(c1, "c1_")
    cnf2 = transform(c2, "c2_")

    cnf = cnf1 & cnf2

    # Inputs should be the same.
    # Mitter_input isn't necessary. (Only here to preserve the name of the entree. Easier to get along with)
    for input in c1.getInputs():
        mitter_input = SatVar(input)
        c1_input = SatVar("c1_" + input)
        c2_input = SatVar("c2_" + input)
        cnf = cnf & mk_eq(mitter_input, c1_input) & mk_eq(mitter_input, c2_input)

    outputs = list(c1.getOutputs())
    n = len(outputs)
    s = SatVar("mitter_output")

    # Computation of the mitter output :
    # Xor of the outputs of the Circuits
    # Then an or of all these xor (as we only have made a binary_or function, we do as many or as needed)
    #
    # The code would be simplier if a 1 Litteral were added to always make a binary or, even when there only is one xor
    # But it would be less efficient.
    if n == 1:
        c1_output = SatVar("c1_" + outputs[0])
        c2_output = SatVar("c2_" + outputs[0])
        cnf = cnf & mk_xor(s, c1_output, c2_output)
    else:
        for i, output in enumerate(outputs):
            c1_output = SatVar("c1_" + output)
            c2_output = SatVar("c2_" + output)
            xor_output = SatVar("mitter_xor_" + output)
            cnf = cnf & mk_xor(xor_output, c1_output, c2_output)

            if i == 1:
                ith_or = SatVar("mitter_or_1")
                if i + 1 == n:
                    ith_or = s

                xor_prev = SatVar("mitter_xor_" + outputs[0]) # = [i-1]

                cnf = cnf & mk_or(ith_or, xor_prev, xor_output)
            if i>1:
                ith_or = SatVar("mitter_or_" + str(i))
                if i + 1 == n:
                    ith_or = s

                or_prev = SatVar("mitter_or_" + str(i-1))
                cnf = cnf & mk_or(ith_or, or_prev, xor_output)


    cnf = cnf & s

    solution = Solver().solve(cnf)

    if not solution:
        return (True, None)
    else:
        return (False, solution.assignment)
