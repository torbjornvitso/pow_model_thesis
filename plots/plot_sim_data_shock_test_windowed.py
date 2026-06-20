import matplotlib.pyplot as plt

from data_io import read_dataset_shock_test, read_sim_data

hash_rate_shock_data = []
difficulty_shock_data = []

h_sim_data = []
d_sim_data = []
p_k_sim_data = []
lambda_k_sim_data = []
t_sim_data = []
delta_t_sim_data = []
t_obs_sim_data = []
e_k_sim_data = []
u_k_sim_data = []

all_delta_t = []


def plot_sim_data_shock_test_btc(
    processed_dataset_path: str,
    sim_data_results_path: str,
):

    read_dataset_shock_test(
        processed_dataset_path, hash_rate_shock_data, difficulty_shock_data
    )

    read_sim_data(
        sim_data_results_path,
        h_sim_data,
        d_sim_data,
        p_k_sim_data,
        lambda_k_sim_data,
        delta_t_sim_data,
        t_obs_sim_data,
        e_k_sim_data,
        u_k_sim_data,
    )

    total_avg_time_sim = 0

    for t in t_obs_sim_data:
        total_avg_time_sim += t

    total_avg_time_sim = total_avg_time_sim / len(t_obs_sim_data)

    for window in delta_t_sim_data:
        for dt in window:
            all_delta_t.append(dt)

    k = range(len(hash_rate_shock_data))

    figA, ax1 = plt.subplots(figsize=(8, 5))

    ax1.set_xlabel("Adjustment window $k$", fontsize=12)
    ax1.set_ylabel("Difficulty", fontsize=12)

    ax1.plot(
        k,
        d_sim_data,
        color="#f7931a",
        linewidth=2,
        label="Difficulty (PoW model)",
    )

    ax1.set_yscale("log")
    ax1.grid(alpha=0.2)

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Hash rate [hashes/sec]", fontsize=12)

    ax2.plot(
        k,
        hash_rate_shock_data,
        color="black",
        linewidth=2,
        label="Hash-rate",
    )

    ax2.set_yscale("log")
    ax2.spines["top"].set_visible(False)

    ax1.set_title("Response of difficulty under hash-rate shock", fontsize=14)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, frameon=False, loc="lower left")

    figA.tight_layout()
    plt.savefig("validation_of_control_properties_difficulty.png", dpi=300)
    plt.show()

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.set_xlabel("Adjustment window $k$", fontsize=12)
    ax.set_ylabel("Averaged inter-event time [sec]", fontsize=12)

    ax.plot(
        k,
        t_obs_sim_data,
        color="#f7931a",
        linewidth=2,
        label="Averaged inter-event time",
    )

    ax.grid(alpha=0.2)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.tick_params(left=False)

    ax.set_title(
        "Response of averaged inter-event time under hash-rate shock", fontsize=14
    )
    ax.legend(frameon=False, loc="upper left")

    fig.tight_layout()
    plt.savefig("validation_of_control_properties_event_time.png", dpi=300)
    plt.show()
