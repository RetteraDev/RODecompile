
"""
opcode module - potentially shared between dis and other modules which
operate on bytecodes (e.g. peephole optimizers).
"""

__all__ = ["cmp_op", "hasconst", "hasname", "hasjrel", "hasjabs",
           "haslocal", "hascompare", "hasfree", "opname", "opmap",
           "HAVE_ARGUMENT", "EXTENDED_ARG"]

cmp_op = ('<', '<=', '==', '!=', '>', '>=', 'in', 'not in', 'is',
        'is not', 'exception match', 'BAD')

hasconst = []
hasname = []
hasjrel = []
hasjabs = []
haslocal = []
hascompare = []
hasfree = []

opmap = {}
opname = [''] * 256
for op in range(256): opname[op] = '<%r>' % (op,)
del op

def def_op(name, op):
    opname[op] = name
    opmap[name] = op

def name_op(name, op):
    def_op(name, op)
    hasname.append(op)

def jrel_op(name, op):
    def_op(name, op)
    hasjrel.append(op)

def jabs_op(name, op):
    def_op(name, op)
    hasjabs.append(op)

# Instruction opcodes for compiled code
# Blank lines correspond to available opcodes

def_op('STOP_CODE', 20)
def_op('POP_TOP', 21)
def_op('ROT_TWO', 22)
def_op('ROT_THREE', 23)
def_op('DUP_TOP', 24)
def_op('ROT_FOUR', 25)

def_op('NOP', 9)
def_op('UNARY_POSITIVE', 10)
def_op('UNARY_NEGATIVE', 11)
def_op('UNARY_NOT', 12)
def_op('UNARY_CONVERT', 13)

def_op('UNARY_INVERT', 15)

def_op('BINARY_POWER', 19)
def_op('BINARY_MULTIPLY', 0)
def_op('BINARY_DIVIDE', 1)
def_op('BINARY_MODULO', 2)
def_op('BINARY_ADD', 3)
def_op('BINARY_SUBTRACT', 4)
def_op('BINARY_SUBSCR', 5)
def_op('BINARY_FLOOR_DIVIDE', 26)
def_op('BINARY_TRUE_DIVIDE', 27)
def_op('INPLACE_FLOOR_DIVIDE', 28)
def_op('INPLACE_TRUE_DIVIDE', 29)
def_op('SLICE+0', 30)
def_op('SLICE+1', 31)
def_op('SLICE+2', 32)
def_op('SLICE+3', 33)

def_op('STORE_SLICE+0', 40)
def_op('STORE_SLICE+1', 41)
def_op('STORE_SLICE+2', 42)
def_op('STORE_SLICE+3', 43)

def_op('DELETE_SLICE+0', 50)
def_op('DELETE_SLICE+1', 51)
def_op('DELETE_SLICE+2', 52)
def_op('DELETE_SLICE+3', 53)

def_op('STORE_MAP', 56)
def_op('INPLACE_ADD', 57)
def_op('INPLACE_SUBTRACT', 54)
def_op('INPLACE_MULTIPLY', 55)
def_op('INPLACE_DIVIDE', 60)
def_op('INPLACE_MODULO', 61)
def_op('STORE_SUBSCR', 58)
def_op('DELETE_SUBSCR', 59)
def_op('BINARY_LSHIFT', 66)
def_op('BINARY_RSHIFT', 67)
def_op('BINARY_AND', 68)
def_op('BINARY_XOR', 65)
def_op('BINARY_OR', 62)
def_op('INPLACE_POWER', 63)
def_op('GET_ITER', 64)

def_op('PRINT_EXPR', 70)
def_op('PRINT_ITEM', 71)
def_op('PRINT_NEWLINE', 72)
def_op('PRINT_ITEM_TO', 73)
def_op('PRINT_NEWLINE_TO', 74)
def_op('INPLACE_LSHIFT', 82)
def_op('INPLACE_RSHIFT', 83)
def_op('INPLACE_AND', 84)
def_op('INPLACE_XOR', 85)
def_op('INPLACE_OR', 86)
def_op('BREAK_LOOP', 87)
def_op('WITH_CLEANUP', 81)
def_op('LOAD_LOCALS', 75)
def_op('RETURN_VALUE', 76)
def_op('IMPORT_STAR', 77)
def_op('EXEC_STMT', 78)
def_op('YIELD_VALUE', 79)
def_op('POP_BLOCK', 80)
def_op('END_FINALLY', 88)
def_op('BUILD_CLASS', 89)

HAVE_ARGUMENT = 90

name_op('STORE_NAME', 93)
name_op('DELETE_NAME', 94)
def_op('UNPACK_SEQUENCE', 92)
jrel_op('FOR_ITER', 90)
def_op('LIST_APPEND', 91)
name_op('STORE_ATTR', 103)
name_op('DELETE_ATTR', 104)
name_op('STORE_GLOBAL', 105)
name_op('DELETE_GLOBAL', 106)
def_op('DUP_TOPX', 107)
def_op('LOAD_CONST', 100)
hasconst.append(100)
name_op('LOAD_NAME', 101)
def_op('BUILD_TUPLE', 102)
def_op('BUILD_LIST', 95)
def_op('BUILD_SET', 96)
def_op('BUILD_MAP', 97)
name_op('LOAD_ATTR', 98)
def_op('COMPARE_OP', 99)
hascompare.append(99)
name_op('IMPORT_NAME', 108)
name_op('IMPORT_FROM', 109)
jrel_op('JUMP_FORWARD', 110)
jabs_op('JUMP_IF_FALSE_OR_POP', 111)
jabs_op('JUMP_IF_TRUE_OR_POP', 119)
jabs_op('JUMP_ABSOLUTE', 113)
jabs_op('POP_JUMP_IF_FALSE', 112)
jabs_op('POP_JUMP_IF_TRUE', 126)

name_op('LOAD_GLOBAL', 116)

jabs_op('CONTINUE_LOOP', 114)
jrel_op('SETUP_LOOP', 124)
jrel_op('SETUP_EXCEPT', 125)
jrel_op('SETUP_FINALLY', 115)

def_op('LOAD_FAST', 120)
haslocal.append(120)
def_op('STORE_FAST', 121)
haslocal.append(121)
def_op('DELETE_FAST', 122)
haslocal.append(122)

def_op('RAISE_VARARGS', 130)
def_op('CALL_FUNCTION', 131)
def_op('MAKE_FUNCTION', 132)
def_op('BUILD_SLICE', 133)
def_op('MAKE_CLOSURE', 135)
def_op('LOAD_CLOSURE', 134)
hasfree.append(134)
def_op('LOAD_DEREF', 137)


hasfree.append(137)
def_op('STORE_DEREF', 136)
hasfree.append(136)
def_op('CALL_FUNCTION_VAR', 140)
def_op('CALL_FUNCTION_KW', 141)
def_op('CALL_FUNCTION_VAR_KW', 142)

jrel_op('SETUP_WITH', 143)

def_op('EXTENDED_ARG', 145)
EXTENDED_ARG = 145
def_op('SET_ADD', 147)
def_op('MAP_ADD', 146)

del def_op, name_op, jrel_op, jabs_op
