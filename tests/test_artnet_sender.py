import random
import numpy as np
from src.artnet.artnet_sender import ArtNetSender
from src.artnet.artnet_data_class import OpCode 


class MockSocket:
    def __init__(self):
        self.data = []

    def sendto(self, packet, destination):
        self.data = [packet, destination]


def create_ArtNetSender():
    my_mock_socket = MockSocket()
    my_artnet_sender = ArtNetSender("127.0.0.1", 6454, 0, False,my_mock_socket,op_code=OpCode.OpDmx)
    return [my_artnet_sender, my_mock_socket]


def test_init_header():
    my_artnet_sender = create_ArtNetSender()[0]
    header = bytearray()
    header.extend(bytearray("Art-Net", "utf8"))
    array_header = [0x0, 0x00, 0x50, 0x0, 14, 0, 0x00, 0, 0, 2, 0]

    for item in array_header:
        header.append(item)

    assert my_artnet_sender.header == header


def test_send_data():
    tmp = create_ArtNetSender()
    my_artnet_sender = tmp[0]
    my_mock_socket = tmp[1]

    test_data = []
    for i in range(512):
        test_data.append(random.randrange(999))
    my_artnet_sender.send_data(test_data)

    art_net_data = np.pad(test_data, (0, 512 - len(test_data)), mode="constant")

    art_net_data = np.clip(art_net_data, 0, 255).astype(np.uint8)

    packet = bytearray()
    packet.extend(my_artnet_sender.header)
    packet.extend(bytearray(art_net_data))

    assert my_mock_socket.data[0] == packet
    assert my_mock_socket.data[1] == (
        my_artnet_sender.ip_address,
        my_artnet_sender.port,
    )
