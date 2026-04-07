from data_io import read_dataset_eth, write_sim_data
from data_pre_process import pre_process_data_eth
from plots import eth_plot_sim_data
from pow_functions import (
    probability_of_success_eth,
    event_rate,
    timestamps,
    calculate_inter_event_times_eth,
    quantized_timing_index,
    quantized_correction_map,
    difficulty_adjustment_update_eth,
    difficulty_bomb,
    low_pass_filter,
)

h_real_data = []
d_real_data = []
t_real_data = []

h_sim_data = []
d_sim_data = []
p_k_sim_data = []
lambda_k_sim_data = []
t_sim_data = []
delta_t_sim_data = []
t_obs_sim_data = []
e_k_sim_data = []
u_k_sim_data = []


def pow_feedback_mechanism_incremental_bounded_proportional_controller(
    N: int,
    phi: int,
    u_min: int,
    u_max: int,
    processed_data_path: str,
    sim_data_path: str,
    from_blockheight: int,
    to_blockheight: int,
):
    pre_process_data_eth(from_blockheight, to_blockheight)

    read_dataset_eth(processed_data_path, h_real_data, d_real_data, t_real_data)

    d_0 = d_real_data[0]
    t_0 = 0

    t_i = t_0
    d_k = d_0

    k = 1

    for h_k in h_real_data:
        block_number = from_blockheight + k
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
        # d_k_plus_one += difficulty_bomb(block_number, 9700000)

        d_k = d_k_plus_one
        t_i = t_i_k[-1]
        k += 1

        p_k_sim_data.append(p_k)
        lambda_k_sim_data.append(lambda_k)
        t_sim_data.append(t_i_k)
        delta_t_sim_data.append(delta_t_i_k)
        t_obs_sim_data.append(T_obs_k)
        e_k_sim_data.append(e_k)
        u_k_sim_data.append(u_k)

    write_sim_data(
        sim_data_path,
        h_sim_data,
        d_sim_data,
        delta_t_sim_data,
        p_k_sim_data,
        lambda_k_sim_data,
        t_obs_sim_data,
        e_k_sim_data,
        u_k_sim_data,
    )

    eth_plot_sim_data(13, processed_data_path, sim_data_path)
