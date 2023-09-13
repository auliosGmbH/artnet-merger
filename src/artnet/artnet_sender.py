"""
Device Controller class for controlling the unity simulator over art net
"""

import socket
import numpy as np
from src.clock import Clock
from src.artnet.artnet_data_class import OpCode

import struct
from struct import pack_into
ARTNET_FPS = 44

ARTNET_STRING = b'Art-Net\x00'


class ArtNetSender():
    def __init__(
        self,
        ip_address: str,
        port: int = 6454,
        universe_id: int = 0,
        broadcast: bool = False,
        input_socket=None,
        fps: int = 0,
        op_code: OpCode = OpCode.OpDmx,
    ):
        self.__ip_address = ip_address
        self.__port = port
        self.__broadcast = broadcast
        self.op_code = op_code

        if input_socket is None:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if input_socket is None and broadcast:
            self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        elif input_socket:
            self.__socket = input_socket

        self.__header = bytearray()
        self.__init_header(universe_id)

        if fps > 0:        
            self.__clock = Clock(fps)
        else:
            self.__clock = None

        self.__last_packet= None
        self.__header_sequence = 0

    def __get_local_ip(self) -> str:
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return socket.gethostbyname("")

    @property
    def header(self) -> bytearray:
        return self.__header

    @property
    def ip_address(self) -> str:
        return self.__ip_address

    @property
    def port(self) -> int:
        return self.__port

    @property
    def broadcast(self) -> bool:
        return self.__broadcast

    def __str__(self):
        return f"ArtNetSender(ip_address={self.__ip_address}, port={self.__port}, broadcast={self.__broadcast})"

    def __add_default_header(self, data: bytearray) -> bytearray:

        pack_into("8s", data, 0,ARTNET_STRING)
        pack_into("H", data, 8,self.op_code.value)
        return data

    def __init_header(self, universe_id: int=None):

        if self.op_code == OpCode.OpPollReply:
            packet = bytearray(239)
            self.__add_default_header(packet)

            ip_address = self.__get_local_ip()
            ip_bytes = bytes(map(int, ip_address.split('.')))

            pack_into("4s", packet, 10,ip_bytes)

            pack_into("B", packet, 23,0b00000000) # status 1


            short_name = "Alex - test" # max 18
            short_name = short_name.encode("utf-8")
            short_name = short_name + b"\x00" * (18 - len(short_name))
            pack_into("18s", packet, 26,short_name)

            long_name = "Alex - Merge Artnet Data" # max 64
            long_name = long_name.encode("utf-8")
            long_name = long_name + b"\x00" * (64 - len(long_name))
            pack_into("64s", packet, 44,long_name)


            self.__header.extend(packet)

        if self.op_code == OpCode.OpDmx:
            packet = bytearray(10)
            self.__add_default_header(packet)

            self.header.extend(packet)

            self.__header.extend([ 0x0, 14, 0, 0x00])
            self.__header.extend(self.__extract_mbs_and_lsb(universe_id)[::-1])
            self.__header.extend(self.__extract_mbs_and_lsb(512))


        if self.op_code == OpCode.OpPoll:
            packet = bytearray(10)
            self.__add_default_header(packet)
            self.header.extend(packet)

            self.__header.extend(self.__get_version())
            flags = 0b00000010
            self.__header.extend([flags, 0x0])
                 
    def __get_version(self):
        return [0x0, 14]

    def __extract_mbs_and_lsb(self, number):
        low = number & 0xFF
        high = (number >> 8) & 0xFF
        return [high, low]

    def __increase_sequence(self):
        self.__header_sequence += 1
        if self.__header_sequence > 255:
            self.__header_sequence = 0
        self.__header[12] = self.__header_sequence

    def __transform_data(self, data: list):
        if 1 <= len(data) <= 512:
            # transform data
            art_net_data = np.pad(data, (0, 512 - len(data)), mode="constant")
            art_net_data = np.clip(art_net_data, 0, 255).astype(np.uint8)

            packet = bytearray()
            self.__increase_sequence()
            packet.extend(self.__header)
            packet.extend(bytearray(art_net_data))

            return packet
        raise Exception("Given Artnet data does not have the right length")

    def send_data(self, data: list):

        packet = self.__transform_data(data)
        self.__last_data = packet

        # send data
        self.__socket.sendto(packet, (self.__ip_address, self.__port))
        if self.__clock:
            self.__clock.sleep()

    def send_poll(self):

        assert self.op_code == OpCode.OpPoll, "OpCode is not OpPoll"
        assert self.__broadcast, "Broadcast is not set to True"

        self.__socket.sendto(self.__header, (self.ip_address, self.__port))
        print("sent poll")

    def send_poll_reply(self):
        self.__socket.sendto(self.__header, (self.ip_address, self.__port))
        print("sent poll reply ")

