from datetime import datetime
from sys import exc_info

import logging
logger = logging.getLogger(__name__)


def extended_trace(func=None, redact=[]):
    '''
    This small decorator will trace the execution of your code every time it
    enters or exits a decorated function (by thread) and will insert appropriate
    indent into the log file along with exception information.
    http://djangosnippets.org/snippets/2250/
    '''
    import threading
    import traceback

    def wrapper(func):
        def decorator(*args, **kwargs):
            if not hasattr(trace, 'local'):
                trace.local = threading.local()
            tl = trace.local

            if not hasattr(tl, 'log_indent'):
                tl.log_indent = 0

            funcname = func.__module__ + "." + func.__name__

            # List all positional arguments
            margs = [str("'%s'" % arg if isinstance(arg, str) else arg) for arg in [("********" if i in redact else arg) for i, arg in enumerate(args)]]

            # List all keyword arguments
            margs.extend(["%s=%s" % (key, str("'%s'" % val if isinstance(val, str) else val)) for key, val in [(key, ("********" if key in redact else val)) for key, val in kwargs.items()]])

            try:
                logger.debug("\t" * tl.log_indent + "Entering %s(%s)" % (funcname, ", ".join(margs)))
                tl.log_indent+=1
                retval = func(*args, **kwargs)
                tl.log_indent-=1
                logger.debug("\t" * tl.log_indent + "Leaving %s = %s" % (funcname, retval))
                return retval
            except Exception as e:
                tl.log_indent -= 1
                file = traceback.extract_tb()[-1][0]
                line = traceback.extract_tb()[-1][1]
                clsfunc = e.__class__.__name__
                logger.error("\t" * tl.log_indent + "Encountered error in %s: %s(%s) [%s:%i]" % (funcname, clsfunc, e.message, file, line))
                raise e, None, exc_info()[2]
        return decorator

    if func:
        return wrapper(func)
    else:
        return wrapper


def trace(func=None, log_return=False):
    '''
    This is a decorator that logs function arguments, return object and time
    taken for execution as well as any exception that might have been raised
    by the function. Useful for debug logging.
    http://djangosnippets.org/snippets/1382/
    '''

    def wrapper(*args, **kw):
        start = datetime.now()
        e = None
        try:
            ret = func(*args, **kw)
        except Exception, e:
            pass
        time_taken = datetime.now() - start

        if log_return:
            logger.debug(
                "name=%s args=%s, kw=%s, time=%s" % (
                    func.__name__, args, kw, ret, time_taken)
            )
        else:
            logger.debug("name=%s, args=%s, kw=%s, time=%s" % (
                func.__name__, args, kw, time_taken)
            )

        if e:
            logger.exception(e)
            raise e, None, exc_info()[2]
        return ret
    return wrapper
