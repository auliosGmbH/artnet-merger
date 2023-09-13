from dataclasses import dataclass
import time
import enum
import struct

class OpCode(enum.Enum):
    OpPoll = 0x2000
    OpPollReply = 0x2100
    OpDiagData = 0x2300
    OpCommand = 0x2400

    OpDmx = 0x5000
    OpNzs = 0x5100
    OpSync = 0x5200

    OpAddress = 0x6000
    OpInput = 0x7000

    OpTodRequest = 0x8000
    OpTodData = 0x8100
    OpTodControl = 0x8200
    OpRdm = 0x8300
    OpRdmSub = 0x8400

    OpVideoSetup = 0xa010
    OpVideoPalette = 0xa020
    OpVideoData = 0xa040
    
    OpMacMaster = 0xf000
    OpMacSlave = 0xf100

    OpFirmwareMaster = 0xf200
    OpFirmwareReply = 0xf300
    OpFileTnMaster = 0xf400
    OpFileFnMaster = 0xf500
    OpFileFnReply = 0xf600
    OpIpProg = 0xf800
    OpIpProgReply = 0xf900

    OpMedia = 0x9000
    OpMediaPatch = 0x9100
    OpMediaControl = 0x9200
    OpMediaContrlReply = 0x9300

    OpTimeCode = 0x9700
    OpTimeSync = 0x9800
    OpTrigger = 0x9900

    OpDirectory = 0x9a00
    OpDirectoryReply = 0x9b00

class RecivedArtNetData:
    def __init__(self,raw_data:bytearray,sender_addr:str):
        self.raw_data : bytes = raw_data
        self.sender_ip : str = sender_addr[0]
        self.sender_port : int = sender_addr[1]

        self.header : bytes = raw_data[0:18]

        self.op_code = (self.raw_data[9] << 8) | self.raw_data[8]
        self.op_code_name = OpCode(self.op_code)

        if self.op_code_name == OpCode.OpPollReply:
            self.ip : str = str(self.raw_data[10]) + "." + str(self.raw_data[11]) + "." + str(self.raw_data[12]) + "." + str(self.raw_data[13])
            self.port : int = (self.raw_data[15] << 8) | self.raw_data[14]

            self.ver_hi : int = self.raw_data[16]
            self.ver_lo : int = self.raw_data[17]

            self.net_switch : int = self.raw_data[18]
            self.sub_switch : int = self.raw_data[19]

            self.oem_hi : int = self.raw_data[20]
            self.oem_lo : int = self.raw_data[21]

            self.ubea_version : int = self.raw_data[22]

            self.status1 : int = self.raw_data[23]

            self.esta_man_lo : int = self.raw_data[24]
            self.esta_man_hi : int = self.raw_data[25]

            self.short_name : str = self.raw_data[26:44].decode("utf-8") # 18 bytes

            self.long_name : str = self.raw_data[44:108].decode("utf-8") # 64 bytes

            self.node_report : str = self.raw_data[108:172].decode("utf-8") # 64 bytes

            self.num_ports_hi : int = self.raw_data[172]
            self.num_ports_lo : int = self.raw_data[173]

            self.port_types : list = self.raw_data[174:178] # 4 bytes

            self.good_input : list = self.raw_data[178:182] # 4 bytes
            self.good_output : list = self.raw_data[182:186] # 4 bytes

            self.swin : list = self.raw_data[186:190] # 4 bytes
            self.swout : list = self.raw_data[190:194] # 4 bytes

            self.style : int = self.raw_data[200]
            self.mac : str = self.raw_data[201:207]

            self.status2 = self.raw_data[212]


        if self.op_code_name == OpCode.OpPoll:
            self.flags = self.raw_data[12]
            self.priority = self.raw_data[13]

        if self.op_code_name == OpCode.OpDmx:

            self.prot_ver_hi : int = self.raw_data[10]
            self.prot_ver_lo : int = self.raw_data[11]

            self.sequence : int = raw_data[12]

            self.universe : int = int.from_bytes(raw_data[14:15], "big") 
            self.physical : int = raw_data[13]

            self.length: int = (self.raw_data[16] << 8) | self.raw_data[17]

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


