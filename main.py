from src.artnet_reciver import ArtNetReciver
from src.merge_and_send import MergeAndSend
import argparse
from src.settings import Settings, MergeSettings,MergeMethod
import queue

import threading

def start_artnet_reciver(incomming_data_queue: queue.Queue):
    recv = ArtNetReciver()
    recv.start_recive(incomming_data_queue)


if __name__ == "__main__":

    # settings 
    settings = Settings("169.254.216.70")
    settings.merge_settings.append(MergeSettings([0,1],1,MergeMethod.HTP))

    incomming_data_queue = queue.Queue()

    merge_and_send = MergeAndSend(settings)

    recv_thread = threading.Thread(target=start_artnet_reciver,args=(incomming_data_queue,),daemon=True)
    recv_thread.start()
    
    merge_and_send.start_merge_universes(incomming_data_queue)


#TODO: search for artnet recivers -> use mdns listener
#TODO: broadcast signal, that you are artnet reciver
