import matplotlib.pyplot as plt
import numpy as np

from data_io import read_dataset_eth, read_sim_data

hash_rate_real_data = []
difficulty_real_data = []
t_obs_real_data = []
t_total = []
u_k_real = []

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


def eth_plot_sim_data(processed_dataset_path: str, sim_data_results_path: str):

    read_dataset_eth(
        processed_dataset_path,
        hash_rate_real_data,
        difficulty_real_data,
        t_total,
        u_k_real,
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

    k = range(len(hash_rate_real_data))

    ## Inter-event time distribution simulated ##

    figA, ax = plt.subplots(figsize=(8, 5))

    ax.hist(
        t_obs_sim_data,
        bins=120,
        density=True,
        alpha=0.85,
        color="black",
        edgecolor="none",
        label="Simulated inter-event times",
    )

    mean_time = np.mean(t_obs_sim_data)
    ax.axvline(
        mean_time,
        color="#5F73E6",
        linestyle="--",
        linewidth=2,
        label=f"Mean inter-event time ({mean_time:.2f})",
    )

    ax.set_xlim(left=0)
    ax.set_xlabel("Inter-event time Δt [sec]", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.set_title("Simulated inter-event time distribution", fontsize=14)
    ax.grid(alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False)

    figA.tight_layout()
    plt.savefig("inter_event_time_distribution_simulated_eth.png", dpi=300)
    plt.show()

    # Inter-event time distribution real Ethereum ##

    figD, ax = plt.subplots(figsize=(8, 5))

    bins = np.arange(0, max(t_total), 1)

    ax.hist(
        t_total,
        bins=bins,
        density=True,
        alpha=0.9,
        color="#5F73E6",
        edgecolor="none",
        label="Real inter-event times",
    )

    mean_time = np.mean(t_total)
    ax.axvline(
        mean_time,
        color="black",
        linestyle="--",
        linewidth=2,
        label=f"Mean inter-event time ({mean_time:.2f})",
    )

    ax.set_xlim(left=0)

    ax.set_xlabel("Inter-event time Δt [sec]", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.set_title("Ethereum inter-event time distribution (real data)", fontsize=14)

    ax.grid(alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False)

    figD.tight_layout()
    plt.savefig("inter_event_time_distribution_eth_realdata.png", dpi=300)
    plt.show()

    ## Evolution of Bitcoin difficulty vs simulated difficulty ##

    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot lines
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
        color="#5F73E6",
        linewidth=1.5,
        alpha=1,
        label="Ethereum difficulty (real data)",
    )

    # Axes
    ax.set_xlabel("Adjustment $k$", fontsize=12)
    ax.set_ylabel("Difficulty", fontsize=12)
    ax.set_title("Evolution of Ethereum difficulty: model vs real data", fontsize=14)

    # Log scale

    # Style
    ax.grid(alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False, loc="upper left")

    fig.tight_layout()
    plt.savefig("difficulty_comparison.png", dpi=300)
    plt.show()

    # Relative deviaiton of simulated difficulty vs real Ethereum difficulty ##

    # fig_var, ax = plt.subplots(figsize=(8, 5))

    # # Convert to arrays
    # d_sim_array = np.asarray(d_sim_data, dtype=float)
    # d_real_array = np.asarray(difficulty_real_data, dtype=float)

    # # # Relative error
    # relative_error = (d_sim_array - d_real_array) / d_real_array

    # # Plot
    # ax.plot(
    #     np.arange(len(d_sim_array)),
    #     relative_error,
    #     color="black",
    #     linewidth=1.5,
    #     label="Relative difficulty deviation",
    # )

    # # Optional mean error line
    # mean_error = np.mean(relative_error)
    # ax.axhline(
    #     mean_error,
    #     color="#5F73E6",
    #     linestyle="--",
    #     linewidth=2,
    #     label=f"Mean error ({mean_error:.3e})",
    # )

    # # Labels and title
    # ax.set_xlabel("Adjustment window $k$", fontsize=12)
    # ax.set_ylabel(
    #     "Relative deviation",
    #     fontsize=12,
    # )
    # ax.set_title(
    #     "Relative deviation in difficulty adjustment: model vs real data", fontsize=14
    # )

    # # Style
    # ax.grid(alpha=0.2)
    # ax.spines["top"].set_visible(False)
    # ax.spines["right"].set_visible(False)
    # ax.legend(frameon=False, loc="best")

    # fig_var.tight_layout()
    # plt.savefig("difficulty_relative_error.png", dpi=300)
    # plt.show()

    # Evolution of simulated controller term ##

    fig_sim, ax = plt.subplots(figsize=(8, 5))

    k_sim = np.arange(len(u_k_sim_data))

    ax.plot(
        k_sim,
        u_k_sim_data,
        color="black",
        linewidth=1.0,
        label="Simulated correction term",
    )

    mean_sim = np.mean(u_k_sim_data)

    ax.axhline(
        mean_sim,
        color="#5F73E6",
        linestyle="--",
        linewidth=2,
        label=f"Simulated mean ({mean_sim:.4f})",
    )

    ax.set_xlabel(r"Adjustment window $k$", fontsize=12)
    ax.set_ylabel(r"Correction term $u_k$", fontsize=12)

    ax.set_title("Evolution of simulated correction term", fontsize=14)

    ax.grid(alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False)

    fig_sim.tight_layout()
    plt.savefig("u_k_evolution_simulated.png", dpi=300)
    plt.show()

    ## Evolution of real Ethereum correction term ##

    fig_real, ax = plt.subplots(figsize=(8, 5))

    k_real = np.arange(len(u_k_real))

    ax.plot(
        k_real,
        u_k_real,
        color="#667EEA",
        linewidth=1.0,
        label="Real correction term",
    )

    mean_real = np.mean(u_k_real)

    ax.axhline(
        mean_real,
        color="black",
        linestyle="--",
        linewidth=2,
        label=f"Real mean ({mean_real:.4f})",
    )

    ax.set_xlabel(r"Adjustment window $k$", fontsize=12)
    ax.set_ylabel(r"Correction term $u_k$", fontsize=12)

    ax.set_title(
        "Evolution of Ethereum correction term (real data)",
        fontsize=14,
    )

    ax.grid(alpha=0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False)

    fig_real.tight_layout()
    plt.savefig("u_k_evolution_real_eth.png", dpi=300)
    plt.show()

    ## Absolute deviation in controller signal ##

    # fig_err, ax = plt.subplots(figsize=(8, 5))

    # u_sim = np.asarray(u_k_sim_data, dtype=float)
    # u_real = np.asarray(u_k_real, dtype=float)

    # min_len = min(len(u_sim), len(u_real))

    # u_sim = u_sim[:min_len]
    # u_real = u_real[:min_len]

    # k_plot = np.arange(min_len)

    # # Absolute deviation
    # u_error = u_sim - u_real

    # ax.plot(
    #     k_plot,
    #     u_error,
    #     color="black",
    #     linewidth=1.0,
    #     label="Absolute difficulty correction term deviation",
    # )

    # mean_error = np.mean(u_error)

    # ax.axhline(
    #     mean_error,
    #     color="#5F73E6",
    #     linestyle="--",
    #     linewidth=2,
    #     label=f"Mean deviation ({mean_error:.4f})",
    # )

    # ax.set_xlabel(r"Block index $k$", fontsize=12)
    # ax.set_ylabel(r"Absolute deviation $u_k$", fontsize=12)

    # ax.set_title(
    #     "Absolute deviation in difficulty correction term: model vs real data",
    #     fontsize=14,
    # )

    # ax.grid(alpha=0.2)
    # ax.spines["top"].set_visible(False)
    # ax.spines["right"].set_visible(False)

    # ax.legend(frameon=False)

    # fig_err.tight_layout()
    # plt.savefig("u_k_deviation.png", dpi=300)
    # plt.show()
