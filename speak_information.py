#!/usr/bin/env python
from gtts import gTTS
import subprocess

def speak(speech, name):
    info_tts = gTTS(text=speech, lang="en", slow=False)
    info_tts.save(name + ".mp3")

    subprocess.run(["play", "-q", name + ".mp3"])


def speak_full_info(temperature_data=None, temperature_statistics=None, pressure_data=None, pressure_statistics=None, humidity_data=None, humidity_statistics=None,data_polling=None):
    if len(temperature_data) == 0 or len(pressure_data) == 0 or len(humidity_data) == 0:
        cur_full_info = "No polling has taken place. Please wait a few moments."
    elif len(temperature_data) == 1 or len(pressure_data) == 1 or len(humidity_data) == 1:
        cur_full_info = "Only one poll has taken place. Please wait at least {} seconds for the next poll.".format(
            data_polling)
    else:
        cur_full_info = "Latest: {:.0f} Fahrenheit {}, with {} evidence, over about {} degrees; " \
                        "pressure: {:.0f} hPa {}, with {} evidence, over about {} hectopascals;" \
                        " {:.0f} % relative humidity {}, with {} evidence,  over about {} %.".format(temperature_data[-1],
                                                                                                     temperature_statistics["r-value"]["relationship"],
                                                                                                     temperature_statistics["p-value"]["evidence"],
                                                                                                     temperature_statistics["approx delta"]["string"],
                                                                                                     pressure_data[-1],
                                                                                                     pressure_statistics["r-value"]["relationship"],
                                                                                                     pressure_statistics["p-value"]["evidence"],
                                                                                                     pressure_statistics["approx delta"]["string"],
                                                                                                     humidity_data[-1],
                                                                                                     humidity_statistics["r-value"]["relationship"],
                                                                                                     humidity_statistics["p-value"]["evidence"],
                                                                                                     humidity_statistics["approx delta"]["string"])
    speak(cur_full_info, "cur_full_info")


def speak_info(temperature_data, pressure_data, humidity_data):
    if len(temperature_data) == 0 or len(pressure_data) == 0 or len(humidity_data) == 0:
        cur_info = "No polling has taken place. Please wait a few moments."
    else:
        cur_info = "Latest: {0:.0f} Fahrenheit, pressure: {1:.0f} hPa,{2:.0f} % relative humidity".format(temperature_data[-1],
                                                                                                          pressure_data[-1],
                                                                                                          humidity_data[-1])
    speak(cur_info, "cur_info")