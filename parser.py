#!/usr/bin/env python3

from funcparserlib.parser import *
from funcparserlib.parser import with_forward_decls
from tokenize import generate_tokens, TokenInfo
from io import StringIO
from functools import reduce

from circuit import *

import token

# FIXME: There seems to be an inconsistency between the token.type and
# the type constants defined in token!
MY_NEWLINE = 58

def tokenize(s):
    return [t for t in  generate_tokens(StringIO(s).readline)
            if t.type not in [token.ENDMARKER, token.NEWLINE, MY_NEWLINE]]

def tokval(tok):
    return tok.string

def make_bool(s):
    return s == '1'

# @RULE:
# boolean ::= '1' | '0'
boolean = (
    some(lambda tok: tok.type == token.NUMBER and tok.string in ['1','0'])
    >> tokval
    >> make_bool
    >> Literal
)

# @RULE
# variable ::= NAME (as Variable)
variable = (
    some(lambda tok: tok.type == token.NAME)
    >> tokval
    >> Variable
)

# @RULE
# variable ::= NAME (as string)
name = (
    some(lambda tok: tok.type == token.NAME)
    >> tokval
)

# Operator functor
op = (
    lambda s: some(lambda tok: tok.type == token.OP and tok.string == s)
    >> tokval
)

comma = op(',')

# Keyword functor
keyword = (
    lambda s: some(lambda tok: tok.type == token.NAME and tok.string == s)
    >> tokval
    )

# @KEYWORD 'inputs'
inp = keyword('inputs')

# @KEYWORD 'outputs'
outp = keyword('outputs')

# @KEYWORD 'circ'
circ = keyword('circ')

const = lambda x: lambda _: x

# Functor for operator construction. Returns a parser functor that
# results in the second argument f, the function associated with the
# operator.
makeop = lambda s, f: op(s) >> const(f)

# Functor constructing a binary node
def make_node(f, opstr):
    return lambda x, y: BinOp(f, opstr, x, y)

# Functor constructing a unary node
def make_unode(f, opstr):
    return lambda x: UnOp(f, opstr, x)

# Functor constructing an output, which is just a pair of a variable
# and an expression
def make_output(x, e):
    return (x, e)

# Binary operators
import operator
and_ = makeop('&', make_node(operator.and_, '&'))
or_  = makeop('|', make_node(operator.or_,'|'))
xor  = makeop('^', make_node(operator.xor,'^'))
not_ = makeop('~', make_unode(operator.not_,'~'))
asgn = makeop('=', make_output)

# Evaluate a tree-ish expression by folding (reducing) it
def eval_expr(z, l):
    return reduce(lambda s, y: y[0](s, y[1]), l, z)

# Evaluate a unary expression
def eval_uexpr(f, x):
    return f(x)

# Evaluate a binary expression
def eval_binexpr(x, f, y):
    return f(x, y)

# Assemble nested list
def assemble(x, y):
    if type(y) is list:
        return [x] + y
    else:
        return [x, y]

# Currying 
unarg = lambda f: lambda x: f(*x)

# Curried functors for evaluation functions and constructors
f = unarg(eval_expr)
g = unarg(eval_uexpr)
h = unarg(eval_binexpr)
collect = unarg(assemble)
make_circ = unarg(Circuit)

# @RULE:
# primary ::= boolean | variable | '(' expr ')'
@with_forward_decls
def primary():
    return boolean | variable | ((op('(') + expr + op(')')) >> (lambda x: x[1]))

# @RULE
# literal ::= not primary | primary
literal = not_ + primary >> g | primary

# @RULE
# minterm ::= literal (and literal)*
minterm = literal + many(and_ + literal) >> f

# @RULE
# esop ::= minterm (xor minterm)*
esop = minterm + many(xor + minterm) >> f

# @RULE
# expr ""= esop (or esop)*
expr = esop + many(or_ + esop) >> f

# @RULE
# assign = variable '=' expr
assign = variable + asgn + expr >> h

# @RULE
# varlist ::= variable (',' variable)*
varlist = variable + many(skip(comma) + variable) >> collect

# @RULE
# inputs ::= 'inputs' ':' varlist
inputs = skip(inp) + skip(op(':')) + varlist

# @RULE
# outputs ::= 'outputs' ':' varlist
outputs = skip(outp) + skip(op(':')) + varlist

# @RULE
# body ::= (assign)*
body = many(assign)

# @RULE
# circuit ::= 'circ' name '{' inputs outputs body '}' EOF
circuit =  (skip(circ) + name
            + skip(op('{'))
            + inputs
            + outputs
            + body
            + skip(op('}'))
            + skip(finished)) >> make_circ


# main parse function
def parse(filename):
    print ("[INF] Parsing file '%s'" % filename)
    try:
        with open(filename, 'r') as f:
            s = f.read()
            tok = tokenize(s)
            return circuit.parse(tok)
    except FileNotFoundError as e:
        print ("[ERR] Could not open file '%s'" % filename)
        raise e
    except BrokenCircuitException as e:
        print ("[ERR] %s" % e)
        raise e
    except NoParseError as e:
        epos = e.state.pos
        etok = tok[epos]
        line = etok.line
        start = etok.start[1]
        end = etok.end[1]
        lineNo = etok.start[0]
        print ("[ERR] Syntax error in line %d:" % lineNo)
        print ("[ERR] %s" % line.replace('\n',''))
        print ("[ERR] " + (' '*start) + ('~'*(end-start+1)))
        raise e
            
        
