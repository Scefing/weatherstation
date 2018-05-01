#!/usr/bin/env python
from multiprocessing import Process, Manager
from datetime import datetime
import time
import progressbar
from gtts import gTTS
import subprocess
from pilconvert import palette_convert
from tpf_60 import sensing
from plot_graphs import plot_graph
from inky_write import show_image
import touchphat

@touchphat.on_touch("A")
def handle_a():
    global speaking
    speaking = True

class Weather:

    def __init__(self, image_file, polling_time=60, sleep_time=1, data_polling=1, data_timeout=None):
        manager = Manager()
        self.temperature_data = manager.list()
        self.pressure_data = manager.list()
        self.humidity_data = manager.list()
        self.image_file = image_file
        self.data_polling = data_polling
        self.data_timeout = data_timeout

        if polling_time < 20:
            raise ValueError("Polling time cannot be less 20s, the refresh rate of the screen.")
        if data_polling > polling_time:
            raise ValueError("Data must be polled at least once per screen refresh.")
        if polling_time/data_polling > 60:
            UserWarning("Data will show the last {} seconds, but only be polled every {} seconds.".format(data_polling*60, polling_time))
        if polling_time/data_polling > 180:
            raise ValueError("Too much data will be lost in between screen refreshes (120+ data points).")
        self.polling_time = polling_time

        if sleep_time > 60:
            UserWarning("Sleeping longer than 60s will mean that the screen updates less than once per minute.")
        self.sleep_time = sleep_time

    def speak_info(self):
        cur_info = "Latest: {0:.0f} Fahrenheit, pressure: {1:.0f} hPa,{2:.0f} % relative humidity".format(self.temperature_data[-1],
                                                                                                          self.pressure_data[-1],
                                                                                                          self.humidity_data[-1])
        info_tts = gTTS(text=cur_info, lang="en", slow=False)
        info_tts.save("cur_info.mp3")

        subprocess.run(["play", "-q", "cur_info.mp3"])

    def run(self):
        global speaking
        sensor_process = Process(target=sensing,args=(self.temperature_data, self.pressure_data, self.humidity_data,self.data_polling, self.data_timeout))
        sensor_process.daemon = True
        sensor_process.start()

        time_mark = datetime.now()
        bar = progressbar.ProgressBar(widgets=["Polling: ",progressbar.AnimatedMarker()], max_value=progressbar.UnknownLength)
        while True:
            if speaking:
                speaking = False

                speaker = Process(target=self.speak_info)
                speaker.daemon = True
                speaker.start()

            date_delta = datetime.now() - time_mark
            if date_delta.total_seconds() >= self.polling_time:
                bar.finish()
                time_mark = datetime.now()
                print(time_mark)

                cur_info = "Latest: {0:.2f} F,{1:.2f} hPa,{2:.3f} %RH".format(self.temperature_data[-1],
                                                                              self.pressure_data[-1],
                                                                              self.humidity_data[-1])
                print(cur_info)

                plot_graph(self.temperature_data, self.pressure_data, self.humidity_data, self.image_file)
                palette_convert(self.image_file)

                inky_process = Process(target=show_image, args=(self.image_file, self.temperature_data,
                                                                                 self.pressure_data,
                                                                                 self.humidity_data))
                inky_process.daemon = True
                inky_process.start()

                bar.start()
            else:
                bar.update(date_delta.total_seconds())
            time.sleep(self.sleep_time)


if __name__ == "__main__":
    speaking = False

    w = Weather(image_file="test.png", data_polling=60, polling_time=360, sleep_time=1)
    w.run()


