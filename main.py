from src.artnet_reciver import ArtNetReciver
from src.merge_and_send import MergeAndSend
import argparse
from src.settings import Settings, MergeSettings,MergeMethod,UniverseRange
import queue
from zeroconf import ServiceBrowser, Zeroconf
import threading

from src.mdns_listener import MdnsListener

from src.serialization import SerializeObj


def start_artnet_reciver(incomming_data_queue: queue.Queue):
    recv = ArtNetReciver()
    recv.start_recive(incomming_data_queue)

def start_mdns_listener() -> MdnsListener:
    zeroconf = Zeroconf()
    listener = MdnsListener()
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)

    return listener

import json
if __name__ == "__main__":

    # settings 
    # settings = Settings("169.254.216.70")

    # settings.merge_settings.append(MergeSettings([0,1],1,MergeMethod.RANGE))
    # settings.merge_settings[0].range = [UniverseRange(0,0,500),UniverseRange(1,0,512)]


    obj = SerializeObj()

    obj.load_json(path="settings.json")

    settings = json.loads(obj.json,object_hook=Settings.from_json)

    # start mdns listener
    mdns_listener = start_mdns_listener()

    incomming_data_queue = queue.Queue()

    merge_and_send = MergeAndSend(settings)

    recv_thread = threading.Thread(target=start_artnet_reciver,args=(incomming_data_queue,),daemon=True)
    recv_thread.start()
    
    merge_and_send.start_merge_universes(incomming_data_queue)