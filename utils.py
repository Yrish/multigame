from managers import Asset as AssetManager

class Utils:
    """
    Holds utilities for the game and repetitive analysis
    Utils class is static!
    """

    @staticmethod
    def multiIndex(lis, obj):
        """
        Args:
            lis = any list
            obj = any object to search the list for
        returns a list of indexes the obj was found at,
        returns an empty lis if the object does not appear in the list
        """
        ret = []
        for i in range(lis.count(obj)):
            off = 0
            if len(ret) != 0:
                off = ret[-1] + 1
            try:
                ret.append(lis.index(obj, off))
            except ValueError:
                return ret
        return ret

    @staticmethod
    def newDefaultManagers():
        return {"Asset":AssetManager()}
