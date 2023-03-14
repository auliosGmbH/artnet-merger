from src.artnet.artnet_reciver import ArtNetReciver


def test_get_local_ip():
    reciver = ArtNetReciver()
    assert reciver.get_local_ip()

def test_get_local_hostname():
    reciver = ArtNetReciver()
    assert reciver.get_local_hostname()
    