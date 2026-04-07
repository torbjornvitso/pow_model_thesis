import matplotlib.pyplot as plt

from data_io import read_dataset_eth, read_sim_data

hash_rate_real_data = []
difficulty_real_data = []
t_obs_real_data = []
t_total = []

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


def eth_plot_sim_data(
    t_ref: int, processed_dataset_path: str, sim_data_results_path: str
):

    read_dataset_eth(
        processed_dataset_path, hash_rate_real_data, difficulty_real_data, t_total
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

    total_avg_time = 0

    for t in t_obs_sim_data:
        total_avg_time += t

    total_avg_time = total_avg_time / len(t_obs_sim_data)

    total_real_time = 0

    for t in t_total:
        total_real_time += t

    total_real_time = total_real_time / len(t_total)

    print("t_real:", total_real_time)

    for window in delta_t_sim_data:
        for dt in window:
            all_delta_t.append(dt)

    k = range(len(hash_rate_real_data))

    figA, axx = plt.subplots()

    axx.set_xlabel("Step k")
    axx.set_ylabel("Difficulty")
    axx.plot(k, d_sim_data, "--", label="Difficulty sim")
    axx.plot(k, difficulty_real_data, "--", label="Difficulty btc")
    axx.set_yscale("log")
    axx.grid(True)

    axy = axx.twinx()
    axy.set_ylabel("Hash rate [hashes/sec]")
    axy.plot(k, hash_rate_real_data, color="black", label="Hash rate")
    axy.set_yscale("log")

    lines1, labels1 = axx.get_legend_handles_labels()
    lines2, labels2 = axy.get_legend_handles_labels()
    axx.legend(lines1 + lines2, labels1 + labels2, loc="best")

    figA.tight_layout()
    plt.show()

    fig, ax = plt.subplots()

    ax.set_xlabel("Step k")
    ax.set_ylabel("Difficulty")

    ax.plot(k, d_sim_data, "--", label="Difficulty PoW model")
    ax.plot(k, difficulty_real_data, "--", label="Difficulty Ethereum data")

    ax.set_yscale("log")
    ax.grid(True)
    ax.legend(loc="best")

    fig.tight_layout()
    plt.show()

    figB, ax = plt.subplots()

    ax.set_xlabel("Step k")
    ax.set_ylabel("Block time [sec]")
    ax.plot(k, t_obs_sim_data, color="black", label="Block time on kth iteration")
    ax.axhline(
        t_ref,
        linestyle="--",
        color="red",
        label=f"Average real time data: ({total_real_time} sec)",
    )
    ax.axhline(
        total_avg_time,
        linestyle="--",
        color="blue",
        label=f"Average PoW model time data: ({total_avg_time} sec)",
    )
    ax.grid(True)
    ax.legend(loc="best")

    figB.tight_layout()
    plt.show()

    figC, ax = plt.subplots()

    ax.set_xlabel("Block time[sec]")
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

    WINDOW = 2048

    # build expanded window-avg real block time
    t_avg = []
    t_tot = 0.0
    counter = 0
    for dt in t_obs_sim_data:
        t_tot += dt
        counter += 1
        if counter == WINDOW:
            t_avg.append(t_tot / counter)
            counter = 0
            t_tot = 0.0
    if counter != 0:
        t_avg.append(t_tot / counter)

    expanded_t_avg = []
    for i, avg in enumerate(t_avg):
        reps = WINDOW if i < len(t_avg) - 1 else (len(t_total) - WINDOW * i)
        expanded_t_avg.extend([avg] * reps)

    m = min(len(hash_rate_real_data), len(expanded_t_avg))
    k2 = range(m)

    figX, axx = plt.subplots()
    axx.set_xlabel("Block index (within range)")
    axx.set_ylabel(f"Avg block time over {WINDOW} blocks [sec]")
    axx.plot(k2, expanded_t_avg[:m], color="black", label="Δt avg (windowed)")
    axx.grid(True)

    axy = axx.twinx()
    axy.set_ylabel("Hash rate [hashes/sec]")
    axy.plot(k2, hash_rate_real_data[:m], "--", label="Hash rate")
    axy.set_yscale("log")

    lines1, labels1 = axx.get_legend_handles_labels()
    lines2, labels2 = axy.get_legend_handles_labels()
    axx.legend(lines1 + lines2, labels1 + labels2, loc="best")

    figX.tight_layout()
    plt.show()
