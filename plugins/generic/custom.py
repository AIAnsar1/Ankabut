from __future__ import print_function

import re
import sys

from core.common import Backend, dataToStdout, getSQLSnippet, isListLike, isStackingAvailable, joinValue
from core.compat import xrange
from core.convert import getUnicode
from core.data import conf, logger
from core.dicts import SQL_STATEMENTS
from core.enums import AutoCompleteType, DBMS
from core.exceptions import AnkabNoneDataException
from core.settings import METADB_SUFFIX, NULL, PARAMETER_SPLITTING_REGEX
from core.shell import autoCompletion
from request import inject
from pkg.six.moves import input as _input

class Custom(object):
    """
    This class defines custom enumeration functionalities for plugins.
    """

    def __init__(self):
        pass

    def sqlQuery(self, query):
        output = None
        sqlType = None
        query = query.rstrip(';')


        try:
            for sqlTitle, sqlStatements in SQL_STATEMENTS.items():
                for sqlStatement in sqlStatements:
                    if query.lower().startswith(sqlStatement):
                        sqlType = sqlTitle
                        break

            if not re.search(r"\b(OPENROWSET|INTO)\b", query, re.I) and (not sqlType or "SELECT" in sqlType):
                infoMsg = "fetching %s query output: '%s'" % (sqlType if sqlType is not None else "SQL", query)
                logger.info(infoMsg)

                if Backend.isDbms(DBMS.MSSQL):
                    match = re.search(r"(\bFROM\s+)([^\s]+)", query, re.I)
                    if match and match.group(2).count('.') == 1:
                        query = query.replace(match.group(0), "%s%s" % (match.group(1), match.group(2).replace('.', ".dbo.")))

                query = re.sub(r"(?i)\w+%s\.?" % METADB_SUFFIX, "", query)

                output = inject.getValue(query, fromUser=True)

                if sqlType and "SELECT" in sqlType and isListLike(output):
                    for i in xrange(len(output)):
                        if isListLike(output[i]):
                            output[i] = joinValue(output[i])

                return output
            elif not isStackingAvailable() and not conf.direct:
                warnMsg = "execution of non-query SQL statements is only "
                warnMsg += "available when stacked queries are supported"
                logger.warning(warnMsg)

                return None
            else:
                if sqlType:
                    infoMsg = "executing %s statement: '%s'" % (sqlType if sqlType is not None else "SQL", query)
                else:
                    infoMsg = "executing unknown SQL command: '%s'" % query
                logger.info(infoMsg)

                inject.goStacked(query)

                output = NULL

        except AnkabNoneDataException as ex:
            logger.warning(ex)

        return output

    def sqlShell(self):
        infoMsg = "calling %s shell. To quit type " % Backend.getIdentifiedDbms()
        infoMsg += "'x' or 'q' and press ENTER"
        logger.info(infoMsg)

        autoCompletion(AutoCompleteType.SQL)

        while True:
            query = None

            try:
                query = _input("sql-shell> ")
                query = getUnicode(query, encoding=sys.stdin.encoding)
                query = query.strip("; ")
            except UnicodeDecodeError:
                print()
                errMsg = "invalid user input"
                logger.error(errMsg)
            except KeyboardInterrupt:
                print()
                errMsg = "user aborted"
                logger.error(errMsg)
            except EOFError:
                print()
                errMsg = "exit"
                logger.error(errMsg)
                break

            if not query:
                continue

            if query.lower() in ("x", "q", "exit", "quit"):
                break

            output = self.sqlQuery(query)

            if output and output != "Quit":
                conf.dumper.sqlQuery(query, output)

            elif not output:
                pass

            elif output != "Quit":
                dataToStdout("No output\n")

    def sqlFile(self):
        infoMsg = "executing SQL statements from given file(s)"
        logger.info(infoMsg)

        for filename in re.split(PARAMETER_SPLITTING_REGEX, conf.sqlFile):
            filename = filename.strip()

            if not filename:
                continue

            snippet = getSQLSnippet(Backend.getDbms(), filename)

            if snippet and all(query.strip().upper().startswith("SELECT") for query in (_ for _ in snippet.split(';' if ';' in snippet else '\n') if _)):
                for query in (_ for _ in snippet.split(';' if ';' in snippet else '\n') if _):
                    query = query.strip()
                    if query:
                        conf.dumper.sqlQuery(query, self.sqlQuery(query))
            else:
                conf.dumper.sqlQuery(snippet, self.sqlQuery(snippet))
