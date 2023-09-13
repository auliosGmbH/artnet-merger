import socket
import numpy as np
import time
from src.artnet.artnet_data_class import RecivedArtNetData, OpCode
from src.artnet.artnet_sender import ArtNetSender
import queue

class ArtNetReciver:
    def __init__(self, port: int = 6454,ip_address: str = None):

        if ip_address != None:
            self.ip_address = ip_address
        else:
            self.ip_address = self.get_local_ip()
        self.__port = port
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__bind_socket_to_local_ip()

        print("ArtNetReciver started on: ", self.ip_address, ":", self.__port)

    def get_local_ip(self) -> str:
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return socket.gethostbyname("")

    def get_local_hostname(self) -> str:
        return socket.gethostname()

    def __bind_socket_to_local_ip(self):
      
        try:
            self.recv_socket.bind((self.ip_address, self.__port))
        except OSError:
            print("Port is already in use")
            self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.recv_socket.bind((self.ip_address, self.__port))
        


    def start_recive(self,artnet_queue: queue.Queue):

        while True:
            data, addr = self.recv_socket.recvfrom(2048)

            if addr[0] == self.__ip:
                continue

            artnet_data  = RecivedArtNetData(data,addr)
            try:
                if artnet_data.op_code_name is OpCode.OpDmx:
                    artnet_queue.put(artnet_data)
                elif artnet_data.op_code_name == OpCode.OpPoll:

                    sender = ArtNetSender(addr[0],port=addr[1],broadcast=False,op_code=OpCode.OpPollReply)
                    sender.send_poll_reply()
                    print("Recived Poll")
                elif artnet_data.op_code_name == OpCode.OpPollReply:
                    #TODO -> use reply
                    print("Recived PollReply")
                    print(artnet_data.__dict__)
                else:
                    #TODO -> handle OpCode.OpTodRequest aka RDM
                    print(artnet_data.op_code_name)
            except:
                print("Error while parsing artnet data")
                pass

            

    