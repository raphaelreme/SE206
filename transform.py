#!/usr/bin/env python3

import sys

import circuit.circuit as circ
from circuit.cnf import SatVar, Solver, Cnf
from circuit.circuit import Circuit
from adder import *

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



def f(node, prefix = ''):
    cnf = Cnf()

    children = node.getChildren()
    if type(node).__name__ == "Variable":
        s = SatVar(prefix+node.getName())
        return s, cnf

    s = SatVar(prefix+ "s" + str(node.getID()))
    if type(node).__name__ == "Literal":
        if (node.getValue()):
            cnf = cnf & s
        else:
            cnf = cnf & ~s
        return s, cnf

    if type(node).__name__ == "BinOp":
        a, cnf1 = f(node.getChild(0), prefix)
        b, cnf2 = f(node.getChild(1), prefix)
        cnf = cnf & cnf1 & cnf2
        if (node.getOp() == "&"):
            cnf = cnf & mk_and(s, a, b)
        elif (node.getOp() == "^"):
            cnf = cnf & mk_xor(s, a, b)
        elif (node.getOp() == "|"):
            cnf = cnf & mk_or(s, a, b)
        else:
            raise ValueError("Unrecognized operator " + node.getOp())
        return s, cnf

    if type(node).__name__ == "UnOp":
        a, cnf1 = f(node.getChild(0), prefix)
        cnf = cnf & cnf1
        if (node.getOp() == "~"):
            cnf = cnf & mk_not(s, a)
        else:
            raise ValueError("Unrecognized operator " + node.getOp())
        return s, cnf

def transform(c: Circuit, prefix: str='') -> Cnf:
    '''The function transform takes a Circuit c and returns a Cnf obtained by the
    Tseitin transformation of c. The optional prefix string will be used for
    all variable names in the Cnf.
    '''

    cnf = Cnf()
    for keys in c.getSignals():
        s = SatVar(prefix+keys)
        node = c.getEquation(keys)

        children = node.getChildren()

        if type(node).__name__ == "Variable":
            a = SatVar(prefix+node.getName())
            cnf = cnf & mk_eq(s, a)

        if type(node).__name__ == "Literal":
            if (node.getValue()):
                cnf = cnf & s
            else:
                cnf = cnf & ~s

        if type(node).__name__ == "BinOp":
            a, cnf1 = f(node.getChild(0), prefix)
            b, cnf2 = f(node.getChild(1), prefix)
            cnf = cnf & cnf1 & cnf2
            if (node.getOp() == "&"):
                cnf = cnf & mk_and(s, a, b)
            elif (node.getOp() == "^"):
                cnf = cnf & mk_xor(s, a, b)
            elif (node.getOp() == "|"):
                cnf = cnf & mk_or(s, a, b)
            else:
                raise ValueError("Unrecognized operator " + node.getOp())


        if type(node).__name__ == "UnOp":
            a, cnf1 = f(node.getChild(0), prefix)
            cnf = cnf & cnf1
            if (node.getOp() == "~"):
                cnf = cnf & mk_not(s, a)
            else:
                raise ValueError("Unrecognized operator " + node.getOp())

    return cnf
