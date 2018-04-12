#!/usr/bin/env python3

class BrokenCircuitException(Exception):
    '''This exception is thrown by the constructor of the Cicruit class if
    it detects either undefined signals or combinational loops.
    '''
    pass

class Node(object):
    '''Base class for circuit nodes'''

    __nextid__ = 0
    
    def __init__(self):
        self.kids = []
        self.id = Node.__nextid__
        Node.__nextid__ += 1

    def __lt__(self, other):
        return self.id < other.id

    def __hash__(self):
        return hash(7879 + self.id) * hash(type(self))
        
    def getID(self):
        '''Get unique node id (as int)'''
        return self.id
        
    def getChildren(self):
        '''Get child nodes of this node'''
        return self.kids

    def getChild(self, i):
        '''Get i-th child of this node'''
        return self.kids[i]

    def setChild(self, i, nd):
        '''Set i-th child of this node'''
        self.kids[i] = nd
        
    def support(self):
        return set()

class Literal(Node):
    '''A circuit node representing a constant Boolean value, which is
    either True or False.
    '''
    
    def __init__(self, b):
        Node.__init__(self)
        self.value = b

    def __repr__(self):
        if self.value:
            return '1'
        else:
            return '0'

    def getValue(self):
        '''Get the literal's value'''
        return self.value

    def support(self):
        return set()
        
class Variable(Node):
    '''A circuit node representing a named internal or input signal.'''

    def __init__(self, name):
        Node.__init__(self)
        self.name = name

    def __repr__(self):
        return ('%s' % self.name)

    def getName(self):
        '''Get the name of the signal'''
        return self.name

    def support(self):
        return {self.name}

class OpNode(Node):
    '''Abstract base class for unary and binary logic gates.'''
    
    def getOp(self):
        '''Get a string representation of the node's function'''
        return opstr

    def getFun(self):
        '''Get the gate function of the node'''
        return f

class BinOp(OpNode):
    '''A circuit node representing a binary logic gate.'''
    
    def __init__(self, f, opstr, x, y):
        Node.__init__(self)
        self.kids = [x, y]
        self.f = f
        self.opstr = opstr

    def __repr__(self):
        return ('(%s %s %s)' % (self.kids[0], self.opstr, self.kids[1]))

    def eval(self, x, y):
        '''Evaluate the node's function with the given inputs'''
        return self.f(x, y)

    def support(self):
        return self.getChild(0).support() | self.getChild(1).support()

class UnOp(OpNode):
    '''A circuit node representing a unary logic gate.'''

    def __init__(self, f, opstr, x):
        Node.__init__(self)
        self.kids = [x]
        self.f = f
        self.opstr = opstr

    def __repr__(self):
        return ('(%s %s)' % (self.opstr, self.kids[0]))

    def eval(self, x):
        '''Evaluate the node's function with the given input'''
        return self.f(x)

    def support(self):
        return self.getChild(0).support()

    
class Circuit(object):
    '''Class representing a logic circuit.'''
    
    def __init__(self, name, inputs, outputs, eqs):
        self.name = name
        self.inputs = {x.name for x in inputs}
        self.outputs = {x.name for x in outputs}
        self.equations = dict()
        for (x,e) in eqs:
            self.equations[x.name] = e
        self.check()

    def check(self):
        '''Perform sanity checks on the circuit: all outputs defined, all
        inputs unconstrained, no undefined signals, no combinational
        loops. This function is called by the constructor. 
        '''

        # Check that all outputs are defined
        for x in self.outputs:
            if not x in self.equations.keys():
                raise BrokenCircuitException("Undefined output '%s'" % x)

        # Check that inputs are unconstrained
        for x in self.inputs:
            if x in self.equations.keys():
                raise BrokenCircuitException("Over-constrained input '%s' " % x)

        # Check that only defined signals are used
        deps = {x: self.equations[x].support() for x in self.equations.keys()}
        signals = self.inputs | self.outputs | self.equations.keys()
        for x,ys in deps.items():
            for y in ys:
                if not y in signals:
                    raise BrokenCircuitException("Undefined signal '%s'" % y)
                    
        # Check that there are no combinational loops in the circuit
        for x in deps.keys():
            stack = []
            def visit(y):
                if y in stack:
                    raise BrokenCircuitException("Combinational loop detected: %s -> %s" % (' -> '.join(stack), y))
                if not y in deps.keys():
                    return
                stack.append(y)
                for z in deps[y]:
                    visit(z)
                stack.pop()
            visit(x)

    def clean(self):
        '''Clean up the structure of the circuit: Collapse nodes with single
        fanout, remove dead nodes.
        '''

        # Collapse non-fanout nodes
        signals = self.outputs | self.equations.keys() | self.inputs
        fanout = {s: set() for s in signals}
        deps = {x: self.equations[x].support() for x in self.equations.keys()}        
        for x, ys in deps.items():
            for y in ys:
                fanout[y].add(x)
        collapse = {x for x,ys in fanout.items() if len(ys) == 1}.difference(self.inputs)
        print ("======================")
        print ("COLLAPSE:")
        print (collapse)
        print ("======================")
        for x in self.getSignals():
            def subst(nd):
                if type(nd) == Variable:
                    y = nd.getName()
                    if y in collapse:
                        print ("collapse %s" % y)
                        return subst(self.equations[y])
                    else:
                        return nd
                elif type(nd) == UnOp:
                    nd.setChild(0, subst(nd.getChild(0)))
                    return nd
                elif type(nd) == BinOp:
                    nd.setChild(0, subst(nd.getChild(0)))
                    nd.setChild(1, subst(nd.getChild(1)))
                    return nd
                else:
                    return nd
            e = self.equations[x]
            self.equations[x] = subst(e)

        # Remove dead nodes
        deps = {x: self.equations[x].support() for x in self.equations.keys()}
        edges = {(x,y) for x, ys in deps.items() for y in ys}
        closure = edges
        while True:
            frontier = {(x,w) for x,y in closure for q,w in closure if q == y}
            nxt_closure = closure | frontier
            if closure == nxt_closure:
                break
            closure = nxt_closure
        live = {y for (x,y) in closure if x in self.outputs}
        dead = signals.difference(live).difference(self.inputs).difference(self.outputs)
        print ("======================")
        print ("DEAD:")
        print (dead)
        print ("======================")
        for s in dead:
            del self.equations[s]
                        
    def getInputs(self):
        '''Returns the set of input identifiers.
        '''
        return self.inputs

    def getOutputs(self):
        '''Returns the set of output identifiers.
        '''
        return self.outputs

    def getSignals(self):
        '''Returns the set of identifiers for which a logic equation is
        defined. This includes the circuit's outputs and any internal
        signals.
        '''
        return self.equations.keys()

    def getEquation(self, x):
        '''Returns the root node of the logic expression assigned to signal x,
        where x is either an output or an internal signal.
        '''
        try:
            return self.equations[x]
        except KeyError:
            raise BrokenCircuitException("Undefined signal '%s'" % s)

    def simulate(self, inputs):
        '''Simulate the circuit. Takes as input a dictionary, mapping input
        names to Boolean values. Returns a dictionary mapping output
        and internal signal names to Boolean values.
        '''

        value = {i: x for (i,x) in inputs.items()}
        
        def sim(node):
            if type(node) == Literal:
                return node.value
            elif type(node) == Variable:
                x = node.name
                try:
                    return value[x]
                except KeyError:
                    y = sim(self.getEquation(x))
                    value[x] = y
                    return y
            elif type(node) == UnOp:
                y = sim(node.getChild(0))
                return node.eval(y)
            elif type(node) == BinOp:
                y = sim(node.getChild(0))
                z = sim(node.getChild(1))
                return node.eval(y, z)
            else:
                raise "Invalid node type."

        signals = self.getSignals()
        for x in signals:
            value[x] = sim(self.getEquation(x))
        return {s: x for (s,x) in value.items() if s in signals}
            
    def __repr__(self):
        s = 'circ %s {\n' % self.name
        s += '\tinputs: %s\n' % ', '.join(sorted(self.inputs))
        s += '\toutputs: %s\n' % ', '.join(sorted(self.outputs))
        for x, e in self.equations.items():
            s += '\t%s = %s\n' % (x, e)
        s += '}'
        return s
