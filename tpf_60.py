#!/usr/bin/env python
import bme680
import time
import matplotlib.pyplot as plt
from pilconvert import palette_convert
import inkyphat


def set_colors(fig):
    fig.gca().axes.xaxis.set_ticks([])
    fig.gca().axes.yaxis.set_ticks([])
    fig.gca().spines["bottom"].set_color("#000000")
    fig.gca().spines["left"].set_color("#000000")
    fig.gca().spines["top"].set_color("#ffffff")
    fig.gca().spines["right"].set_color("#ffffff")
    fig.gca().spines["bottom"].set_linewidth(1.3)
    fig.gca().spines["left"].set_linewidth(1.3)
    fig.gca().spines["top"].set_linewidth(1.3)
    fig.gca().spines["right"].set_linewidth(1.3)


def sensing(outputfile):
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

        fig = plt.figure(1, figsize=(2.12, 1.04), dpi=100)

        sp1 = plt.subplot(311)
        plt.plot(temps, color="#ff0000", linewidth=1.3)

        set_colors(fig)
        sp1.set_ylabel("T", rotation="horizontal")

        sp2 = plt.subplot(312)
        plt.plot(pressures, color="#ff0000", linewidth=1.3)

        set_colors(fig)
        sp2.set_ylabel("P", rotation="horizontal")

        sp3 = plt.subplot(313)
        plt.plot(humidities, color="#ff0000", linewidth=1.3)

        set_colors(fig)
        sp3.set_ylabel("H", rotation="horizontal")

        plt.subplots_adjust(hspace=0.25, wspace=0.35)

        plt.savefig(outputfile, dpi=100)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    sensing("test.png")
    palette_convert("test.png")
    inkyphat.set_image("test.png")
    inkyphat.show()




