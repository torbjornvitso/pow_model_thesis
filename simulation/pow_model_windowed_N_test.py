import matplotlib.pyplot as plt
import numpy as np

from data_io import (
    read_dataset_shock_test,
    write_sim_data,
    HASH_RATE_SHOCK_DATA,
    SIM_RESULTS_SHOCK_TEST,
)
from plots import plot_sim_data_shock_test
from data_pre_process import hashrate_shock_simulation_data
from pow_functions import (
    bounded_correction_map,
    calculate_inter_event_times_btc,
    difficulty_adjustment_update_btc,
    error_ratio,
    event_rate,
    low_pass_filter,
    probability_of_success_btc,
    timestamps,
)

h_shock_test_data = []
d_shock_test_data = []

h_sim_data = []
d_sim_data = []
p_k_sim_data = []
lambda_k_sim_data = []
t_sim_data = []
delta_t_sim_data = []
t_obs_sim_data = []
e_k_sim_data = []
u_k_sim_data = []


def pow_feedback_mechanism_windowed_bounded_proportional_controller_N_test(
    N: int,
    T_ref: int,
    e_min: float,
    e_max: float,
    u_min: float,
    u_max: float,
    processed_data_path: str,
    sim_data_path: str,
    num_window_k: int,
    h0: int,
    gain: int,
    delta_t_list: list,
    all_delta_t_list: list,
):
    hashrate_shock_simulation_data(num_window_k, h0, gain, processed_data_path)

    read_dataset_shock_test(processed_data_path, h_shock_test_data, d_shock_test_data)
    d_0 = d_shock_test_data[0]
    u_0 = 1
    t_0 = 0

    d_k = d_0 * u_0
    t_i = t_0

    delta_t_sum = 0

    for h_k in h_shock_test_data:
        h_sim_data.append(h_k)
        d_sim_data.append(d_k)

        p_k = probability_of_success_btc(d_k)
        lambda_k = event_rate(h_k, p_k)
        t_i_k = timestamps(lambda_k, N, t_i)
        delta_t_i_k = calculate_inter_event_times_btc(t_i_k)
        T_obs_k = low_pass_filter(delta_t_i_k)
        e_k = error_ratio(T_obs_k, T_ref)
        u_k = bounded_correction_map(e_k, e_min, e_max, u_min, u_max)
        d_k_plus_one = difficulty_adjustment_update_btc(d_k, u_k)

        d_k = d_k_plus_one
        t_i = t_i_k[-1]

        p_k_sim_data.append(p_k)
        lambda_k_sim_data.append(lambda_k)
        t_sim_data.append(t_i_k)
        delta_t_sim_data.append(delta_t_i_k)
        t_obs_sim_data.append(T_obs_k)
        e_k_sim_data.append(e_k)
        u_k_sim_data.append(u_k)

        delta_t_sum += T_obs_k
        all_delta_t.append(T_obs_k)

    delta_t_sum = delta_t_sum / len(h_shock_test_data)
    delta_t_list.append(delta_t_sum)

    # write_sim_data(
    #     sim_data_path,
    #     h_sim_data,
    #     d_sim_data,
    #     delta_t_sim_data,
    #     p_k_sim_data,
    #     lambda_k_sim_data,
    #     t_obs_sim_data,
    #     e_k_sim_data,
    #     u_k_sim_data,
    # )


if __name__ == "__main__":
    N_list = [4000]
    delta_t = []
    all_delta_t = []
    for N in N_list:
        pow_feedback_mechanism_windowed_bounded_proportional_controller_N_test(
            N,
            600,
            0.25,
            4,
            0.25,
            4,
            HASH_RATE_SHOCK_DATA,
            SIM_RESULTS_SHOCK_TEST,
            1000,
            7158278.827,
            1,
            delta_t,
            all_delta_t,
        )

    print(delta_t)
    print(all_delta_t)

    inside_sd = 0

    for d_t in all_delta_t:
        if 586.64 <= d_t <= 613.36:
            inside_sd += 1

    print("inside_sd: ", inside_sd)

    plt.figure(figsize=(8, 5))

    plt.plot(N_list, delta_t, marker="o", color="orange", label="Observed block time")

    plt.axhline(y=600, linestyle="--", color="black", label="Reference (600 sec)")

    plt.xlabel("Window size N")
    plt.ylabel("Average block time [sec]")
    plt.title("Effect of window size on block time")

    plt.legend()
    plt.grid()
    plt.savefig("N_test.png", bbox_inches="tight")
    plt.show()

    N = 2016
    std_theoretical = 600 / np.sqrt(N)

    print("Theoretical std:", std_theoretical)

    k_all = range(len(all_delta_t))

    plt.figure(figsize=(10, 5))

    plt.plot(
        k_all, all_delta_t, color="orange", linewidth=1, label="All inter-event times"
    )

    plt.axhline(y=600, linestyle="--", color="black", label="Reference (600 sec)")
    plt.axhline(
        y=600 + std_theoretical,
        linestyle="--",
        color="red",
        label=f"+1 std ({600 + std_theoretical:.2f} sec)",
    )
    plt.axhline(
        y=600 - std_theoretical,
        linestyle="--",
        color="blue",
        label=f"-1 std ({600 - std_theoretical:.2f} sec)",
    )

    plt.xlabel("Event index")
    plt.ylabel("Inter-event time [sec]")
    plt.title("All inter-event times with theoretical ±1 standard deviation")
    plt.legend()
    plt.grid(True)
    plt.savefig("all_delta_t_with_std.png", bbox_inches="tight")
    plt.show()
