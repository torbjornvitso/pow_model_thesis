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

    total_avg_time_real = 0

    for t in t_obs_real_data:
        total_avg_time_real += t

    total_avg_time_real = total_avg_time_real / len(t_obs_real_data)

    for window in delta_t_sim_data:
        for dt in window:
            all_delta_t.append(dt)

    global_hash_rate_growth = (
        np.log(hash_rate_real_data[-1] / hash_rate_real_data[0])
    ) / (len(hash_rate_real_data))

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

    k = range(len(hash_rate_real_data))

    # Inter-event time distribution simulated ##

    figA, ax = plt.subplots(figsize=(8, 5))

    ax.hist(
        all_delta_t,
        bins=120,
        density=True,
        alpha=0.85,
        color="black",
        edgecolor="none",
        label="Simulated inter-event times",
    )

    ax.set_xlim(0, 4000)

    ax.set_xlabel("Inter-event time Δt [sec]", fontsize=10)
    ax.set_ylabel("Density", fontsize=10)
    ax.set_title("Simulated inter-event time distribution", fontsize=12)

    ax.grid(alpha=0.2)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.tick_params(labelsize=9)

    ax.legend(frameon=False, fontsize=9)

    figA.tight_layout()

    plt.savefig(
        "inter_event_time_distribution_simulated.png", dpi=300, bbox_inches="tight"
    )
    plt.show()

    ## Average Inter-Event Time Distribution##

    figB, ax = plt.subplots(figsize=(8, 5))

    ax.hist(
        t_obs_sim_data,
        bins=60,
        density=True,
        alpha=0.9,
        color="black",
        edgecolor="none",
        label="Windowed averages",
    )

    ax.axvline(
        600,
        color="red",
        linestyle="--",
        linewidth=2,
        label="Reference (600 sec)",
    )

    ax.set_xlabel("Averaged inter-event time $\\Delta t_{obs}$ [sec]", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.set_title("Simulated averaged inter-event time distribution", fontsize=14)

    ax.grid(alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False)

    figB.tight_layout()
    plt.savefig("distribution_average_iet.png", dpi=300)
    plt.show()

    ## Evolution of simulated averaged inter-event time ##

    figC, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        k,
        t_obs_sim_data,
        color="black",
        linewidth=1.5,
        label="Simulated averaged inter-event time",
    )

    ax.axhline(
        t_ref,
        linestyle="--",
        linewidth=2,
        color="red",
        label=f"Reference ({t_ref:.0f} sec)",
    )

    ax.axhline(
        total_avg_time_sim,
        linestyle="--",
        linewidth=2,
        color="#f7931a",
        label=f"Simulated mean ({total_avg_time_sim:.1f} sec)",
    )

    ax.set_xlabel("Adjustment window $k$", fontsize=12)
    ax.set_ylabel("Averaged inter-event time $\\Delta t_{obs}$ [sec]", fontsize=12)
    ax.set_title("Evolution of simulated averaged inter-event time", fontsize=14)

    ax.grid(alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False, loc="upper left")

    figC.tight_layout()
    plt.savefig("evolution_averaged_iet.png", dpi=300)
    plt.show()

    ## Relative devation in the averaged inter-event time ##

    figD, ax = plt.subplots(figsize=(8, 5))

    t_obs_sim = np.asarray(t_obs_sim_data, dtype=float)
    t_obs_real = np.asarray(t_obs_real_data, dtype=float)

    min_len = min(len(t_obs_sim), len(t_obs_real))
    t_obs_sim = t_obs_sim[:min_len]
    t_obs_real = t_obs_real[:min_len]
    k_plot = np.arange(min_len)

    rel_error = (t_obs_sim - t_obs_real) / t_obs_real

    ax.plot(
        k_plot,
        rel_error,
        color="black",
        linewidth=1.5,
        label="Relative averaged inter-event time deviation",
    )

    mean_error = np.mean(rel_error)
    ax.axhline(
        mean_error,
        color="#f7931a",
        linestyle="--",
        linewidth=2,
        label=f"Mean error ({mean_error:.3e})",
    )

    ax.set_xlabel("Adjustment window $k$", fontsize=12)
    ax.set_ylabel("Relative deviation", fontsize=12)
    ax.set_title("Relative deviation in averaged inter-event time: model vs real data")

    ax.grid(alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False)

    figD.tight_layout()
    plt.savefig("relative_deviation_avg_iet.png", dpi=300)
    plt.show()

    # # Evolution of Bitcoin difficulty: model vs real data ##

    figE, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        k,
        d_sim_data,
        color="black",
        linewidth=1.5,
        alpha=1,
        label="Simulated difficulty",
    )

    ax.plot(
        k,
        difficulty_real_data,
        linestyle="--",
        color="#f7931a",
        linewidth=1.5,
        alpha=1,
        label="Bitcoin difficulty (real data)",
    )

    ax.set_xlabel("Adjustment window $k$", fontsize=12)
    ax.set_ylabel("Difficulty", fontsize=12)
    ax.set_title("Evolution of Bitcoin difficulty: model vs real data", fontsize=14)

    ax.set_yscale("log")

    ax.grid(alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False, loc="upper left")

    figE.tight_layout()
    plt.savefig("evolution_of_diff_model_vs_realdata.png", dpi=300)
    plt.show()

    ## Evoltuion of Bitcoin difficulty vs simluated difficulty zoomed in ##

    figF, ax = plt.subplots(figsize=(8, 5))

    k_zoom = k[-50:]
    d_sim_zoom = d_sim_data[-50:]
    d_real_zoom = difficulty_real_data[-50:]

    ax.plot(
        k_zoom,
        d_sim_zoom,
        color="black",
        linewidth=1.5,
        alpha=1,
        label="Simulated difficulty",
    )

    ax.plot(
        k_zoom,
        d_real_zoom,
        linestyle="--",
        color="#f7931a",
        linewidth=1.5,
        alpha=1,
        label="Bitcoin difficulty (real data)",
    )

    ax.set_xlabel("Adjustment window $k$", fontsize=12)
    ax.set_ylabel("Difficulty", fontsize=12)
    ax.set_title(
        "Evolution of Bitcoin difficulty (last 50 adjustment windows)",
        fontsize=14,
    )

    ax.set_yscale("log")

    ax.grid(alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False, loc="upper left")

    figF.tight_layout()
    plt.savefig("evolution_of_diff_model_vs_realdata_zoomed.png", dpi=300)
    plt.show()

    # # Relative deviaiton of simulated difficulty vs real Bitcoin difficulty ##

    figG, ax = plt.subplots(figsize=(8, 5))

    d_sim_array = np.asarray(d_sim_data, dtype=float)
    d_real_array = np.asarray(difficulty_real_data, dtype=float)

    relative_error = (d_sim_array - d_real_array) / d_real_array

    ax.plot(
        np.arange(len(d_sim_array)),
        relative_error,
        color="black",
        linewidth=1.5,
        label="Relative difficulty deviation",
    )

    mean_error = np.mean(relative_error)
    ax.axhline(
        mean_error,
        color="#f7931a",
        linestyle="--",
        linewidth=2,
        label=f"Mean error ({mean_error:.3e})",
    )

    ax.set_xlabel("Adjustment window $k$", fontsize=12)
    ax.set_ylabel(
        "Relative deviation",
        fontsize=12,
    )
    ax.set_title(
        "Relative deviation in difficulty adjustment: model vs real data", fontsize=14
    )

    ax.grid(alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="best")

    figG.tight_layout()
    plt.savefig("difficulty_relative_deviatoin.png", dpi=300)
    plt.show()

    ## Hash-rate exponential model vs real hash-rate dynamics ##

    figH, ax = plt.subplots(figsize=(8, 5))

    ax.set_xlabel("Adjustment window $k$", fontsize=12)
    ax.set_ylabel("Hash rate [hashes/sec]", fontsize=12)

    ax.plot(
        k,
        estimated_hash_rate_model,
        color="black",
        linewidth=2,
        label="Exponential model",
    )

    ax.plot(
        k,
        hash_rate_real_data,
        color="#f7931a",
        linewidth=2,
        label="Real hash-rate",
    )

    ax.grid(alpha=0.2)
    ax.set_yscale("log")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False, loc="upper left")

    figH.tight_layout()
    plt.savefig("estimated_hashrate_model_vs_real_log.png", dpi=300)
    plt.show()

    # delayed response from difficulty (last 50 windows) ##

    fig, ax1 = plt.subplots(figsize=(8, 5))

    k_zoom = np.asarray(k)[-50:]
    d_sim_zoom = np.asarray(d_sim_data)[-50:]
    h_real_zoom = np.asarray(hash_rate_real_data)[-50:]

    ax1.plot(
        k_zoom,
        d_sim_zoom,
        color="#f7931a",
        linewidth=2,
        label="Simulated difficulty",
    )

    ax1.set_xlabel("Adjustment window $k$")
    ax1.set_ylabel("Difficulty")
    ax1.set_yscale("log")

    ax2 = ax1.twinx()
    ax2.plot(
        k_zoom,
        h_real_zoom,
        color="black",
        linewidth=1.5,
        alpha=0.8,
        label="Estimated hash-rate",
    )
    ax2.set_ylabel("Hash-rate [hashes/sec]", color="black")
    ax2.set_yscale("log")

    ax1.grid(alpha=0.2)
    ax1.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)

    ax1.set_title("Delayed response of difficulty (last 50 adjustment windows)")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, frameon=False)

    fig.tight_layout()
    plt.savefig("delayed_reponse_of_difficulty_vs_est_hashrate.png", dpi=300)
    plt.show()
