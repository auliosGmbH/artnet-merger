import enum

class MergeMethod(str,enum.Enum):
    HTP = "HTP"
    LTP = "LTP"
    PRIO = "PRIO"
    RANGE = "RANGE"

class Settings: 
    def __init__(self,reciver_ip:str):
        self.reciver_ip = reciver_ip
        self.FPS  = 44
        self.merge_settings = []

    def to_json(self):
        return {
            "reciver_ip": self.reciver_ip,
            "FPS": self.FPS,
            "merge_settings": self.merge_settings,
            "__class__": self.__class__.__name__
        }

    @staticmethod
    def from_json(json_data):

        new_class = eval(json_data.get("__class__"))

        obj = object.__new__(new_class,**json_data)

        for key, value in json_data.items():
            if key == "__class__":
                continue
            setattr(obj, key, value)
        return obj


class UniverseRange:
    def __init__(self,from_universe:int,min:int,max:int):
        self.from_universe = from_universe
        self.min = min
        self.max = max

        assert self.min <= self.max
        assert self.min >= 0
        assert self.max <= 512

    def to_json(self):
        return {
            "from_universe": self.from_universe,
            "min": self.min,
            "max": self.max,
            "__class__": self.__class__.__name__
        }

    def __str__(self):
        return f"from_universe: {self.from_universe}, min: {self.min}, max: {self.max}"

class MergeSettings:
    def __init__(self,from_universe:list,to_universe:int,method:MergeMethod):
        self.from_universe:int = from_universe
        self.to_universe:list = to_universe
        self.method:MergeMethod = method
        self.send_broadcast:bool = False

        self.__range:list = None
        self.__prio:int = None

    def to_json(self):
        return {
            "from_universe": self.from_universe,
            "to_universe": self.to_universe,
            "method": self.method,
            "send_broadcast": self.send_broadcast,
            "range": self.range,
            "prio": self.prio,
            "__class__": self.__class__.__name__
        }

    @property
    def range(self):
        return self.__range

    @range.setter
    def range(self, value):
        if value is None:
            self.__range = None
            return
        assert isinstance(value, list)
        for ranges in value:
            assert isinstance(ranges, UniverseRange)
        self.__range = value

    @property
    def method(self):
        return self.__method
    
    @method.setter
    def method(self, value):

        if type(value) == str:
            value = MergeMethod(value)
        assert isinstance(value, MergeMethod) 
        self.__method = value

    @property
    def prio(self):
        return self.__prio
    
    @prio.setter
    def prio(self, value):
        if value is None:
            self.__prio = None
            return
        assert isinstance(value, int) 
        assert value in self.from_universe
        self.__prio = value