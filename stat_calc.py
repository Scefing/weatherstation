#!/usr/bin/env python
import scipy.stats
import math


def logx_magnitude(number, base=10):
    return int(math.floor(math.log(number, base)))


def calc_delta_exp(data, as_string=False):
    delta = max(data) - min(data)
    if delta > 0:
        if delta < 1:
            mag_delta = logx_magnitude(delta)
            delta_base = round(delta / (10**mag_delta))
        elif delta >= 1:
            rounded_delta = round(delta)

            if math.log(rounded_delta, 10) % 1 == 0:
                delta_base = rounded_delta
                mag_delta = logx_magnitude(rounded_delta, 10)
            else:
                delta_base = rounded_delta
                mag_delta = 1
        else:
            delta_base = 0
            mag_delta = 0

        if as_string:

            return str(delta_base), str(mag_delta)
        else:
            return delta_base, mag_delta
    else:
        if as_string:
            return "0", "0"
        else:
            return 0, 0


def round_first_nonzero(number, exponent):

    if number >= 1:
        return round(number)
    else:
        return round(number, abs(exponent))


def approx_delta(data, as_tts_string=False):
    base, exponent = calc_delta_exp(data, as_string=False)

    rounded_delta = round_first_nonzero(base ** exponent, exponent)

    if as_tts_string:
        if "." in str(rounded_delta):
            return str(rounded_delta).replace(".", " point ")
        else:
            return str(rounded_delta)
    else:
        return rounded_delta


def compute_least_squares(data):
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(data, range(0, len(data)))

    return r_value, p_value


def regression_info(data):

    r_value, p_value = compute_least_squares(data)

    regression_info = {}

    p_data = dict()
    p_data["value"] = p_value
    if p_value <= 0.045:
        p_data["evidence"] = "strong"
        p_data["evidence_symbol"] = "◎"
    elif 0.045 < p_value < 0.055:
        p_data["evidence"] = "uncertain"
        p_data["evidence_symbol"] = "∼"
    elif p_value >= 0.055:
        p_data["evidence"] = "weak"
        p_data["evidence_symbol"] = "✖"
    else:
        p_data["evidence"] = "unknown"
        p_data["evidence_symbol"] = "?"

    regression_info["p-value"] = p_data

    r_data = dict()
    r_data["value"] = r_value
    if r_value == 1:
        r_data["relationship"] = "rising straight up"
        r_data["relationship_symbol"] = "⇑"
    elif 0.7 <= r_value < 1:
        r_data["relationship"] = "rising strongly"
        r_data["relationship_symbol"] = "↑↑↑"
    elif 0.5 <= r_value < 0.7:
        r_data["relationship"] = "rising moderately"
        r_data["relationship_symbol"] = "↑↑"
    elif 0.3 < r_value < 0.5:
        r_data["relationship"] = "rising weakly"
        r_data["relationship_symbol"] = "↑"
    elif -0.3 <= r_value <= 0.3 and r_value != 0:
        r_data["relationship"] = "wavering"
        r_data["relationship_symbol"] = "⇝"
    elif r_value == 0:
        r_data["relationship"] = "unchanging"
        r_data["relationship_symbol"] = "→"
    elif -0.3 < r_value < -0.5:
        r_data["relationship"] = "falling weakly"
        r_data["relationship_symbol"] = "↓"
    elif 0.5 <= r_value < 0.7:
        r_data["relationship"] = "falling moderately"
        r_data["relationship_symbol"] = "↓↓"
    elif -0.7 <= r_value < -1:
        r_data["relationship"] = "falling strongly"
        r_data["relationship_symbol"] = "↓↓↓"
    elif r_value == -1:
        r_data["relationship"] = "falling straight down"
        r_data["relationship_symbol"] = "⇓"
    else:
        r_data["relationship"] = "unknown direction"
        r_data["relationship_symbol"] = "⟳"

    regression_info["r-value"] = r_data

    return regression_info


def full_statistics(data):

    base_stats = regression_info(data)

    base_stats["approx delta"] = {}

    base_stats["approx delta"]["string"] = approx_delta(data, as_tts_string=True)
    base_stats["approx delta"]["int"] = approx_delta(data, as_tts_string=False)

    return base_stats

def calc_statistics(temperature_data=None, temperature_statistics=None, pressure_data=None, pressure_statistics=None, humidity_data=None, humidity_statistics=None,condition_flag=None):

    while True:
        condition_flag.acquire()
        condition_flag.wait()
        condition_flag.release()

        temperature_statistics.update(full_statistics(temperature_data))
        pressure_statistics.update(full_statistics(pressure_data))
        humidity_statistics.update(full_statistics(humidity_data))
