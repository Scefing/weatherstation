import matplotlib.pyplot as plt
from random import random

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

def random_label():
    """This is used to create random label for each subplot, since the current deprecated behavior is to reuse
    subplots with the same arguments."""
    return str(random())

def plot_graph(temp_data=None, press_data=None, hum_data=None, outfile=None):

    fig = plt.figure(1, figsize=(1.08, 1.04), dpi=100)

    sp1 = fig.add_subplot(311,label=random_label())
    sp1.plot(temp_data, color="#ff0000", linewidth=1.3)
    set_colors(fig)
    sp1.set_ylabel("T", rotation="horizontal")

    sp2 = fig.add_subplot(312,label=random_label())
    sp2.plot(press_data, color="#ff0000", linewidth=1.3)
    set_colors(fig)
    sp2.set_ylabel("P", rotation="horizontal")

    sp3 = fig.add_subplot(313,label=random_label())
    sp3.plot(hum_data, color="#ff0000", linewidth=1.3)
    set_colors(fig)
    sp3.set_ylabel("H", rotation="horizontal")

    fig.subplots_adjust(hspace=0.25, wspace=0.35)

    plt.savefig(outfile, dpi=100, bbox_inches="tight")