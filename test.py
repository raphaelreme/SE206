#!/usr/bin/env python3

import sys
import random

from circuit import *
from parser import parse

try:
    c = parse('examples/foo.crc')
except Exception as e:
    print ("[INF] Could not load circuit. Good bye!")
    sys.exit(1)

inputs = {x: True for x in c.getInputs()}
print (c.simulate(inputs))

inputs = {x: False for x in c.getInputs()}
print (c.simulate(inputs))

for i in range(10):
    inputs = {x: random.choice([False, True]) for x in c.getInputs()}
    outputs = c.simulate(inputs)
    def b2s(b):
        return '1' if b else '0'
    def d2s(d):
        return ''.join([b2s(b) for (x,b) in d.items()])
    print ('%s -> %s' % (d2s(inputs), d2s(outputs)))
