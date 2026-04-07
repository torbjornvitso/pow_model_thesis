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


def plot_sim_data_shock_test(
    t_ref: int,
    processed_dataset_path: str,
    sim_data_results_path: str,
    from_height: int,
    to_height: int,
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

    figA, ax1 = plt.subplots()

    ax1.set_xlabel("Step k")
    ax1.set_ylabel("Difficulty")
    ax1.plot(k, d_sim_data, "--", label="Difficulty PoW model")
    ax1.plot(k, difficulty_shock_data, "--", label="Difficulty Shock Data")
    ax1.set_yscale("log")
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Hash rate [hashes/sec]")
    ax2.plot(k, hash_rate_shock_data, color="black", label="Hash rate")
    ax2.set_yscale("log")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="best")

    # plt.savefig("hashrate_shock_x8_difficulty.png", bbox_inches="tight")
    figA.tight_layout()
    plt.show()

    figB, ax = plt.subplots()

    ax.set_xlabel("Step k")
    ax.set_ylabel("Average block time [sec]")
    ax.plot(
        k, t_obs_sim_data, color="black", label="Average block time on kth iteration"
    )
    ax.axhline(t_ref, linestyle="--", color="red", label=f"Reference: ({t_ref} sec)")
    ax.axhline(
        total_avg_time_sim,
        linestyle="--",
        color="blue",
        label=f"Avg. event interval sim: ({total_avg_time_sim} sec)",
    )

    ax.grid(True)
    ax.legend(loc="best")

    # plt.savefig("hashrate_shock_x8_event_interval.png", bbox_inches="tight")
    figB.tight_layout()
    plt.show()
