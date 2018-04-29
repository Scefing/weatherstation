from multiprocessing import Process, Manager
from datetime import datetime
import time
from pilconvert import palette_convert
from tpf_60 import sensing
from plot_graphs import plot_graph
from inky_write import show_image

class Weather:

    def __init__(self, image_file, polling_time=60,sleep_time=15):
        manager = Manager()
        self.temperature_data = manager.list()
        self.pressure_data = manager.list()
        self.humidity_data = manager.list()
        self.image_file = image_file

        if polling_time < 20:
            raise ValueError("Polling time cannot be less 20s, the refresh rate of the screen.")
        self.polling_time = polling_time

        if sleep_time > 60:
            UserWarning("Sleeping longer than 60s will mean that the screen updates less than once per minute.")
        self.sleep_time = sleep_time

    def run(self):
        sensor_process = Process(target=sensing,args=(self.temperature_data, self.pressure_data, self.humidity_data))
        sensor_process.daemon = True
        sensor_process.start()

        time_mark = datetime.now()
        while True:
            date_delta = datetime.now() - time_mark
            if date_delta.total_seconds() >= self.polling_time:
                time_mark = datetime.now()

                plot_graph(self.temperature_data, self.pressure_data, self.humidity_data, self.image_file)
                palette_convert(self.image_file)

                inky_process = Process(target=show_image, args=(self.image_file,))
                inky_process.daemon = True
                inky_process.start()

            time.sleep(self.sleep_time)


if __name__=="__main__":
    w = Weather("test.png")
    w.run()