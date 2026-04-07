import numpy as np
import matplotlib.pyplot as plt

global_hash_growth_list = [0.02, 0.1, 0.5, 2, 4, 8, 10]
expected_event_interval_list = []
t_ref = 600
t = 1


def plot_expected_hash_growth():
    for sigma in global_hash_growth_list:
        expected_event_interval = t_ref * ((1 - np.exp(-sigma * t)) / (sigma * t))
        expected_event_interval_list.append(expected_event_interval)
        print(expected_event_interval)

    plt.figure(figsize=(8, 5))

    plt.plot(
        global_hash_growth_list,
        expected_event_interval_list,
        marker="o",
        color="orange",
        label="Event interval",
    )

    plt.axhline(y=600, linestyle="--", color="black", label="Reference (600 sec)")

    plt.xlabel("Growth rate σ")
    plt.ylabel("Expected event time [sec]")
    plt.title("Expected event time under exponential hash-rate growth")

    plt.legend()
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    plot_expected_hash_growth()
