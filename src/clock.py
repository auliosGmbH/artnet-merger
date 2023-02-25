import time
class Clock:
    
    def __init__(self, fps):
        self.start = time.perf_counter()
        self.frame_length = 1/fps
    @property
    def tick(self):
        return int((time.perf_counter() - self.start)/self.frame_length)

    def sleep(self):
        r = self.tick + 1
        while self.tick < r:
            time.sleep(1/1000)
