from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
from src.artnet.artnet_reciver import ArtNetReciver
from src.artnet.artnet_data_class import RecivedArtNetData
from threading import Thread
from queue import Queue
from src.clock import Clock
import sys

class TrackArtnetFps(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.reciver = ArtNetReciver(ip_address="127.0.0.1")
        self.reciver_queue = Queue()
        self.__clock = Clock(44)

        # Set up the graph
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.plot_data = [0] * 512  # assuming 512 channels
        self.curve = self.graphWidget.plot(self.plot_data)
        self.graphWidget.setYRange(0, 255)  # DMX values range from 0 to 255

    def start(self):
        Thread(target=self.reciver.start_recive, args=(self.reciver_queue,), daemon=True).start()

        # Set up a timer to update the graph
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # update every 50 ms

    def update(self):
        while not self.reciver_queue.empty():
            artnet = self.reciver_queue.get()
            data = artnet.data
            
            # Ensure data is bytes, then convert to a list of integers
            if data is not None and isinstance(data, bytes):
                self.plot_data = list(bytearray(data))
                self.curve.setData(self.plot_data)  # Update the curve with the new data
            else:
                print(f"Unexpected data format: {data}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    track = TrackArtnetFps()
    track.start()
    track.show()
    sys.exit(app.exec())
