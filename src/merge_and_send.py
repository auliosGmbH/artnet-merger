from src.artnet_data_class import ArtnetData
from src.clock import Clock
from src.settings import Settings, MergeSettings, MergeMethod
from src.artnet_sender import ArtNetSender
import queue
import numpy as np


class MergeAndSend:
    def __init__(self, settings: Settings):
        self.universes = {}
        self.merge_settings = settings.merge_settings
        self.settings = settings

        self.__clock = Clock(settings.FPS)

        self.sender = []
        for merge_settings in self.merge_settings:
            self.sender.append(ArtNetSender(ip_address=settings.reciver_ip,
                               universe_id=merge_settings.to_universe, broadcast=merge_settings.send_broadcast))


    def start_merge_universes(self, incomming_data_queue: queue.Queue):
        while incomming_data_queue.empty():
            self.__clock.sleep()
            # wait for data

        while True:

            for i in range(incomming_data_queue.qsize()):
                data = incomming_data_queue.get()
                self.universes[data.universe] = data

            for idx, merge_settings in enumerate(self.merge_settings):
                res = []

                if merge_settings.method == MergeMethod.HTP:
                    res = self.__merge_htp(merge_settings)

                elif merge_settings.method == MergeMethod.LTP:
                    res = self.__merge_ltp(merge_settings)

                elif merge_settings.method == MergeMethod.PRIO:
                    res = self.__merge_prio(merge_settings)
                elif merge_settings.method == MergeMethod.RANGE:
                    res = self.__merge_range(merge_settings)
                
                self.sender[idx].send_data(res)

            self.__clock.sleep()

    def __merge_ltp(self, merge_settings: MergeSettings):
        pass

    def __merge_prio(self, merge_settings: MergeSettings):
        return self.universes[merge_settings.prio].data

    def __merge_range(self, merge_settings: MergeSettings):
        res = np.zeros(512)
        for range in merge_settings.range:
            if range.from_universe in self.universes:
                res[range.min:range.max] = self.universes[range.from_universe].data[range.min:range.max]
        return res

    def __merge_htp(self, merge_settings: MergeSettings):
        res = []
        for universe in merge_settings.from_universe:
            if universe in self.universes:
                res.append(self.universes[universe].data)

        if len(res) == 0:
            return np.zeros(512)
        res = [max(x) for x in zip(*res)]

        return res
