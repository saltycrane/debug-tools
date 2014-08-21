import inspect
import sys
from functools import wraps
from pprint import pformat

from blessings import Terminal


enabled = True


def _color_print(msg, type):
    term = Terminal()
    COLORS = {
        'prt': term.cyan,
        'pvar1': term.yellow,
        'pvar2': term.white,
        'pfunc': term.green,
        'pstack': term.green,
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


def pstack():
    '''Print the parent function name'''
    if enabled:
        for frame in inspect.stack():
            msg = '%s:%d %s' % (frame[1], frame[2], frame[3])
            _color_print(msg, 'pstack')


def pvar(expression, format=None):
    """print eval('str(<expression>)')
    """
    if enabled:
        frame = sys._getframe(1)
        globals = frame.f_globals
        locals = frame.f_locals
        result = eval('%s' % expression, globals, locals)
        _color_print('\n>>> %s (%s:%s):' % (expression,
                                            frame.f_code.co_filename,
                                            frame.f_lineno), 'pvar1')
        if not isinstance(result, basestring):
            result = pformat(result)
        if format == 'xml':
            result = _format_xml(result)
        _color_print(result, 'pvar2')


def pxml(expression):
    # TODO: DRY. same as pvar above but can't call pvar because of use of locals
    if enabled:
        frame = sys._getframe(1)
        globals = frame.f_globals
        locals = frame.f_locals
        result = eval('%s' % expression, globals, locals)
        _color_print('\n>>> %s (%s:%s):' % (expression,
                                            frame.f_code.co_filename,
                                            frame.f_lineno), 'pvar1')
        if isinstance(result, basestring):
            result = _format_xml(result)
        else:
            result = pformat(result)
        _color_print(result, 'pvar2')


def _format_xml(s):
    import re
    import xml.dom.minidom
    s = unicode(s).encode("utf-8")
    s = xml.dom.minidom.parseString(s)
    s = s.toprettyxml(indent='  ')
    regex = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)
    return regex.sub('>\g<1></', s)


def pstr(expression):
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
