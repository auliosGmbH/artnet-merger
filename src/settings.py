import enum

class MergeMethod(enum.Enum):
    HTP = "HTP"
    LTP = "LTP"
    PRIO = "PRIO"

class Settings: 
    def __init__(self,reciver_ip:str):
        self.reciver_ip = reciver_ip
        self.FPS  = 44
        self.merge_settings = []

class MergeSettings:
    def __init__(self,from_universe:list,to_universe:int,method:MergeMethod):
        self.from_universe = from_universe
        self.to_universe = to_universe
        self.method = method
        self.send_broadcast = False

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