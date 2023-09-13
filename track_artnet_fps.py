import time
from src.artnet.artnet_reciver import ArtNetReciver
from src.artnet.artnet_data_class import RecivedArtNetData
from threading import Thread
from queue import Queue
from src.clock import Clock

class TrackArtnetFps:
    def __init__(self) -> None:
        self.reciver = ArtNetReciver(ip_address="127.0.0.1")
        self.reciver_queue = Queue()
        self.__clock = Clock(44)

        # Dictionary to store timing, frame count, and previous data for each universe
        self.universe_data = {}

    def start(self):
        Thread(target=self.reciver.start_recive, args=(self.reciver_queue,), daemon=True).start()

        # Wait for data
        while self.reciver_queue.empty():
            self.__clock.sleep()

        while True:
            for _ in range(self.reciver_queue.qsize()):
                artnet = self.reciver_queue.get()
                
                universe = artnet.universe
                data = artnet.data

                if universe not in self.universe_data:
                    self.universe_data[universe] = {
                        "frame_count": 0, 
                        "prev_time": time.time(),
                        "prev_data": None, 
                        "changed_frame_count": 0
                    }

                self.universe_data[universe]["frame_count"] += 1

                if self.universe_data[universe]["prev_data"] != data:
                    self.universe_data[universe]["changed_frame_count"] += 1
                self.universe_data[universe]["prev_data"] = data

                current_time = time.time()
                elapsed_time = current_time - self.universe_data[universe]["prev_time"]
                if elapsed_time > 1.0:
                    fps = self.universe_data[universe]["frame_count"] / elapsed_time
                    changed_fps = self.universe_data[universe]["changed_frame_count"] / elapsed_time
                    
                    # Construct the display string with colored numbers
                    display_str = (
                        f"Universe {universe}:\n"
                        f"FPS: \033[92m{fps:.2f}\033[0m\n"
                        f"Changed FPS: \033[92m{changed_fps:.2f}\033[0m\n"
                        f"Time per frame: \033[92m{1000/fps:.2f}\033[0m ms\n"
                        "------------------------\n"
                    )

                    # Use \r to refresh the same line and end='' to prevent a newline after print
                    print(display_str, end='', flush=True)

                    # Reset counts and time
                    self.universe_data[universe]["frame_count"] = 0
                    self.universe_data[universe]["changed_frame_count"] = 0
                    self.universe_data[universe]["prev_time"] = current_time

if __name__ == "__main__":
    track = TrackArtnetFps()
    track.start()
