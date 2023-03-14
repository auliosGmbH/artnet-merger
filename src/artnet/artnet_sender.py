"""
Device Controller class for controlling the unity simulator over art net
"""

import socket
import numpy as np
from src.clock import Clock
from src.artnet.artnet_data_class import OpCode

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

    def __init_header(self, universe_id: int):
        self.__header.extend(ARTNET_STRING)

        self.__header.append(self.op_code.value & 0xff)  # low byte of opcode
        self.__header.append(self.op_code.value >> 8)  # high byte of opcode

        if self.op_code == OpCode.OpDmx:
            self.__header.extend([0x00, 0x50])
            self.__header.extend([0x0, 0x00, 0x50, 0x0, 14, 0, 0x00])
            self.__header.extend(self.__extract_mbs_and_lsb(universe_id)[::-1])
            self.__header.extend(self.__extract_mbs_and_lsb(512))       


        if self.op_code == OpCode.OpPoll:
            self.__header.extend(self.__get_version())
            flags = 0b00000010
            self.__header.extend([flags, 0x0])


    def bitsToBytes(self,a):
        s = i = 0
        for x in a:
            s += s + x
            i += 1
            if i == 8:
                yield s
                s = i = 0
        if i > 0:
            yield s << (8 - i)
                 
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
