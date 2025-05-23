import sys, time







PYVERSION = sys.version.split()[0]


if PYVERSION < "2.6":
    sys.exit("[ ETA ]: ( %s ) [CRITICAL] incompatible Python version detected ('%s'). To successfully run sqlmap you'll have to use version 2.6, 2.7 or 3.x (visit 'https://www.python.org/downloads/')" % (time.strftime("%X"), PYVERSION))
    
errors = []
extensions = ("bz2", "gzip", "pyexpat", "ssl", "sqlite3", "zlib")

for _ in extensions:
    try:
        __import__()
    except ImportError:
        errors.append(_)

if errors:
    errMsg = "[ ETA ]: ( %s ) [CRITICAL] missing one or more core extensions (%s) " % (time.strftime("%X"), ", ".join("'%s'" % _ for _ in errors))
    errMsg += "most likely because current version of Python has been "
    errMsg += "built without appropriate dev packages"
    sys.exit(errMsg)