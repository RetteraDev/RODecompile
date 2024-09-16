#Embedded file name: I:/bag/tmp/tw2/res/entities\common/gamescript.o
import gametypes
from gamelog import error

class ScriptRunningEnv(object):
    GLOBAL_VARS = {}
    INVALID_OPCODES = ['raise', 'while']
    SCRIPT_CACHE = {}

    @staticmethod
    def processExec(scriptKey, script, localVars = {}):
        ScriptRunningEnv._setupSandbox()
        if not ScriptRunningEnv.SCRIPT_CACHE.has_key(scriptKey):
            codeObj = compile(script, '', 'exec')
            ScriptRunningEnv.SCRIPT_CACHE[scriptKey] = codeObj
        codeObj = ScriptRunningEnv.SCRIPT_CACHE[scriptKey]
        locals = {}
        for key, value in localVars.items():
            locals[key] = value

        for key, value in ScriptRunningEnv.GLOBAL_VARS.items():
            locals[key] = value

        exec codeObj in locals
        return ScriptRunningEnv.GLOBAL_VARS['retv']

    @staticmethod
    def _checkOpcode(node, depth):
        for key, subNode in enumerate(node):
            name = subNode.__class__.__name__
            if name in ScriptRunningEnv.INVALID_OPCODES:
                error('@szh: ScriptRunningEnv: invalid opcode:%s' % (name,))
                return False
            if hasattr(subNode, '__iter__'):
                ScriptRunningEnv._checkOpcode(subNode, depth + 1)

        return True

    @staticmethod
    def _setupSandbox():
        if len(ScriptRunningEnv.GLOBAL_VARS) == 0:
            safeBuiltins = {}
            for fname in ('print', 'abs', 'chr', 'cmp', 'complex', 'dict', 'divmod', 'enumerate', 'filter', 'float', 'hex', 'int', 'len', 'list', 'long', 'map', 'max', 'min', 'oct', 'ord', 'pow', 'range', 'reduce', 'reversed', 'round', 'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'unichr', 'unicode', 'xrange', 'zip', 'repr'):
                safeBuiltins[fname] = __builtins__[fname]

            ScriptRunningEnv.GLOBAL_VARS['__builtins__'] = safeBuiltins
            import math
            for fname in ('acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'copysign', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum', 'hypot', 'isinf', 'isnan', 'ldexp', 'log', 'log10', 'log1p', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'trunc'):
                ScriptRunningEnv.GLOBAL_VARS[fname] = getattr(math, fname)

            ScriptRunningEnv.GLOBAL_VARS['retv'] = None

            def retf(x):
                ScriptRunningEnv.GLOBAL_VARS['retv'] = x

            ScriptRunningEnv.GLOBAL_VARS['ret'] = retf
        ScriptRunningEnv.GLOBAL_VARS['retv'] = 0

    @staticmethod
    def reloadScript():
        ScriptRunningEnv.GLOBAL_VARS = {}
        ScriptRunningEnv._setupSandbox()
        ScriptRunningEnv.SCRIPT_CACHE = {}


class FormularEvalEnv(object):
    GLOBAL_VARS = {}

    @staticmethod
    def evaluate(script, localVars):
        FormularEvalEnv._setupSandbox()
        locals = {}
        for key, value in localVars.items():
            locals[key] = value

        return eval(script, FormularEvalEnv.GLOBAL_VARS, locals)

    @staticmethod
    def _setupSandbox():
        if len(FormularEvalEnv.GLOBAL_VARS) == 0:
            safeBuiltins = {}
            for fname in ('abs', 'chr', 'cmp', 'divmod', 'float', 'hex', 'int', 'max', 'min', 'pow', 'round', 'sum'):
                safeBuiltins[fname] = __builtins__[fname]

            FormularEvalEnv.GLOBAL_VARS['__builtins__'] = safeBuiltins
            import math
            for fname in ('acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'copysign', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum', 'hypot', 'isinf', 'isnan', 'ldexp', 'log', 'log10', 'log1p', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'trunc'):
                FormularEvalEnv.GLOBAL_VARS[fname] = getattr(math, fname)

    @staticmethod
    def reloadScript():
        FormularEvalEnv.GLOBAL_VARS = {}
        FormularEvalEnv._setupSandbox()


def makeFuncFromScript(formulaId, *argsName):

    def f(*args):
        if len(args) != len(argsName):
            raise Exception('@zs:error!!!!, _makeFuncFromScript error!!!')
            return
        locals = {}
        for name, arg in zip(argsName, args):
            locals[name] = arg

        import formula
        return formula.calcFormulaById(formulaId, locals)

    return f


FORMULA_FLV = makeFuncFromScript(gametypes.FORMULA_ID_LV, 'lv')
FORMULA_POWER = makeFuncFromScript(gametypes.FORMULA_ID_POWER, 'power')
FORMULA_FLV_5 = makeFuncFromScript(gametypes.FORMULA_ID_LV_5, 'lv')
