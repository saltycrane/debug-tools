import inspect
import sys
from functools import wraps
from pprint import pformat

from blessings import Terminal


enabled = True


def _color_print(msg, type):
    term = Terminal()
    COLORS = {
        'prt': term.yellow,
        'pvar1': term.yellow,
        'pvar2': term.white,
        'pfunc': term.green,
        'enter': term.green,
        'exit': term.green,
        'normal': term.normal,
    }
    print >> sys.stderr, COLORS[type] + msg + COLORS['normal']


def prt(text):
    if enabled:
        frame = sys._getframe(1)
        _color_print('>>> %s (%s:%s):' % (text,
                                          frame.f_code.co_filename,
                                          frame.f_lineno), 'prt')


def pfunc():
    '''Print the parent function name'''
    if enabled:
        frame = inspect.stack()[1]
        msg = '%s:%d %s' % (frame[1], frame[2], frame[3])
        _color_print(msg, 'pfunc')


def pvar(expression):
    """print eval('str(<expression>)')
    """
    if enabled:
        frame = sys._getframe(1)
        globals = frame.f_globals
        locals = frame.f_locals
        result = eval('str(%s)' % expression, globals, locals)
        _color_print('>>> %s (%s:%s):' % (expression,
                                          frame.f_code.co_filename,
                                          frame.f_lineno), 'pvar1')
        if not isinstance(result, basestring):
            result = pformat(result)
        _color_print(result, 'pvar2')


def pdeco(print_args=False):
    '''Print the parent function name'''
    def true_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if enabled:
                if print_args:
                    msg = '>>> ENTERING %s(args=%s, kwargs=%s) %s:%s' % (
                        f.__code__.co_name, args, kwargs,
                        f.__code__.co_filename, f.__code__.co_firstlineno,
                        )
                else:
                    msg = '>>> ENTERING %s() %s:%s' % (
                        f.__code__.co_name,
                        f.__code__.co_filename, f.__code__.co_firstlineno,
                        )
                _color_print(msg, 'enter')
            r = f(*args, **kwargs)

            if enabled:
                msg = '>>> EXITING %s() %s:%s' % (
                    f.__code__.co_name,
                    f.__code__.co_filename, f.__code__.co_firstlineno,
                    )
                _color_print(msg, 'exit')
            return r
        return wrapper
    return true_decorator