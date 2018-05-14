#!/usr/bin/env python3

import sys

import circuit.circuit as circ
from circuit.cnf import SatVar, Solver

def check(c1, c2):

    # TODO: implement me
    pass

# ================================================================= TEST CODE

if __name__ == '__main__':

    adder1 = circ.parse('examples/fa.crc')
    adder2 = circ.parse('examples/fa2.crc')
    adder3 = circ.parse('examples/fa3.crc')
    adder4 = circ.parse('examples/fa4.crc')  # faulty adder

    # These should be equivalent
    assert (check(adder1, adder2))
    assert (check(adder2, adder3))
    assert (check(adder1, adder3))

    # Those aren't
    assert (not check(adder1, adder4))
    assert (not check(adder2, adder4))
    assert (not check(adder3, adder4))

    carry_ripple = circ.parse('examples/cra8.crc')
    
    # And this one is completely different
    assert (not check(adder1, carry_ripple))

    
