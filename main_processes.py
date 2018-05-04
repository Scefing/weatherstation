#!/usr/bin/env python
from multiprocessing import Manager, Pool, Pipe
from datetime import datetime
import time
import progressbar
from gtts import gTTS
import subprocess
from pilconvert import palette_convert
from tpf_60 import sensing
from plot_graphs import plot_graph
from inky_write import show_image
from stat_calc import full_statistics
import touchphat

@touchphat.on_touch("A")
def handle_a():
    global speak_values
    speak_values = True

@touchphat.on_touch("B")
def handle_b():
    global speak_all_values
    speak_all_values = True

class Weather:

    def __init__(self, image_file=None, screen_polling_time=60, sleep_time=1, data_polling_time=1, data_limit=60, data_timeout=None):
        self.pool = Pool(8)

        manager = Manager()

        self.temperature_data = manager.list()
        self.pressure_data = manager.list()
        self.humidity_data = manager.list()

        self.temperature_statistics = manager.dict()
        self.pressure_statistics = manager.dict()
        self.humidity_statistics = manager.dict()

        self.calculate_condition = manager.Condition()

        self.image_file = image_file
        self.data_polling = data_polling_time
        self.data_timeout = data_timeout
        self.data_limit = data_limit

        if screen_polling_time < 20:
            raise ValueError("Polling time cannot be less 20s, the refresh rate of the screen.")
        if data_polling_time > screen_polling_time:
            raise ValueError("Data must be polled at least once per screen refresh.")
        if screen_polling_time/data_polling_time > 60:
            UserWarning("Data will show the last {} seconds, but only be polled every {} seconds.".format(data_polling_time * 60, screen_polling_time))
        if screen_polling_time/data_polling_time > 180:
            raise ValueError("Too much data will be lost in between screen refreshes (120+ data points).")
        self.polling_time = screen_polling_time

        if sleep_time > 60:
            UserWarning("Sleeping longer than 60s will mean that the screen updates less than once per minute.")
        self.sleep_time = sleep_time

    def speak(self, speech, name):

        info_tts = gTTS(text=speech, lang="en", slow=False)
        info_tts.save(name + ".mp3")

        subprocess.run(["play", "-q", name + ".mp3"])

    def speak_full_info(self):
        if len(self.temperature_data) == 0 or len(self.pressure_data) == 0 or len(self.humidity_data) == 0:
            cur_full_info = "No polling has taken place. Please wait a few moments."
        elif len(self.temperature_data) == 1 or len(self.pressure_data) == 1 or len(self.humidity_data) == 1:
            cur_full_info = "Only one poll has taken place. Please wait at least {} seconds for the next poll.".format(self.data_polling)
        else:
            cur_full_info = "Latest: {:.0f} Fahrenheit {}, with {} evidence, over about {} degrees; " \
                            "pressure: {:.0f} hPa {}, with {} evidence, over about {} hectopascals;" \
                            " {:.0f} % relative humidity {}, with {} evidence,  over about {} %.".format(self.temperature_data[-1],
                                                                                                         self.temperature_statistics["r-value"]["relationship"],
                                                                                                         self.temperature_statistics["p-value"]["evidence"],
                                                                                                         self.temperature_statistics["approx delta"]["string"],
                                                                                                         self.pressure_data[-1],
                                                                                                         self.pressure_statistics["r-value"]["relationship"],
                                                                                                         self.pressure_statistics["p-value"]["evidence"],
                                                                                                         self.pressure_statistics["approx delta"]["string"],
                                                                                                         self.humidity_data[-1],
                                                                                                         self.humidity_statistics["r-value"]["relationship"],
                                                                                                         self.humidity_statistics["p-value"]["evidence"],
                                                                                                         self.humidity_statistics["approx delta"]["string"])
        self.speak(cur_full_info, "cur_full_info")

    def speak_info(self):
        if len(self.temperature_data) == 0 or len(self.pressure_data) == 0 or len(self.humidity_data) == 0:
            cur_info = "No polling has taken place. Please wait a few moments."
        else:
            cur_info = "Latest: {0:.0f} Fahrenheit, pressure: {1:.0f} hPa,{2:.0f} % relative humidity".format(self.temperature_data[-1],
                                                                                                              self.pressure_data[-1],
                                                                                                              self.humidity_data[-1])
        self.speak(cur_info, "cur_info")

    def calc_statistics(self):

        while True:
            self.calculate_condition.acquire()
            self.calculate_condition.wait()
            self.calculate_condition.release()

            self.temperature_statistics.update(full_statistics(self.temperature_data))
            self.pressure_statistics.update(full_statistics(self.pressure_data))
            self.humidity_statistics.update(full_statistics(self.humidity_data))

    def run(self):
        global speak_values
        global speak_all_values
        self.pool.apply_async(func=sensing, args=(self.temperature_data, self.pressure_data, self.humidity_data, self.data_polling, self.data_limit, self.data_timeout, self.calculate_condition))

        time_mark = datetime.now()
        bar = progressbar.ProgressBar(widgets=["Polling: ", progressbar.AnimatedMarker()], max_value=progressbar.UnknownLength)
        while True:
            if speak_values:
                speak_values = False

                self.pool.apply_async(func=self.speak_info)

            elif speak_all_values:
                speak_all_values = False

                self.pool.apply_async(func=self.speak_full_info)

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

                self.pool.apply_async(func=show_image, args=(self.image_file, self.temperature_data,
                                                             self.pressure_data, self.humidity_data))

                bar.start()

            else:
                bar.update(date_delta.total_seconds())
            time.sleep(self.sleep_time)


if __name__ == "__main__":
    speak_values = False
    speak_all_values = False

    while True:
        try:
            long_short = input("Short (1), long (2), or day-long (3) [default: 1]?")

            if long_short == "1" or long_short == "":
                dt_polling_time = 1
                scr_polling_time = 60
                dt_limit = 60
                break
            elif long_short == "2":
                dt_polling_time = 60
                scr_polling_time = 60
                dt_limit = 60
            elif long_short == "3":
                dt_polling_time = 60
                scr_polling_time = 60
                dt_limit = 1440
                break
            else:
                "Select 1, 2, or 3."
        except KeyboardInterrupt:
            pass

    w = Weather(image_file="test.png", data_polling_time=dt_polling_time, screen_polling_time=scr_polling_time, sleep_time=1, data_limit=dt_limit)
    w.run()

