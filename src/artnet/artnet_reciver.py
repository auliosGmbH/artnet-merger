import socket
import numpy as np
import time
from src.artnet.artnet_data_class import RecivedArtNetData, OpCode
import queue

class ArtNetReciver:
    def __init__(self, port: int = 6454,ip_address: str = None):

        self.__port = port
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__bind_socket_to_local_ip()
        print("ArtNetReciver started on: ", self.get_local_ip(), ":", self.__port)

    def get_local_ip(self) -> str:
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return socket.gethostbyname("")

    def get_local_hostname(self) -> str:
        return socket.gethostname()

    def __bind_socket_to_local_ip(self):
        try:
            self.recv_socket.bind((self.get_local_ip(), self.__port))
        except OSError:
            print("Port is already in use")
            self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.recv_socket.bind((self.get_local_ip(), self.__port))


    def start_recive(self,artnet_queue: queue.Queue):

        while True:
            data, addr = self.recv_socket.recvfrom(2048)
            # TODO -> check addr host addr 


            artnet_data  = RecivedArtNetData(data,addr)
            try:
                if artnet_data.op_code_name == OpCode.OpDmx:
                    artnet_queue.put(artnet_data)
                elif artnet_data.op_code_name == OpCode.OpPoll:
                    #TODO -> send reply
                    print("Recived Poll")
                    print(artnet_data.flags)
                    print(artnet_data.priority)
                    print(data)
                elif artnet_data.op_code_name == OpCode.OpPollReply:
                    #TODO -> use reply
                    print("Recived PollReply")
                    print(data)
                else:
                    #TODO -> handle OpCode.OpTodRequest aka RDM
                    print(artnet_data.op_code_name)
                
            except:
                #print(data)
                print("Error while parsing artnet data")
                pass

            

    