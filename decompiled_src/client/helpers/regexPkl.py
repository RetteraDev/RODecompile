#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/regexPkl.o
import re, sre_compile, sre_parse, _sre
import cPickle as pickle

def rawCompile(p, flags = 0):
    if sre_compile.isstring(p):
        pattern = p
        p = sre_parse.parse(p, flags)
    else:
        pattern = None
    code = sre_compile._code(p, flags)
    return (pattern, p, code)


def buildCompiled(pattern, p, flags, code):
    if p.pattern.groups > 100:
        raise AssertionError('sorry, but this version only supports 100 named groups')
    groupindex = p.pattern.groupdict
    indexgroup = [None] * p.pattern.groups
    for k, i in groupindex.items():
        indexgroup[i] = k

    return _sre.compile(pattern, flags | p.pattern.flags, code, p.pattern.groups - 1, groupindex, indexgroup)


def compileHalfAndPkl(regex, flag):
    r, p, code = rawCompile(regex, flag)
    return pickle.dumps((r, p, code))


def unpklAndFulfillOtherHalfCompile(pkl):
    r, p, code = pickle.loads(pkl)
    return buildCompiled(r, p, re.U, code)
