import matplotlib.pyplot as plt


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

def plot_graph(data=None, outfile=None):

    fig = plt.figure(1, figsize=(2.12, 1.04), dpi=100)

    sp1 = plt.subplot(311)
    plt.plot(data[0], color="#ff0000", linewidth=1.3)

    set_colors(fig)
    sp1.set_ylabel("T", rotation="horizontal")

    sp2 = plt.subplot(312)
    plt.plot(data[1], color="#ff0000", linewidth=1.3)

    set_colors(fig)
    sp2.set_ylabel("P", rotation="horizontal")

    sp3 = plt.subplot(313)
    plt.plot(data[2], color="#ff0000", linewidth=1.3)

    set_colors(fig)
    sp3.set_ylabel("H", rotation="horizontal")

    plt.subplots_adjust(hspace=0.25, wspace=0.35)

    plt.savefig(outfile, dpi=100)