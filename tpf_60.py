#!/usr/bin/env python
import bme680
import time
from pilconvert import palette_convert
from plot_graphs import plot_graph
from PIL import Image
import inkyphat


def sensing(outfile):
    sensor = bme680.BME680()

    # These oversampling settings can be tweaked to
    # change the balance between accuracy and noise in
    # the data.

    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)

    temps = []
    humidities = []
    pressures = []

    print("Polling:")
    try:
        for x in range(0, 60):
            if sensor.get_sensor_data():
                cel_temp = sensor.data.temperature
                fahr_temp = (cel_temp * 9 / 5) + 32

                output = "{0:.2f} F,{1:.2f} hPa,{2:.3f} %RH".format(fahr_temp, sensor.data.pressure,
                                                                    sensor.data.humidity)

                temps.append(fahr_temp)
                pressures.append(sensor.data.pressure)
                humidities.append(sensor.data.humidity)

                print(output)
                time.sleep(1)

    except KeyboardInterrupt:
        pass

    plot_graph(data=[temps, pressures, humidities], outfile=outfile)


if __name__ == "__main__":
    sensing("test.png")
    palette_convert("test.png")
    inkyphat.paste(Image.open("test.png"))
    inkyphat.show()




