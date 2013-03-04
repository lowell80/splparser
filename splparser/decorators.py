
from splparser.exceptions import SPLSyntaxError, TerminatingSPLSyntaxError
from splparser.parser import SPLParser

OPTIMIZE = False

def splcommandrule(f):
    cmd = f.__doc__.split(':')[1].split()[0].strip().lower()
    cmdlexer = 'splparser.lexers.' + cmd + 'lexer'
    cmdlexer = __import__(cmdlexer, fromlist=['__import__ is dumb'])
    cmdparsetab = cmd + '_parsetab'
    cmdparsetab_dir = 'parsetabs'
    cmdrules = 'splparser.rules.' + cmd + 'rules'
    cmdrules = __import__(cmdrules, fromlist=['fromlist does nothing'])
    parser = SPLParser(cmdlexer, cmdparsetab, cmdparsetab_dir, cmdrules, optimize=OPTIMIZE)
    def helper(p):
        try:
            p[0]  = parser.parse(' '.join(p[1:]))
        except Exception as e:
            raise TerminatingSPLSyntaxError(e.message) 
    helper.__doc__ = f.__doc__
    return helper

def notimplemented(f):
    cmd = f.__doc__.split(':')[1].split()[0].strip().lower()
    def helper(p):
        raise NotImplementedError(cmd + " is not yet implemented.")
    helper.__doc__ = f.__doc__
    return helper

