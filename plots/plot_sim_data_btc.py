import matplotlib.pyplot as plt
import numpy as np

from data_io import read_dataset_btc, read_sim_data

hash_rate_real_data = []
difficulty_real_data = []
t_obs_real_data = []

h_sim_data = []
d_sim_data = []
p_k_sim_data = []
lambda_k_sim_data = []
t_sim_data = []
delta_t_sim_data = []
t_obs_sim_data = []
e_k_sim_data = []
u_k_sim_data = []
h_g_sim_date = []
exp_event_interval_sim_data = []
estiamted_local_hash_rate = []

all_delta_t = []

estimated_hash_rate_model = []


def plot_sim_data(
    t_ref: int,
    processed_dataset_path: str,
    sim_data_results_path: str,
    from_height: int,
    to_height: int,
    N: int,
):

    read_dataset_btc(
        processed_dataset_path,
        hash_rate_real_data,
        difficulty_real_data,
        h_g_sim_date,
        exp_event_interval_sim_data,
        t_obs_real_data,
    )

    estiamted_local_hash_rate.append(hash_rate_real_data[0])

    print("start:", estiamted_local_hash_rate)

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

    print("var t_obs:", np.var(t_obs_sim_data))

    residuals = np.array(t_obs_sim_data) - np.array(exp_event_interval_sim_data)

    print("var residuals:", np.var(residuals))

    total_avg_time_sim = 0

    for t in t_obs_sim_data:
        total_avg_time_sim += t

    total_avg_time_sim = total_avg_time_sim / len(t_obs_sim_data)

    total_avg_time_real = 0

    for t in t_obs_real_data:
        total_avg_time_real += t

    total_avg_time_real = total_avg_time_real / len(t_obs_real_data)

    for window in delta_t_sim_data:
        for dt in window:
            all_delta_t.append(dt)

    total_exp_event_interval = 0

    for exp_t in exp_event_interval_sim_data:
        total_exp_event_interval += exp_t

    total_exp_event_interval = total_exp_event_interval / (
        len(exp_event_interval_sim_data) - 1
    )

    print("avg_event_interval:", total_exp_event_interval)

    local_expected_event_interval_based_on_local_hash_growth_loss = []
    total_t = 0

    for h_g in h_g_sim_date:
        exp_event_int = t_ref * ((1 - np.exp(-h_g)) / (h_g))
        if h_g == 0:
            exp_event_int = 600
            total_t += exp_event_int
            local_expected_event_interval_based_on_local_hash_growth_loss.append(
                exp_event_int
            )
        else:
            total_t += exp_event_int
            local_expected_event_interval_based_on_local_hash_growth_loss.append(
                exp_event_int
            )
    print("total_time: ", total_t / len(h_g_sim_date))

    global_hash_rate_growth = (
        np.log(hash_rate_real_data[-1] / hash_rate_real_data[0])
    ) / (len(hash_rate_real_data))

    global_expected_event_interval = t_ref * (
        (1 - np.exp(-global_hash_rate_growth)) / (global_hash_rate_growth)
    )

    print("first block:", from_height)
    print("last block:", to_height)
    print("last_hash_rate", hash_rate_real_data[-1])
    print("first_hash_rate", hash_rate_real_data[0])
    print("global_hash-rate-growth: ", global_hash_rate_growth)
    print("global_expected_event_interval: ", global_expected_event_interval)
    print("expected_event_interval: ", total_exp_event_interval)

    for i in range(len(hash_rate_real_data)):
        if i != 0:
            estimated_hash_rate = hash_rate_real_data[0] * np.e ** (
                global_hash_rate_growth * (i + 1)
            )
            estimated_hash_rate_model.append(estimated_hash_rate)
        else:
            estimated_hash_rate = hash_rate_real_data[0] * np.e ** (
                global_hash_rate_growth * (i)
            )
            estimated_hash_rate_model.append(estimated_hash_rate)

    print("estimated_hash_rate_model_lenght:", len(estimated_hash_rate_model))
    k = range(len(hash_rate_real_data))
    print("k", k)

    figA, ax1 = plt.subplots()

    ax1.set_xlabel("Step k")
    ax1.set_ylabel("Difficulty")
    ax1.plot(k, d_sim_data, "--", label="Difficulty PoW model")
    ax1.plot(k, difficulty_real_data, "--", label="Difficulty Bitcoin data")
    ax1.set_yscale("log")
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Hash rate [hashes/sec]")
    ax2.plot(k, hash_rate_real_data, color="black", label="Hash rate")
    ax2.set_yscale("log")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="best")

    figA.tight_layout()
    plt.show()

    fig_hash, ax = plt.subplots()

    ax.set_xlabel("Step k")
    ax.set_ylabel("Hash rate [hashes/sec]")
    ax.plot(
        k,
        estimated_hash_rate_model,
        color="black",
        label="Estimated hash-rate model",
    )
    # ax.plot(
    #     k,
    #     estiamted_local_hash_rate,
    #     color="yellow",
    #     label="Estimated local exponential model",
    # )
    ax.plot(
        k,
        hash_rate_real_data,
        color="orange",
        label="Hash-rate real data",
    )
    ax.grid(True)
    ax.legend(loc="best")
    fig_hash.tight_layout()
    plt.show()

    fig_event_time_real, ax = plt.subplots()

    ax.set_xlabel("Step k")
    ax.set_ylabel("Event interval [sec]")
    ax.plot(
        k, exp_event_interval_sim_data, color="red", label="Expected event interval"
    )
    ax.plot(k, t_obs_real_data, color="blue", label="Real event interval")
    ax.grid(True)
    ax.legend(loc="best")

    fig_event_time_real.tight_layout()
    plt.show()

    fig_event_time_sim, ax = plt.subplots()

    ax.set_xlabel("Step k")
    ax.set_ylabel("Hash rate [hashes/sec]")
    ax.plot(k, t_obs_sim_data, color="black", label="Sim event interval")
    ax.plot(
        k, exp_event_interval_sim_data, color="red", label="Expected event interval"
    )
    ax.grid(True)
    ax.legend(loc="best")

    fig_event_time_sim.tight_layout()
    plt.show()

    fig, ax = plt.subplots()

    ax.set_xlabel("Step k")
    ax.set_ylabel("Difficulty")

    ax.plot(k, d_sim_data, "--", label="Difficulty PoW model")
    ax.plot(k, difficulty_real_data, "--", label="Difficulty Bitcoin data")

    ax.set_yscale("log")
    ax.grid(True)
    ax.legend(loc="best")

    fig.tight_layout()
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
    ax.axhline(
        total_avg_time_real,
        linestyle="--",
        color="green",
        label=f"Avg. event interval real: ({total_avg_time_real} sec)",
    )
    ax.axhline(
        global_expected_event_interval,
        linestyle="--",
        color="purple",
        label=f"Expected avg. event interval: ({global_expected_event_interval} sec)",
    )
    # ax.axhline(
    #     total_exp_event_interval,
    #     linestyle="--",
    #     color="orange",
    #     label=f"Expected event interval: ({total_exp_event_interval} sec)",
    # )
    ax.grid(True)
    ax.legend(loc="best")

    figB.tight_layout()
    plt.show()

    figC, ax = plt.subplots()

    ax.set_xlabel("Observed average block time over n events [sec]")
    ax.set_ylabel("Density")

    ax.hist(
        t_obs_sim_data,
        bins=30,
        density=True,
        alpha=1,
        color="black",
        label="Avg. inter-event time in a window k",
    )

    figC.tight_layout()
    plt.show()

    figD, ax = plt.subplots()
    ax.set_xlabel("Inter-event time Δt [sec]")
    ax.set_ylabel("Density")

    ax.hist(
        all_delta_t,
        bins=80,
        density=True,
        alpha=1,
        color="black",
        label="All inter-event times",
    )

    ax.grid(True)
    ax.legend(loc="best")
    figD.tight_layout()
    plt.show()

    # Convert hashes/sec -> EH/s for nicer scale like CoinWarz
    # hash_rate_real_ehs = [h / 1e18 for h in hash_rate_real_data]

    # figH, ax = plt.subplots()
    # ax.set_xlabel("Step k (difficulty adjustment)")
    # ax.set_ylabel("Hash rate [EH/s]")

    # ax.plot(
    #     k,
    #     hash_rate_real_ehs,
    #     color="black",
    #     label="Estimated hash rate (from BTC data)",
    # )
    # ax.grid(True)
    # ax.legend(loc="best")
    # figH.tight_layout()
    # plt.show()
