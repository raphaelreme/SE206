#!/usr/bin/env python3

import circuit.circuit as circ
from circuit.cnf import SatVar, Solver, Cnf

# circ full_adder {
#      inputs: a, b, cin
#      outputs: s, cout
#      s0 = a ^ b
#      s = s0 ^ cin
#      cout = (a & b) | (s0 & cin)
# }

# Inputs
a = SatVar('a')
b = SatVar('b')
cin = SatVar('cin')

# Outputs
s = SatVar('s')
cout = SatVar('cout')

# Internal variables (if needed)
s0 = SatVar('s0')
s1 = SatVar('s1')
s2 = SatVar('s2')


def mk_or(s, a, b):
    """Take 2 inputs a, b and 1 output s. Return the cnf of the gate s <=> a | b"""
    return (a | b | ~s) & (s | ~a) & (s | ~b)

def mk_and(s, a, b):
    """Take 2 inputs a, b and one output s. Return the cnf of the gate s <=> a & b"""
    return (~a | ~b | s) & (~s | a) & (~s | b)

def mk_xor(s, a, b):
    """Take 2 inputs a, b and 1 output s. Return the cnf of the gate s <=> a ^ b"""
    return (~s | a | b) & (~s | ~a | ~b) & (s | ~a | b) & (s | a | ~b)

def mk_not(s, a):
    """Take 1 inputs a and 1 output s. Return the cnf of the gate s <=> ~a"""
    return (s | a) & (~s | ~a)

def mk_eq(s, a):
    """Take 1 inputs a and 1 output s. Return the cnf of the gate s <=> a"""
    return (s | ~a) & (~s | a)

def mk_adder():
    return mk_xor(s0, a, b) & mk_xor(s, cin, s0) & mk_and(s1, a, b) & mk_and(s2, cin, s0) & mk_or(cout, s1, s2)

def solve():
    """Return a solution to the adder cnf.
    A solution is just a hint that the output is well defined (that there is no contradiction in the circuit)"""
    return Solver().solve(mk_adder())
