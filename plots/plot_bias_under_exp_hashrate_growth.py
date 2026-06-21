import numpy as np
import matplotlib.pyplot as plt

global_hash_growth_list = [0.02, 0.1, 0.5, 2, 4, 8, 10]
expected_event_interval_list = []
t_ref = 600
t = 1


def plot_expected_hash_growth():
    expected_event_interval_list.clear()

    for sigma in global_hash_growth_list:
        expected_event_interval = t_ref * ((1 - np.exp(-sigma * t)) / (sigma * t))
        expected_event_interval_list.append(expected_event_interval)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        global_hash_growth_list,
        expected_event_interval_list,
        marker="o",
        markersize=5,
        linewidth=2,
        color="#f7931a",
        label="Expected averaged inter-event time",
    )

    ax.axhline(
        y=t_ref,
        linestyle="--",
        linewidth=2,
        color="black",
        label=f"Reference ({t_ref} sec)",
    )

    ax.set_xlabel("Growth rate $\\sigma$", fontsize=12)
    ax.set_ylabel("Expected averaged inter-event time [sec]", fontsize=12)
    ax.set_title(
        "Bias under exponential hash-rate growth",
        fontsize=14,
    )

    ax.grid(alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="lower left")

    fig.tight_layout()
    plt.savefig("expected_event_time_vs_growth.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    plot_expected_hash_growth()
