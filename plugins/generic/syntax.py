import re

from core.common import Backend
from core.convert import getBytes
from core.data import conf
from core.enums import DBMS
from core.exceptions import AnkabUndefinedMethod

class Syntax(object):
    """
    This class defines generic syntax functionalities for plugins.
    """

    def __init__(self):
        pass

    @staticmethod
    def _escape(expression, quote=True, escaper=None):
        retVal = expression

        if quote:
            for item in re.findall(r"'[^']*'+", expression):
                original = item[1:-1]
                if original:
                    if Backend.isDbms(DBMS.SQLITE) and "X%s" % item in expression:
                        continue
                    if re.search(r"\[(SLEEPTIME|RAND)", original) is None:  # e.g. '[SLEEPTIME]' marker
                        replacement = escaper(original) if not conf.noEscape else original

                        if replacement != original:
                            retVal = retVal.replace(item, replacement)
                        elif len(original) != len(getBytes(original)) and "n'%s'" % original not in retVal and Backend.getDbms() in (DBMS.MYSQL, DBMS.PGSQL, DBMS.ORACLE, DBMS.MSSQL):
                            retVal = retVal.replace("'%s'" % original, "n'%s'" % original)
        else:
            retVal = escaper(expression)

        return retVal

    @staticmethod
    def escape(expression, quote=True):
        errMsg = "'escape' method must be defined "
        errMsg += "inside the specific DBMS plugin"
        raise AnkabUndefinedMethod(errMsg)
