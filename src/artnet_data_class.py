from dataclasses import dataclass
import time
class ArtnetData:
    def __init__(self,raw_data:bytearray,sender_addr:str):
        self.raw_data : bytes = raw_data
        self.sender_ip : str = sender_addr[0]
        self.sender_port : int = sender_addr[1]

        self.header : bytes = raw_data[0:18]
        self.universe : int = int.from_bytes(raw_data[14:15], "big") 
        self.sequence : int = raw_data[12]
        self.physical : int = raw_data[13]

        self.length: int = raw_data[16] * 256 + raw_data[17] # TODO check right conversion for length 

        self.data : bytes =  raw_data[18:]
        self.time = time.perf_counter()


    @property
    def header(self):
        return self.__header

    @property
    def data(self):
        return self.__data

    @header.setter
    def header(self, value):
        assert len(value) == 18
        assert value[0:8] == b'Art-Net\x00'
        self.__header = value

    @data.setter
    def data(self, value):
        assert len(value) == self.length
        self.__data = value

    @property
    def sender_ip(self):
        return self.__sender_ip
    
    @sender_ip.setter
    def sender_ip(self, value):
        assert isinstance(value, str)        
        self.__sender_ip = value

    @property
    def universe(self):
        return self.__universe
    
    @universe.setter
    def universe(self, value):
        assert isinstance(value, int)
        assert 0 <= value <= 65535
        self.__universe = value

    @property
    def sender_port(self):
        return self.__sender_port
    
    @sender_port.setter
    def sender_port(self, value):
        assert isinstance(value, int)
        assert 0 <= value <= 65535
        self.__sender_port = value

    @property
    def sequence(self):
        return self.__sequence
    
    @sequence.setter
    def sequence(self, value):
        assert isinstance(value, int)
        assert 0 <= value <= 255
        self.__sequence = value

    @property
    def physical(self):
        return self.__physical
    
    @physical.setter
    def physical(self, value):
        assert isinstance(value, int)
        assert 0 <= value <= 255
        self.__physical = value

    @property
    def length(self):
        return self.__length
    
    @length.setter
    def length(self, value):
        assert isinstance(value, int)
        assert 0 <= value <= 512
        self.__length = value


