import enum

class MergeMethod(enum.Enum):
    HTP = "HTP"
    LTP = "LTP"
    PRIO = "PRIO"
    RANGE = "RANGE"

class Settings: 
    def __init__(self,reciver_ip:str):
        self.reciver_ip = reciver_ip
        self.FPS  = 44
        self.merge_settings = []


class UniverseRange:
    def __init__(self,from_universe:int,min:int,max:int):
        self.from_universe = from_universe
        self.min = min
        self.max = max

        assert self.min <= self.max
        assert self.min >= 0
        assert self.max <= 512

class MergeSettings:
    def __init__(self,from_universe:list,to_universe:int,method:MergeMethod):
        self.from_universe:int = from_universe
        self.to_universe:list = to_universe
        self.method:MergeMethod = method
        self.send_broadcast:bool = False

        self.__prio:int = None
        self.__range:list = None

    @property
    def range(self):
        return self.__range

    @range.setter
    def range(self, value):
        assert isinstance(value, list)
        for range in value:
            assert isinstance(range, UniverseRange)
        self.__range = value

    @property
    def method(self):
        return self.__method
    
    @method.setter
    def method(self, value):
        assert isinstance(value, MergeMethod) 
        self.__method = value

    @property
    def prio(self):
        return self.__prio
    
    @prio.setter
    def prio(self, value):
        assert self.method == MergeMethod.PRIO
        assert isinstance(value, int) 
        assert prio in self.from_universe
        self.__prio = value