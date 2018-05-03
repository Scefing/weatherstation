#!/usr/bin/env python
import bme680
import time


def sensing(temp_data=None, press_data=None, hum_data=None, polling=1,, data_limit=60, timeout=None):
    sensor = bme680.BME680()

    # These oversampling settings can be tweaked to
    # change the balance between accuracy and noise in
    # the data.

    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)

    time_total = 0
    while True:
        if sensor.get_sensor_data():
            cel_temp = sensor.data.temperature
            fahr_temp = (cel_temp * 9 / 5) + 32

            temp_data.append(fahr_temp)
            if len(temp_data) > data_limit:
                temp_data.pop(0)

            press_data.append(sensor.data.pressure)
            if len(press_data) > data_limit:
                press_data.pop(0)

            hum_data.append(sensor.data.humidity)
            if len(hum_data) > data_limit:
                hum_data.pop(0)

            if timeout:
                if time_total >= timeout:
                    break
                else:
                    time_total += 1
            time.sleep(polling)
