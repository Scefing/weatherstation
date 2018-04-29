#!/usr/bin/env python
import bme680
import time
from pilconvert import palette_convert
from plot_graphs import plot_graph
from PIL import Image
import inkyphat


def sensing(temp_data=None, hum_data=None, press_data=None, timeout=None):
    sensor = bme680.BME680()

    # These oversampling settings can be tweaked to
    # change the balance between accuracy and noise in
    # the data.

    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)

    print("Polling:")
    try:
        time_total = 0
        while True:
            if sensor.get_sensor_data():
                cel_temp = sensor.data.temperature
                fahr_temp = (cel_temp * 9 / 5) + 32

                output = "{0:.2f} F,{1:.2f} hPa,{2:.3f} %RH".format(fahr_temp, sensor.data.pressure,
                                                                    sensor.data.humidity)
                temp_data.append(fahr_temp)
                if len(temp_data) > 60:
                    temp_data.pop(0)

                press_data.append(sensor.data.pressure)
                if len(press_data) > 60:
                    press_data.pop(0)

                hum_data.append(sensor.data.humidity)
                if len(hum_data) > 60:
                    hum_data.pop(0)

                print(output)

                if timeout:
                    if time_total >= timeout:
                        break
                    else:
                        time_total += 1
                time.sleep(1)

    except KeyboardInterrupt:
        pass



if __name__ == "__main__":
    temp, press, hum = [],[],[]
    sensing(temp, press, hum, timeout=60)
    plot_graph(temp, press, hum, "test.png")
    palette_convert("test.png")
    inkyphat.paste(Image.open("test.png"))
    inkyphat.show()




