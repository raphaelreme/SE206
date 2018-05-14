#!/usr/bin/env python3

import sys

import circuit.circuit as circ
from circuit.cnf import SatVar, Solver


def transform(c):

    # TODO: implement me
    pass

# ================================================================= TEST CODE

if __name__ == '__main__':

    adder = circ.parse('examples/fa.crc')
    cnf = transform(adder)
    print (cnf)
    
