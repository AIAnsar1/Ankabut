from core.common import Backend, readInput
from core.data import logger
from core.enums import OS
from core.exceptions import AnkabUndefinedMethod


class Fingerprint(object):
    """
    This class defines generic fingerprint functionalities for plugins.
    """

    def __init__(self, dbms):
        Backend.forceDbms(dbms)

    def getFingerprint(self):
        errMsg = "'getFingerprint' method must be defined "
        errMsg += "into the specific DBMS plugin"
        raise AnkabUndefinedMethod(errMsg)

    def checkDbms(self):
        errMsg = "'checkDbms' method must be defined "
        errMsg += "into the specific DBMS plugin"
        raise AnkabUndefinedMethod(errMsg)

    def checkDbmsOs(self, detailed=False):
        errMsg = "'checkDbmsOs' method must be defined "
        errMsg += "into the specific DBMS plugin"
        raise AnkabUndefinedMethod(errMsg)

    def forceDbmsEnum(self):
        pass

    def userChooseDbmsOs(self):
        warnMsg = "for some reason sqlmap was unable to fingerprint "
        warnMsg += "the back-end DBMS operating system"
        logger.warning(warnMsg)

        msg = "do you want to provide the OS? [(W)indows/(l)inux]"

        while True:
            os = readInput(msg, default='W').upper()

            if os == 'W':
                Backend.setOs(OS.WINDOWS)
                break
            elif os == 'L':
                Backend.setOs(OS.LINUX)
                break
            else:
                warnMsg = "invalid value"
                logger.warning(warnMsg)
