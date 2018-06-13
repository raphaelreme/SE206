#!/usr/bin/env python3

import circuit.circuit as circ
from circuit.cnf import SatVar, Solver

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


def mk_adder():
    
    # TODO: Construct CNF for full adder
    return None


# ================================================================= TEST CODE

if __name__ == '__main__':
    cnf = mk_adder()
    adder = circ.parse('benchmarks/fa.crc')
    print (cnf)

    if cnf is None:
        print ("CNF is empty (None). Go do something about it...")
        exit (1)

    # Function to constrain CNF with input conditions
    def constrain(cnf, test):
        def constr(x):
            return SatVar(x) if test[x] else ~SatVar(x)
        return cnf & constr('a') & constr('b') & constr('cin')        

    # Functions to display test cases
    def head():
        print ("a b cin | cout s")
        print ("--------+-------")
    red = '\033[31m'
    green = '\033[32m'
    normal = '\033[0m'
    def row(sim, sat):
        r =  "%i %i  %i  |   " % (sim['a'], sim['b'], sim['cin'])
        good = True
        complete = True
        if (not sat):
            r += red + '-  -' + normal + ' [UNSAT]'
        else:
            if not ('cout' in sat.keys()):
                r += red
                r += '-  '
                complete = False
            elif sim['cout'] == sat['cout']:
                r += green
                r += '%i  ' % sim['cout']
            else:
                r += red
                r += '%i  ' % sim['cout']
                good = False
            if not ('s' in sat.keys()):
                r += red
                r += '-'
                complete = False
            elif sim['s'] == sat['s']:
                r += green 
            else:
                r += red
                good = False
            r += '%i' % sim['s'] + normal
            if not good:
                r += ' [wrong outputs]'
            if not complete:
                r += ' [incomplete solution]'
        print (r)
    
    # test all input conditions
    B = [False, True]
    tests = [{'a':a, 'b':b, 'cin':c} for a in B for b in B for c in B]
    solver = Solver()
    head()
    for test in tests:
        sim = adder.simulate(test)        
        sat = solver.solve(constrain(cnf, test))
        row(sim, sat)
