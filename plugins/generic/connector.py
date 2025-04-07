import os

from core.data import conf, logger
from core.exceptions import AnkabFilePathException, AnkabUndefinedMethod

class Connector(object):
    """
    This class defines generic dbms protocol functionalities for plugins.
    """

    def __init__(self):
        self.connector = None
        self.cursor = None
        self.hostname = None

    def initConnection(self):
        self.user = conf.dbmsUser or ""
        self.password = conf.dbmsPass or ""
        self.hostname = conf.hostname
        self.port = conf.port
        self.db = conf.dbmsDb

    def printConnected(self):
        if self.hostname and self.port:
            infoMsg = "connection to %s server '%s:%d' established" % (conf.dbms, self.hostname, self.port)
            logger.info(infoMsg)

    def closed(self):
        if self.hostname and self.port:
            infoMsg = "connection to %s server '%s:%d' closed" % (conf.dbms, self.hostname, self.port)
            logger.info(infoMsg)

        self.connector = None
        self.cursor = None

    def initCursor(self):
        self.cursor = self.connector.cursor()

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connector:
                self.connector.close()
        except Exception as ex:
            logger.debug(ex)
        finally:
            self.closed()

    def checkFileDb(self):
        if not os.path.exists(self.db):
            errMsg = "the provided database file '%s' does not exist" % self.db
            raise AnkabFilePathException(errMsg)

    def connect(self):
        errMsg = "'connect' method must be defined "
        errMsg += "inside the specific DBMS plugin"
        raise AnkabUndefinedMethod(errMsg)

    def fetchall(self):
        errMsg = "'fetchall' method must be defined "
        errMsg += "inside the specific DBMS plugin"
        raise AnkabUndefinedMethod(errMsg)

    def execute(self, query):
        errMsg = "'execute' method must be defined "
        errMsg += "inside the specific DBMS plugin"
        raise AnkabUndefinedMethod(errMsg)

    def select(self, query):
        errMsg = "'select' method must be defined "
        errMsg += "inside the specific DBMS plugin"
        raise AnkabUndefinedMethod(errMsg)
