import numpy as np
import matplotlib.pyplot as plt

from data_io import (
    read_dataset_shock_test,
    HASH_RATE_SHOCK_DATA,
)

from data_pre_process import hashrate_shock_simulation_data_eth
from pow_functions import (
    probability_of_success_eth,
    event_rate,
    timestamps,
    calculate_inter_event_times_eth,
    quantized_timing_index,
    quantized_correction_map,
    difficulty_adjustment_update_eth,
    low_pass_filter,
)


def single_shock_test(
    N: int,
    phi: int,
    u_min: float,
    u_max: float,
    h_shock_test_data: list,
    d0: int,
):

    h_sim_data = []
    d_sim_data = []
    p_k_sim_data = []
    lambda_k_sim_data = []
    t_sim_data = []
    delta_t_sim_data = []
    t_obs_sim_data = []
    e_k_sim_data = []
    u_k_sim_data = []

    t0 = 0

    t_i = t0
    d_k = d0

    for h_k in h_shock_test_data:
        h_sim_data.append(h_k)
        d_sim_data.append(d_k)

        p_k = probability_of_success_eth(d_k)
        lambda_k = event_rate(h_k, p_k)
        t_i_k = timestamps(lambda_k, N, t_i)
        delta_t_i_k = calculate_inter_event_times_eth(t_i_k, t_i)
        T_obs_k = low_pass_filter(delta_t_i_k)
        e_k = quantized_timing_index(T_obs_k, phi)
        u_k = quantized_correction_map(e_k, u_min, u_max)
        d_k_plus_one = difficulty_adjustment_update_eth(d_k, u_k)

        d_k = d_k_plus_one
        t_i = t_i_k[-1]

        p_k_sim_data.append(p_k)
        lambda_k_sim_data.append(lambda_k)
        t_sim_data.append(t_i_k)
        delta_t_sim_data.append(delta_t_i_k)
        t_obs_sim_data.append(T_obs_k)
        e_k_sim_data.append(e_k)
        u_k_sim_data.append(u_k)

    return {
        "d": np.asarray(d_sim_data, dtype=float),
        "t_obs": np.asarray(t_obs_sim_data, dtype=float),
        "u": np.asarray(u_k_sim_data, dtype=float),
    }


def eth_monte_carlo_shock_test(
    num_sim: int,
    N: int,
    phi: int,
    u_min: float,
    u_max: float,
    processed_data_path: str,
    num_window_k: int,
    h0: int,
    gain: int,
):
    hashrate_shock_simulation_data_eth(num_window_k, h0, gain, processed_data_path)

    h_shock_test_data = []
    d_shock_test_data = []

    read_dataset_shock_test(processed_data_path, h_shock_test_data, d_shock_test_data)

    d_0 = d_shock_test_data[0]

    d_all_sim = []
    t_obs_all_sim = []
    u_all_sim = []

    for i in range(num_sim):
        print(f"Monte Carlo simulation {i + 1}/{num_sim}")

        single_sim_data = single_shock_test(
            N=N,
            phi=phi,
            u_min=u_min,
            u_max=u_max,
            h_shock_test_data=h_shock_test_data,
            d0=d_0,
        )

        d_all_sim.append(single_sim_data["d"])
        t_obs_all_sim.append(single_sim_data["t_obs"])
        u_all_sim.append(single_sim_data["u"])

    d_all_sim = np.vstack(d_all_sim)
    t_obs_all_sim = np.vstack(t_obs_all_sim)
    u_all_sim = np.vstack(u_all_sim)

    return {
        "gain": gain,
        "hash_sim_data": h_shock_test_data,
        "difficulty_mean": np.mean(d_all_sim, axis=0),
        "difficulty_pertcentile_downwards": np.percentile(d_all_sim, 5, axis=0),
        "difficulty_pertcentile_upwards": np.percentile(d_all_sim, 95, axis=0),
        "correction_term_mean": np.mean(u_all_sim, axis=0),
        "correction_term_downwards": np.percentile(u_all_sim, 5, axis=0),
        "correction_term_upwards": np.percentile(u_all_sim, 95, axis=0),
        "inter_event_time_mean": np.mean(t_obs_all_sim, axis=0),
        "inter_event_time_downwards": np.percentile(t_obs_all_sim, 5, axis=0),
        "inter_event_time_upwards": np.percentile(t_obs_all_sim, 95, axis=0),
    }


def plot_monte_carlo_sim(sim_data):
    k = np.arange(len(sim_data["difficulty_mean"]))

    fig, ax1 = plt.subplots(figsize=(8, 5))

    ax1.plot(
        k,
        sim_data["difficulty_mean"],
        color="#5F73E6",
        linewidth=2,
        label="Difficulty mean",
    )

    ax1.fill_between(
        k,
        sim_data["difficulty_pertcentile_downwards"],
        sim_data["difficulty_pertcentile_upwards"],
        color="#5F73E6",
        alpha=0.12,
        label="Range of difficulty realizations",
    )

    ax1.set_xlabel("Adjustment window $k$", fontsize=12)
    ax1.set_ylabel("Difficulty", fontsize=12)
    ax1.set_yscale("log")
    ax1.grid(alpha=0.2)

    ax2 = ax1.twinx()

    ax2.plot(
        k,
        sim_data["hash_sim_data"],
        color="black",
        linewidth=2,
        label="Constant hash-rate input",
    )

    ax2.set_ylabel("Hash-rate [hashes/sec]", fontsize=12)
    ax2.set_yscale("log")

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax2.spines["top"].set_visible(False)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(
        lines1 + lines2,
        labels1 + labels2,
        frameon=False,
        loc="lower right",
    )

    ax1.set_title("Stochastic difficulty response", fontsize=14)

    fig.tight_layout()
    plt.savefig("monte_carlo_mean_difficulty_response.png", dpi=300)
    plt.show()

    ## Mean behvaior of eth around equillibrium, with time constant comparance ##

    fig, ax1 = plt.subplots(figsize=(8, 5))

    difficulty_from_shock_start = sim_data["difficulty_mean"][1000:]
    k = np.arange(len(difficulty_from_shock_start))

    ax1.plot(
        k,
        difficulty_from_shock_start,
        color="#5F73E6",
        linewidth=2,
        label="Monte Carlo mean",
    )

    ax1.set_xlabel("Adjustment window $k$", fontsize=12)
    ax1.set_ylabel("Difficulty", fontsize=12)
    ax1.set_yscale("log")
    ax1.grid(alpha=0)

    tau = 1477

    tau_ticks = [
        0,
        tau,
        2 * tau,
        3 * tau,
        4 * tau,
        5 * tau,
        6 * tau,
    ]

    ax1.set_xticks(tau_ticks)

    ax1.set_xticklabels(
        [
            "0",
            "1477",
            "2954",
            "4431",
            "5908",
            "7385",
            "8862",
        ]
    )

    ax1.axvline(
        tau,
        color="gray",
        linestyle=":",
        alpha=0.25,
        linewidth=1,
    )

    ax1.axvline(
        2 * tau,
        color="gray",
        linestyle=":",
        alpha=0.25,
        linewidth=1,
    )

    ax1.axvline(
        3 * tau,
        color="gray",
        linestyle=":",
        alpha=0.25,
        linewidth=1,
    )

    ax1.axvline(
        4 * tau,
        color="gray",
        linestyle=":",
        alpha=0.25,
        linewidth=1,
    )

    ax1.axvline(
        5 * tau,
        color="gray",
        linestyle=":",
        alpha=0.25,
        linewidth=1,
    )

    ax1.axvline(
        6 * tau,
        color="gray",
        linestyle=":",
        alpha=0.25,
        linewidth=1,
    )

    ax2.axhline(
        63.2,
        color="gray",
        linestyle="--",
        linewidth=1,
        alpha=0.25,
    )

    ax2.axhline(
        86.5,
        color="gray",
        linestyle="--",
        linewidth=1,
        alpha=0.25,
    )

    ax2.axhline(
        95.0,
        color="gray",
        linestyle="--",
        linewidth=1,
        alpha=0.25,
    )

    ax2.text(
        len(k) * 0.01,
        63.2 + 1.5,
        r"$\tau$",
        fontsize=12,
        color="gray",
    )

    ax2.text(
        len(k) * 0.01,
        86.5 + 1.5,
        r"$2\tau$",
        fontsize=12,
        color="gray",
    )

    ax2.text(
        len(k) * 0.01,
        95.0 + 1.5,
        r"$3\tau$",
        fontsize=12,
        color="gray",
    )

    # ax2.set_ylim(conv_min, conv_max)
    ax2.set_ylabel("Recovery [%]", fontsize=12)

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax2.spines["top"].set_visible(False)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(
        lines1 + lines2,
        labels1 + labels2,
        frameon=False,
        loc="upper right",
    )

    ax1.set_title("Mean difficulty recovery under hash-rate shock", fontsize=14)

    fig.tight_layout()
    plt.savefig("monte_carlo_mean_difficulty_response_time_constant.png", dpi=300)
    plt.show()

    ## Correction term ##

    fig, ax = plt.subplots(figsize=(8, 5))

    u_mean = sim_data["correction_term_mean"]
    u_p00 = sim_data["correction_term_downwards"]
    u_p100 = sim_data["correction_term_upwards"]

    u_mean = sim_data["correction_term_mean"]

    k = np.arange(len(u_mean))

    ax.plot(
        k,
        u_mean,
        color="#5F73E6",
        linewidth=2,
        label=r"Mean correction term $\bar{u}_k$",
    )

    ax.fill_between(
        k,
        u_p00,
        u_p100,
        color="#5F73E6",
        alpha=0.15,
        label="Full simulation range",
    )

    ax.axhline(
        0,
        color="black",
        linewidth=1,
        linestyle="--",
        alpha=0.7,
    )

    ax.set_xlabel(r"Adjustment window $k$", fontsize=12)

    ax.set_ylabel(r"Correction term $u_k$", fontsize=12)

    ax.set_title(
        "Correction term response",
        fontsize=14,
    )

    ax.grid(alpha=0.2)

    ax.spines["top"].set_visible(False)

    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False, loc="lower right")

    fig.tight_layout()

    plt.savefig("monte_carlo_correction_term_response.png", dpi=300)

    plt.show()

    ## Inter-event time ##

    fig, ax = plt.subplots(figsize=(8, 5))

    t_mean = sim_data["inter_event_time_mean"]
    t_p00 = sim_data["inter_event_time_downwards"]
    t_p100 = sim_data["inter_event_time_upwards"]

    k = np.arange(len(u_mean))

    mean_t_value = np.mean(t_mean)

    ax.plot(
        k,
        t_mean,
        color="#5F73E6",
        linewidth=2,
        label=rf"Mean inter-event time ({mean_t_value:.2f} s)",
    )

    ax.fill_between(
        k,
        t_p00,
        t_p100,
        color="#5F73E6",
        alpha=0.15,
        label="Range of inter-event time realizations",
    )

    ax.axhline(
        0,
        color="black",
        linewidth=1,
        linestyle="--",
        alpha=0.7,
    )

    ax.set_xlabel(r"Block index $k$", fontsize=12)

    ax.set_ylabel(r"Inter-event time $t_{obs,k}$", fontsize=12)

    ax.set_title(
        "Inter-event time",
        fontsize=14,
    )

    ax.grid(alpha=0.2)

    ax.spines["top"].set_visible(False)

    ax.spines["right"].set_visible(False)

    ax.legend(frameon=False, loc="lower right")

    fig.tight_layout()

    plt.savefig("monte_carlo_inter_event_time_response.png", dpi=300)

    plt.show()


if __name__ == "__main__":
    results = eth_monte_carlo_shock_test(
        1000,
        1,
        10,
        -99,
        1,
        HASH_RATE_SHOCK_DATA,
        10000,
        2.98 * (10**14),
        2,
    )

    plot_monte_carlo_sim(results)
