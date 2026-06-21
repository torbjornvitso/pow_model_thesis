import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_real_inter_events():
    data_inter_events = pd.read_csv("data/node/inter_events_processed_data.csv")

    delta_t_sec = data_inter_events["delta_t_min"] * 60

    delta_t_sec = delta_t_sec[(delta_t_sec > 0) & (delta_t_sec < 8200)]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(
        delta_t_sec,
        bins=120,
        density=True,
        alpha=0.85,
        color="#f7931a",
        edgecolor="none",
        label="Real inter-event times",
    )

    ax.set_xlim(0, 4000)
    ax.set_xlabel("Inter-event time Δt [sec]", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.set_title("Bitcoin inter-event time distribution (real data)", fontsize=14)

    ax.grid(alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False)

    fig.tight_layout()
    plt.savefig("inter_event_time_distribution_btc.png", dpi=300)
    plt.show()


def plot_windowed_inter_events():
    data_windowed = pd.read_csv("data/node/avg_k_events_processed_data.csv")

    delta_t_obs = data_windowed["avg_t_sec"]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(
        delta_t_obs,
        bins=50,
        density=True,
        alpha=0.85,
        color="#f7931a",
        edgecolor="none",
        label="Windowed averages",
    )

    ax.set_xlabel("Averaged inter-event time $t_{obs}$ [sec]", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.set_title("Averaged inter-event times distribution (Bitcoin data)", fontsize=14)
    ax.axvline(600, color="red", linestyle="--", label="Reference (600 sec)")

    ax.grid(alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False)

    fig.tight_layout()
    plt.savefig("averaged_inter_event_time_distribution_btc.png", dpi=300)
    plt.show()


def plot_real_windowed_dynamics():
    data_windowed = pd.read_csv("data/node/avg_k_events_processed_data.csv")

    t_obs_real_data = data_windowed["avg_t_sec"].to_numpy()
    k = np.arange(len(t_obs_real_data))

    t_ref = 600

    total_avg_time_real = t_obs_real_data.mean()

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        k,
        t_obs_real_data,
        color="#f7931a",
        linewidth=1.5,
        label="Real averaged inter-event time",
    )

    ax.axhline(
        t_ref,
        linestyle="--",
        linewidth=2,
        color="red",
        label=f"Reference ({t_ref:.0f} sec)",
    )

    ax.axhline(
        total_avg_time_real,
        linestyle="--",
        linewidth=2,
        color="black",
        label=f"Real mean ({total_avg_time_real:.1f} sec)",
    )

    ax.set_xlabel("Adjustment window $k$", fontsize=12)
    ax.set_ylabel("Averaged inter-event time $\\Delta t_{obs}$ [sec]", fontsize=12)
    ax.set_title("Evolution of averaged inter-event time (Bitcoin data)", fontsize=14)

    ax.grid(alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False, loc="upper left")

    fig.tight_layout()
    plt.savefig("evolution_of_averaged_inter_event_time.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    plot_real_inter_events()
    plot_windowed_inter_events()
    plot_real_windowed_dynamics()
