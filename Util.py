import sys
import getpass

class Util(object):
    __isDebugMode = False
    def __init__(self) -> None:
        pass

    @classmethod
    def isDebugMod(cls)->bool:
        if sys.gettrace() or cls.__isDebugMode:
            return True
        else:
            return False

    @classmethod
    def enableDebugMode(cls)->None:
        cls.__isDebugMode = True

    @staticmethod
    def getCurrentUser()->str:
        return getpass.getuser()
