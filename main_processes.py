#!/usr/bin/env python
from multiprocessing import Manager, Process
from datetime import datetime
import time
import progressbar
import touchphat

from pilconvert import palette_convert
from tpf_60 import sensing
from plot_graphs import plot_graph
from inky_write import show_tpf_image, show_weather_image
from stat_calc import calc_statistics
from speak_information import speak_info, speak_full_info, speak_screen_change

@touchphat.on_touch("A")
def handle_a():
    global speak_values
    speak_values = True

@touchphat.on_touch("B")
def handle_b():
    global speak_all_values
    speak_all_values = True

@touchphat.on_touch("Enter")
def handle_enter():
    global screen_change_press
    screen_change_press += 1

class Weather:

    def __init__(self, image_file=None, screen_polling_time=60, sleep_time=1, data_polling_time=1, data_limit=60,
                 data_timeout=None):

        manager = Manager()

        self.temperature_data = manager.list()
        self.pressure_data = manager.list()
        self.humidity_data = manager.list()

        self.temperature_statistics = manager.dict()
        self.pressure_statistics = manager.dict()
        self.humidity_statistics = manager.dict()
        self.cur_screen = manager.list()
        self.cur_screen.append(0)

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



    def run(self):
        global speak_values
        global speak_all_values
        global screen_change_press

        sensor = Process(target=sensing, args=(self.temperature_data, self.pressure_data, self.humidity_data, self.data_polling, self.data_limit, self.data_timeout, self.calculate_condition), daemon=True)
        sensor.start()

        calc_stat = Process(target=calc_statistics, kwargs=dict(temperature_data=self.temperature_data,
                                                                temperature_statistics=self.temperature_statistics,
                                                                pressure_data=self.pressure_data,
                                                                pressure_statistics=self.pressure_statistics,
                                                                humidity_data=self.humidity_data,
                                                                humidity_statistics=self.humidity_statistics,
                                                                condition_flag=self.calculate_condition), daemon=True)
        calc_stat.start()

        time_mark = datetime.now()
        bar = progressbar.ProgressBar(widgets=["Polling: ", progressbar.AnimatedMarker()], max_value=progressbar.UnknownLength)
        while True:
            if speak_values:
                speak_values = False

                spk_info = Process(target=speak_info, kwargs=dict(temperature_data=self.temperature_data,
                                                                           pressure_data=self.pressure_data,
                                                                           humidity_data=self.humidity_data), daemon=True)


                spk_info.start()

            elif speak_all_values:
                speak_all_values = False

                spk_all_info = Process(target=speak_full_info, kwargs=dict(temperature_data=self.temperature_data,
                                                                  temperature_statistics=self.temperature_statistics,
                                                                  pressure_data=self.pressure_data,
                                                                  pressure_statistics=self.pressure_statistics,
                                                                  humidity_data=self.humidity_data,
                                                                  humidity_statistics=self.humidity_statistics,
                                                                  data_polling=self.data_polling), daemon=True)

                spk_all_info.start()

            if screen_change_press >= 1:
                screen_changes = screen_change_press
                screen_change_press = 0

                self.cur_screen.append((self.cur_screen[0] + screen_changes) % 4)
                self.cur_screen.pop(0)

                spk_changing_screen = Process(target=speak_screen_change, args=(self.cur_screen,), daemon=True)
                spk_changing_screen.start()

            date_delta = datetime.now() - time_mark
            if date_delta.total_seconds() >= self.polling_time:
                bar.finish()

                time_mark = datetime.now()
                print(time_mark)

                if self.cur_screen[0] == 0:

                    cur_info = "Latest: {0:.2f} F,{1:.2f} hPa,{2:.3f} %RH".format(self.temperature_data[-1],
                                                                                  self.pressure_data[-1],
                                                                                  self.humidity_data[-1])
                    print(cur_info)

                    plot_graph(self.temperature_data, self.pressure_data, self.humidity_data, self.image_file)
                    palette_convert(self.image_file)

                    inky_show = Process(target=show_tpf_image, args=(self.image_file, self.temperature_data,
                                                                     self.pressure_data, self.humidity_data), daemon=True)
                    inky_show.start()
                else:
                    inky_show = Process(target=show_weather_image, daemon=True)
                    inky_show.start()

                bar.start()

            else:
                bar.update(date_delta.total_seconds())
            time.sleep(self.sleep_time)


if __name__ == "__main__":
    speak_values = False
    speak_all_values = False
    screen_change_press = 0

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

