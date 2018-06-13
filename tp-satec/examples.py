#!/usr/bin/env python3

import sys
import random

import circuit.circuit as circ
from circuit.cnf import SatVar, Solver



# ===================================== Loading and simulating circuits
print ("===============================")

# Load and simulate full adder circuit
try:
    fa = circ.parse('benchmarks/fa.crc')
except Exception as e:
    print ("[INF] Could not load circuit. Good bye!")
    raise e    

# Write circuit graph to file
with open('fa.dot', 'w') as f:
    f.write(fa.dot())

inputs = dict()
print ("{:^3}{:^3}{:^4}|{:^4}{:^3}".format('a','b','cin','cout','s'))
print ("-" * 10 + "+" + "-" * 8)
for i in range(8):

    # Convert i to a vector of Booleans
    bits = [b ==  '1' for b in format(i, '03b')]

    # Assign inputs
    inputs['a'] = bits[0]
    inputs['b'] = bits[1]
    inputs['cin'] = bits[2]

    # Simulate the full adder circuit
    signals = fa.simulate(inputs)
    print ("{:^3}{:^3}{:^4}|{:^4}{:^3}".format(inputs['a'], inputs['b'],
                                               inputs['cin'], signals['cout'],
                                               signals['s']))
    
print ("===============================")

    
# Let's try something bigger: 16 bit ripple carry adder...
try:
    c = circ.parse('benchmarks/csa16.crc')
except Exception as e:    
    print ("[INF] Could not load circuit. Good bye!")
    raise e

# Convenient function to group bits to a bitvector
def makeBV(name, width):
    bv = ['%s_%d' % (name, i) for i in range(width-1, -1, -1)]
    return bv

# Convenient function to get the integer value of a bitvector
def evalBV(bv, values):
    assignment = ['1' if values[x] else '0' for x in bv]
    bitstr = ''.join(assignment)
    return int(bitstr, 2)

a = makeBV('a', 16)  # 16 bit input a
b = makeBV('b', 16)  # 16 bit input b
s = makeBV('s', 17)  # 17 bit output s (sum)

# Do some random simulations...
for i in range(10):

    # Set inputs to random values
    inputs = {x: random.choice([False, True]) for x in c.getInputs()}

    # Simulate adder circuit
    signals = c.simulate(inputs)

    # Extract only output values 
    outputs = {x: b for (x,b) in signals.items() if x in c.getOutputs()}

    # Get integer values for a, b, and s
    aint = evalBV(a, inputs)
    bint = evalBV(b, inputs)
    sint = evalBV(s, outputs)    
    print ('{:>6} + {:>6} = {:>6}'.format(aint, bint, sint))

    # Checki if the result is correct
    assert(aint + bint == sint)

# ===================================== Internal structure of circuits
print ("===============================")

inputs = c.getInputs()   # input signals
outputs = c.getOutputs() # output signals
signals = c.getSignals() # output and internal signals (there is an equation for each)

nd = c.getEquation('s_13')
print ("Node s_13: {} [type {}]".format(nd, type(nd)))
print ("Node id: {}".format(nd.getID()))
print ("Node operation: {}".format(nd.getOp()))
for ch in nd.getChildren():
    print ("Child node (id: {}): {} [type: {}]".format(ch.getID(), ch, type(ch)))
    
# ===================================== CNF formulas and SAT solving
print ("===============================")

x = SatVar('x')
y = SatVar('y')
z = SatVar('z')

cnf = (x | ~y) & (z | y)
print (cnf)

solver = Solver()
solution = solver.solve(cnf)
print (solution)

cnf &= ~x
print (cnf)
solution = solver.solve(cnf)
print (solution)
if solution:
    print ("x = {}".format(solution[x]))
    print ("y = {}".format(solution['y']))
    print ("z = {}".format(solution[SatVar('z')]))

cnf &= ~y
print (cnf)
solution = solver.solve(cnf)
print (solution)

cnf &= ~z
print (cnf)
solution = solver.solve(cnf)
print (solution)
assert (not solution)

